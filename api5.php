<?php
header("Content-Type: application/json");

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

$fastapi_url = "http://127.0.0.1:8000/add_vlans";

try {

    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    /* ============================================================
       POST — configure VLANs
       JS payload: { cred_id, devices[], vlans[] }   (vlans are GLOBAL)
       PHP binds global vlans to every device, then forwards to FastAPI.
       ============================================================ */
    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (empty($devicedata['cred_id'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])
            || empty($devicedata['vlans'])
            || !is_array($devicedata['vlans'])) {
            echo json_encode(["status" => "error", "message" => "cred_id, devices[] and vlans[] are required!!👾👾"]);
            exit();
        }

        $credId      = $devicedata['cred_id'];
        $devices     = $devicedata['devices'];
        $globalVlans = $devicedata['vlans'];

        /* ---------- 2. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found 👾👾"]);
            exit();
        }

        /* ---------- 3. VALIDATE EVERY DEVICE, ATTACH GLOBAL VLANS ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );

        $errors    = [];
        $validated = [];

        foreach ($devices as $i => $device) {

            if (empty($device['id'])) {
                $errors[] = "devices[$i]: missing id";
                continue;
            }

            $devId = $device['id'];

            $devStmt->execute([':id' => $devId]);
            $devRow = $devStmt->fetch(PDO::FETCH_ASSOC);

            if (!$devRow) {
                $errors[] = "device $devId: not found in devices table👾👾";
                continue;
            }

            $mgmtIp = $devRow['management_ip'];
            if (empty($mgmtIp)) {
                $errors[] = "device $devId: no management_ip (required!!👾👾)";
                continue;
            }

            $validated[] = [
                'id'            => $devId,
                'management_ip' => $mgmtIp,
                'platform'      => $devRow['platform'],
                'version'       => $devRow['ver'],
                'family'        => $devRow['family'],
                'vlans'         => $globalVlans
            ];
        }

        if (!empty($errors)) {
            echo json_encode([
                "status"  => "error",
                "message" => "validation failed — nothing was configured",
                "errors"  => $errors
            ]);
            exit();
        }

        /* ---------- 4. CREATE JOB ---------- */
        $jobId = bin2hex(random_bytes(16));

        $jobStmt = $pdo->prepare(
            "INSERT INTO jobs (job_id, status, payload)
             VALUES (:id, 'pending', :payload)"
        );
        $jobStmt->execute([
            ':id'      => $jobId,
            ':payload' => json_encode($validated)
        ]);

        /* ---------- 5. NOTIFY FASTAPI ---------- */
        $remotePayload = [
            'action'  => 'configure',
            'job_id'  => $jobId,
            'profile' => $profile,
            'devices' => $validated,
            'async'   => true
        ];

        $json_payload = json_encode($remotePayload);

        $ch = curl_init($fastapi_url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $json_payload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen($json_payload)
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        error_log("SENDING TO FASTAPI: " . $json_payload);

        $response = curl_exec($ch);
        $curlErr  = curl_error($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($response === false || $curlErr !== '' || $httpCode < 200 || $httpCode >= 300) {
            error_log("FASTAPI ERROR BODY: " . $response);

            $pdo->prepare(
                "UPDATE jobs SET status='failed', result=:r
                 WHERE job_id=:id AND status='pending'"
            )->execute([
                ':r'  => "dispatch failed: " . ($curlErr ?: "HTTP $httpCode"),
                ':id' => $jobId
            ]);

            echo json_encode([
                "status"  => "error",
                "message" => "could not reach fastapi👾👾 — remote cancelled",
                "job_id"  => $jobId
            ]);
            exit();
        }

        echo json_encode([
            "status" => "accepted",
            "job_id" => $jobId
        ]);
        exit();
    }

    /* ============================================================
       GET — polling (?job=<id>) or list vlans
       ============================================================ */
    if ($method === "GET") {

        /* ---------- POLLING BRANCH ---------- */
        if (!empty($_GET['job'])) {

            $stmt = $pdo->prepare("SELECT status, result, payload FROM jobs WHERE job_id = :id");
            $stmt->execute([':id' => $_GET['job']]);
            $job = $stmt->fetch(PDO::FETCH_ASSOC);

            if (!$job) {
                echo json_encode(["status" => "error", "message" => "unknown job"]);
                exit();
            }

            if ($job['status'] === 'pending' || $job['status'] === 'running') {
                echo json_encode(["status" => "pending", "job_id" => $_GET['job']]);
                exit();
            }

            if ($job['status'] === 'failed') {
                echo json_encode([
                    "status"  => "error",
                    "job_id"  => $_GET['job'],
                    "message" => $job['result'] ?: "job failed"
                ]);
                exit();
            }

            // status === 'done' → write VLANs to DB, exactly once
            if ($job['status'] === 'done' && $job['result'] !== 'written') {

                $remoteList = json_decode($job['payload'], true);

                $pdo->beginTransaction();
                try {
                    $chk = $pdo->prepare("SELECT result FROM jobs WHERE job_id = :id FOR UPDATE");
                    $chk->execute([':id' => $_GET['job']]);
                    $cur = $chk->fetchColumn();

                    if ($cur === 'written') {
                        $pdo->commit();
                        echo json_encode(["status" => "success", "job_id" => $_GET['job']]);
                        exit();
                    }

                    $insStmt = $pdo->prepare(
                        "INSERT INTO vlans (device_id, vlan_id, vlan_name)
                         VALUES (:id, :vlan_id, :vlan_name)"
                    );

                    foreach ($remoteList as $device) {
                        foreach ($device['vlans'] as $vlan) {
                            $insStmt->execute([
                                ':id'        => $device['id'],
                                ':vlan_id'   => $vlan['id']   ?? '',
                                ':vlan_name' => $vlan['name'] ?? ''
                            ]);
                        }
                    }

                    $pdo->prepare("UPDATE jobs SET result='written' WHERE job_id=:id")
                        ->execute([':id' => $_GET['job']]);

                    $pdo->commit();
                } catch (Exception $e) {
                    $pdo->rollBack();
                    echo json_encode(["status" => "error", "message" => "db write failed: " . $e->getMessage()]);
                    exit();
                }
            }

            echo json_encode(["status" => "success", "job_id" => $_GET['job']]);
            exit();
        }

        /* ---------- LIST BRANCH ---------- */
        $sql = "SELECT
                    v.id           AS vlan_pk,
                    v.device_id,
                    v.vlan_id,
                    v.vlan_name,
                    d.hostname
                FROM vlans v
                LEFT JOIN devices d ON d.device_id = v.device_id
                ORDER BY v.device_id, v.vlan_id";

        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $grouped = [];
        foreach ($rows as $row) {
            $id = $row['device_id'];
            if (!isset($grouped[$id])) {
                $grouped[$id] = [
                    'device_id' => $row['device_id'],
                    'hostname'  => $row['hostname'],
                    'vlans'     => []
                ];
            }
            $grouped[$id]['vlans'][] = [
                'vlan_pk'   => (int)$row['vlan_pk'],
                'vlan_id'   => (int)$row['vlan_id'],
                'vlan_name' => $row['vlan_name']
            ];
        }

        echo json_encode([
            "status"  => "success",
            "devices" => array_values($grouped)
        ]);
        exit();
    }

    /* ============================================================
       DELETE — remove a VLAN
       VLAN → de-configure on device first, then delete from DB
       ============================================================ */
    if ($method === "DELETE") {

        if (empty($devicedata['int'])) {
            echo json_encode(["status" => "error", "message" => "missing vlan id"]);
            exit();
        }
        if (empty($devicedata['cred_id'])) {
            echo json_encode(["status" => "error", "message" => "cred_id is required"]);
            exit();
        }

        $intId  = $devicedata['int'];
        $credId = $devicedata['cred_id'];

        $stmt = $pdo->prepare(
            "SELECT
                 v.id           AS vlan_pk,
                 v.vlan_id,
                 v.vlan_name,
                 v.device_id,
                 d.management_ip,
                 d.platform,
                 d.ver,
                 d.family
             FROM vlans v
             LEFT JOIN devices d ON d.device_id = v.device_id
             WHERE v.id = :int
             LIMIT 1"
        );
        $stmt->execute([':int' => $intId]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row) {
            echo json_encode(["status" => "error", "message" => "vlan $intId not found"]);
            exit();
        }

        $pstmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $pstmt->execute([':id' => $credId]);
        $profile = $pstmt->fetch(PDO::FETCH_ASSOC);

        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found"]);
            exit();
        }

        if (empty($row['management_ip'])) {
            echo json_encode(["status" => "error", "message" => "device {$row['device_id']}: no management_ip — cannot de-configure"]);
            exit();
        }

        $remotePayload = [
            'action'  => 'delete',
            'profile' => $profile,
            'devices' => [[
                'id'            => $row['device_id'],
                'management_ip' => $row['management_ip'],
                'platform'      => $row['platform'],
                'version'       => $row['ver'],
                'family'        => $row['family'],
                'vlans'         => [[
                    'id'   => $row['vlan_id'],
                    'name' => $row['vlan_name']
                ]]
            ]]
        ];

        $json_payload = json_encode($remotePayload);

        $ch = curl_init($fastapi_url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $json_payload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen($json_payload)
        ]);
        curl_setopt($ch, CURLOPT_TIMEOUT, 120);

        $response = curl_exec($ch);
        $curlErr  = curl_error($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($response === false || $curlErr !== '') {
            echo json_encode(["status" => "error", "message" => "fastapi unreachable — $curlErr — nothing deleted👾👾"]);
            exit();
        }

        $result = json_decode($response, true);

        if ($httpCode < 200 || $httpCode >= 300) {
            $msg = $result['message'] ?? "HTTP $httpCode";
            echo json_encode(["status" => "error", "message" => "fastapi error: $msg — nothing deleted👾👾"]);
            exit();
        }
        if (($result['status'] ?? '') !== 'success') {
            $msg = $result['message'] ?? 'unknown';
            echo json_encode(["status" => "error", "message" => "fastapi refused: $msg — nothing deleted👾👾"]);
            exit();
        }

        $stmt = $pdo->prepare("DELETE FROM vlans WHERE id = :int");
        $stmt->execute([':int' => $intId]);

        echo json_encode([
            "status"  => "success",
            "deleted" => $stmt->rowCount()
        ]);
        exit();
    }

} catch (PDOException $e) {
    echo json_encode([
        "status"  => "error",
        "message" => "database failure!!👾👾 : " . $e->getMessage()
    ]);
    exit();
}