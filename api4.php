<?php
header("Content-Type: application/json");

ini_set('display_errors', '0');
error_reporting(0);

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

$fastapi_url = "http://127.0.0.1:8000/add_interfaces";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    /* ============================================================
       POST — configure interfaces
       Physical  → insert immediately
       SVI/Tunnel → create job, notify FastAPI, return 202; poller finishes DB write
       ============================================================ */
    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (!is_array($devicedata)
            || empty($devicedata['cred_id'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])) {
            echo json_encode(["status" => "error", "message" => "cred_id and devices[] are required"]);
            exit();
        }

        $credId  = $devicedata['cred_id'];
        $devices = $devicedata['devices'];

        /* ---------- 2. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found"]);
            exit();
        }

        /* ---------- 3. VALIDATE EVERY DEVICE ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );

        $errors    = [];
        $validated = [];

        foreach ($devices as $i => $device) {

            if (!isset($device['id']) || !isset($device['mode']) || empty($device['interfaces'])) {
                $errors[] = "devices[$i]: missing id/mode/interfaces";
                continue;
            }

            $mode  = $device['mode'];
            $devId = $device['id'];

            if (!in_array($mode, ['physical', 'svi', 'tunnel', 'loopback'], true)) {
                $errors[] = "device $devId: bad mode '$mode'";
                continue;
            }

            $devStmt->execute([':id' => $devId]);
            $devRow = $devStmt->fetch(PDO::FETCH_ASSOC);

            if (!$devRow) {
                $errors[] = "device $devId: not found in devices table";
                continue;
            }

            $mgmtIp = $devRow['management_ip'];
            if (($mode === 'svi' || $mode === 'tunnel') && empty($mgmtIp)) {
                $errors[] = "device $devId: no management_ip (required for $mode)";
                continue;
            }

            $validated[] = [
                'id'            => $devId,
                'mode'          => $mode,
                'management_ip' => $mgmtIp,
                'platform'      => $devRow['platform'],
                'version'       => $devRow['ver'],
                'family'        => $devRow['family'],
                'interfaces'    => $device['interfaces']
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

        /* ---------- 4. SPLIT PHYSICAL vs REMOTE ---------- */
        $physical = array_values(array_filter($validated, fn($d) => $d['mode'] === 'physical'));
        $remote   = array_values(array_filter($validated, fn($d) => $d['mode'] !== 'physical'));

        /* ---------- 5. PHYSICAL: WRITE TO DB NOW ---------- */
        $insertedPhysical = 0;
        if (!empty($physical)) {
            $insStmt = $pdo->prepare(
                "INSERT INTO interfaces (device_id, int_name, int_type, description)
                 VALUES (:id, :name, :type, :desc)"
            );
            $pdo->beginTransaction();
            try {
                foreach ($physical as $device) {
                    foreach ($device['interfaces'] as $intf) {
                        $insStmt->execute([
                            ':id'   => $device['id'],
                            ':name' => $intf['name'] ?? '',
                            ':type' => $device['mode'],
                            ':desc' => $intf['desc'] ?? ''
                        ]);
                        $insertedPhysical++;
                    }
                }
                $pdo->commit();
            } catch (Exception $e) {
                $pdo->rollBack();
                echo json_encode(["status" => "error", "message" => "physical insert failed: " . $e->getMessage()]);
                exit();
            }
        }

        /* ---------- 6. NO REMOTE DEVICES? DONE. ---------- */
        if (empty($remote)) {
            echo json_encode([
                "status"   => "success",
                "inserted" => $insertedPhysical,
                "job_id"   => null
            ]);
            exit();
        }

        /* ---------- 7. REMOTE: CREATE JOB, SEND TO FASTAPI ---------- */
        $jobId = bin2hex(random_bytes(16));

        $jobStmt = $pdo->prepare(
            "INSERT INTO jobs (job_id, status, payload)
             VALUES (:id, 'pending', :payload)"
        );
        $jobStmt->execute([
            ':id'      => $jobId,
            ':payload' => json_encode($remote)
        ]);

        $remotePayload = [
            'action'  => 'configure',
            'job_id'  => $jobId,
            'profile' => $profile,
            'devices' => $remote,
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
             error_log("FASTAPI 422 BODY: " . $response); 
// Only mark failed if still pending (don't clobber a running job)
            $pdo->prepare(
                "UPDATE jobs SET status='failed', result=:r
                 WHERE job_id=:id AND status='pending'"
            )->execute([
                ':r'  => "dispatch failed: " . ($curlErr ?: "HTTP $httpCode"),
                ':id' => $jobId
            ]);

            echo json_encode([
                "status"   => "error",
                "message"  => "could not reach fastapi — physical rows were inserted, remote cancelled",
                "job_id"   => $jobId,
                "inserted" => $insertedPhysical
            ]);
            exit();
        }

        echo json_encode([
            "status"   => "accepted",
            "job_id"   => $jobId,
            "inserted" => $insertedPhysical
        ]);
        exit();
    }

    /* ============================================================
       GET — polling (?job=<id>) or list interfaces
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

            // status === 'done' → write remote devices to interfaces, exactly once
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
                        "INSERT INTO interfaces (device_id, int_name, int_type, ip, netmask, description)
                         VALUES (:id, :name, :type, :ip, :netmask, :desc)"
                    );
                    foreach ($remoteList as $device) {
                        foreach ($device['interfaces'] as $intf) {
                            $insStmt->execute([
                                ':id'   => $device['id'],
                                ':name' => $intf['name'] ?? '',
                                ':type' => $device['mode'],
								':ip' => $intf['ip'],
								':netmask' => $intf['netmask'],
                                ':desc' => $intf['desc'] ?? ''
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
                    i.device_id, d.hostname, i.int_id, i.int_type,
                    i.description, i.int_name, i.state as status, i.ip, i.netmask, i.vrf_id, v.vrf_name
                FROM interfaces i
                LEFT JOIN devices d ON d.device_id = i.device_id
                LEFT JOIN vrfs    v ON v.vrf_id    = i.vrf_id
                ORDER BY i.device_id";

        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $grouped = [];
        foreach ($rows as $row) {
            $id = $row['device_id'];
            if (!isset($grouped[$id])) {
                $grouped[$id] = [
                    'device_id'  => $row['device_id'],
                    'hostname'   => $row['hostname'],
                    'interfaces' => []
                ];
            }
            if ($row['int_name'] !== null) {
                $grouped[$id]['interfaces'][] = [
                    'int_id'         => (int)$row['int_id'],
                    'interface_name' => $row['int_name'],
                    'interface_type' => $row['int_type'],
					'ip' => $row['ip'],
					'netmask' => $row['netmask'],
                    'vrf_name'       => $row['vrf_name'],
                    'status'         => $row['status'],
                    'description'    => $row['description']
                ];
            }
        }

        echo json_encode(["status" => "success", "devices" => array_values($grouped)]);
        exit();
    }

    /* ============================================================
       DELETE — remove an interface
       SVI/Tunnel → de-configure on device first, then delete from DB
       Physical   → delete from DB directly
       ============================================================ */
    if ($method === "DELETE") {

        /* ---------- 1. VALIDATE INPUT ---------- */
        if (empty($devicedata['int'])) {
            echo json_encode(["status" => "error", "message" => "missing int id"]);
            exit();
        }
        if (empty($devicedata['cred_id'])) {
            echo json_encode(["status" => "error", "message" => "cred_id is required"]);
            exit();
        }

        $intId  = $devicedata['int'];
        $credId = $devicedata['cred_id'];

        /* ---------- 2. LOOK UP THE INTERFACE + DEVICE ---------- */
        $stmt = $pdo->prepare(
            "SELECT
                 i.int_id,
                 i.device_id,
                 i.int_name           AS interface_name,
                 i.int_type,
				 i.ip,
				 i.netmask,
                 d.management_ip,
                 d.platform,
                 d.ver,
                 d.family
             FROM interfaces i
             LEFT JOIN devices d ON d.device_id = i.device_id
             WHERE i.int_id = :int
             LIMIT 1"
        );
        $stmt->execute([':int' => $intId]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$row) {
            echo json_encode(["status" => "error", "message" => "interface $intId not found"]);
            exit();
        }

        $mode   = strtolower($row['int_type']);
        $devId  = $row['device_id'];
        $ifName = $row['interface_name'];

        /* ---------- 3. SVI/TUNNEL: DE-CONFIGURE ON DEVICE FIRST ---------- */
        if ($mode === 'svi' || $mode === 'tunnel' || $mode === 'loopback') {

            $pstmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
            $pstmt->execute([':id' => $credId]);
            $profile = $pstmt->fetch(PDO::FETCH_ASSOC);

            if (!$profile) {
                echo json_encode(["status" => "error", "message" => "cred_id $credId not found"]);
                exit();
            }

            if (empty($row['management_ip'])) {
                echo json_encode(["status" => "error", "message" => "device $devId: no management_ip — cannot de-configure"]);
                exit();
            }

            $remotePayload = [
                'action'  => 'delete',
                'profile' => $profile,
                'devices' => [[
                    'id'            => $devId,
                    'mode'          => $mode,
                    'management_ip' => $row['management_ip'],
                    'platform'      => $row['platform'],
                    'version'       => $row['version'],
                    'family'        => $row['family'],
                    'interfaces'    => [[
                        'name' => $ifName,
						'ip' =>$row['ip'],
						'netmask'=> $row['netmask'],
                        'desc' => ''
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
                echo json_encode(["status" => "error", "message" => "fastapi unreachable — $curlErr — nothing deleted"]);
                exit();
            }

            $result = json_decode($response, true);

            if ($httpCode < 200 || $httpCode >= 300) {
                $msg = $result['message'] ?? "HTTP $httpCode";
                echo json_encode(["status" => "error", "message" => "fastapi error: $msg — nothing deleted"]);
                exit();
            }
            if (($result['status'] ?? '') !== 'success') {
                $msg = $result['message'] ?? 'unknown';
                echo json_encode(["status" => "error", "message" => "fastapi refused: $msg — nothing deleted"]);
                exit();
            }
        }

        /* ---------- 4. DELETE FROM DB ---------- */
        $stmt = $pdo->prepare("DELETE FROM interfaces WHERE int_id = :int");
        $stmt->execute([':int' => $intId]);

        echo json_encode([
            "status"  => "success",
            "deleted" => $stmt->rowCount(),
            "remote"  => ($mode === 'svi' || $mode === 'tunnel') ? 'ok' : 'skipped'
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