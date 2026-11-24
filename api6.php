<?php
header("Content-Type: application/json");

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

$fastapi_url = "http://127.0.0.1:8000/add_trunks_access";

try {

    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    /* ============================================================
       POST — configure trunk / access on physical interfaces
       ============================================================ */
    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (empty($devicedata['cred_id'])
            || empty($devicedata['mode'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])
            || empty($devicedata['vlans'])
            || !is_array($devicedata['vlans'])) {
            echo json_encode(["status" => "error", "message" => "cred_id, mode, devices[] and vlans[] are required!!👾👾"]);
            exit();
        }

        $credId      = $devicedata['cred_id'];
        $mode        = $devicedata['mode'];
        $devices     = $devicedata['devices'];
        $globalVlans = $devicedata['vlans'];
        $vlanAction  = $devicedata['vlan_action'] ?? null;
        $nativeVlan  = $devicedata['native_vlan']  ?? null;

        if (!in_array($mode, ['access', 'trunk'], true)) {
            echo json_encode(["status" => "error", "message" => "mode must be 'access' or 'trunk'!!👾👾"]);
            exit();
        }

        if (empty($vlanAction)) {
            $vlanAction = 'replace';
        }
        if (!in_array($vlanAction, ['add', 'except', 'replace'], true)) {
            echo json_encode(["status" => "error", "message" => "vlan_action must be add/except/replace (or blank)!!👾👾"]);
            exit();
        }

        if (!empty($nativeVlan)) {
            if (!is_numeric($nativeVlan) || $nativeVlan < 1 || $nativeVlan > 4094) {
                echo json_encode(["status" => "error", "message" => "native_vlan must be 1-4094!!👾👾"]);
                exit();
            }
        }

        /* ---------- 2. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found 👾👾"]);
            exit();
        }

        /* ---------- 3. VALIDATE EVERY DEVICE + LOOP ITS SELECTED PORTS ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );

        // One prepared statement, executed once per selected int_id
        $portStmt = $pdo->prepare(
            "SELECT int_id, int_name
             FROM interfaces
             WHERE device_id = :id
               AND int_id = :int_id
               AND int_type IN ('physical', 'port-channel')
             LIMIT 1"
        );

        $errors    = [];
        $validated = [];

        foreach ($devices as $i => $device) {

            if (empty($device['id'])) {
                $errors[] = "devices[$i]: missing id";
                continue;
            }

            if (empty($device['ports']) || !is_array($device['ports'])) {
                $errors[] = "device {$device['id']}: no ports[] selected 👾👾";
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

            // ★ Loop the user-selected ports and accumulate resolved rows
            $ports = [];
            foreach ($device['ports'] as $p) {

                $intId = $p['int_id'] ?? null;
                if (empty($intId)) {
                    continue;
                }

                $portStmt->execute([
                    ':id'     => $devId,
                    ':int_id' => (int)$intId
                ]);
                $row = $portStmt->fetch(PDO::FETCH_ASSOC);

                if ($row) {
                    $ports[] = [
                        'int_id'   => (int)$row['int_id'],
                        'int_name' => $row['int_name']
                    ];
                }
            }

            if (empty($ports)) {
                $errors[] = "device $devId: no matching physical/port-channel interfaces for the selected ports 👾👾";
                continue;
            }

            $validated[] = [
                'id'            => $devId,
                'management_ip' => $mgmtIp,
                'platform'      => $devRow['platform'],
                'version'       => $devRow['ver'],
                'family'        => $devRow['family'],
                'ports'         => $ports
            ];
        }

        if (!empty($errors)) {
            echo json_encode([
                "status"  => "error",
                "message" => "validation failed — nothing was configured 👾👾",
                "errors"  => $errors
            ]);
            exit();
        }

        /* ---------- 4. CREATE JOB ---------- */
        $jobId = bin2hex(random_bytes(16));

        $jobPayload = [
            'mode'        => $mode,
            'vlans'       => $globalVlans,
            'vlan_action' => $vlanAction,
            'native_vlan' => $nativeVlan,
            'devices'     => $validated
        ];

        $jobStmt = $pdo->prepare(
            "INSERT INTO jobs (job_id, status, payload)
             VALUES (:id, 'pending', :payload)"
        );
        $jobStmt->execute([
            ':id'      => $jobId,
            ':payload' => json_encode($jobPayload)
        ]);

        /* ---------- 5. NOTIFY FASTAPI ---------- */
        $remotePayload = [
            'action'      => 'configure',
            'job_id'      => $jobId,
            'profile'     => $profile,
            'mode'        => $mode,
            'vlans'       => $globalVlans,
            'vlan_action' => $vlanAction,
            'native_vlan' => $nativeVlan,
            'devices'     => $validated,
            'async'       => true
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
                "message" => "could not reach fastapi 👾👾 — remote cancelled",
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
       GET — polling (?job=<id>) or list trunk/access config
       ============================================================ */
    if ($method === "GET") {

        /* ---------- POLLING BRANCH ---------- */
        if (!empty($_GET['job'])) {

            $stmt = $pdo->prepare("SELECT status, result, payload FROM jobs WHERE job_id = :id");
            $stmt->execute([':id' => $_GET['job']]);
            $job = $stmt->fetch(PDO::FETCH_ASSOC);

            if (!$job) {
                echo json_encode(["status" => "error", "message" => "unknown job 👾👾"]);
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
                    "message" => $job['result'] ?: "job failed 👾👾"
                ]);
                exit();
            }

            if ($job['status'] === 'done' && $job['result'] !== 'written') {

                $jobPayload = json_decode($job['payload'], true);
                $mode       = $jobPayload['mode'];
                $incoming   = $jobPayload['vlans'];
                $vlanAction = $jobPayload['vlan_action'] ?? 'replace';
                $nativeVlan = $jobPayload['native_vlan'] ?? null;
                $devices    = $jobPayload['devices'];

                $incomingIds = array_values(array_map(
                    fn($v) => (string)($v['id'] ?? ''),
                    $incoming
                ));
                $incomingIds = array_filter($incomingIds, fn($v) => $v !== '');

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

                    $readStmt = $pdo->prepare(
                        "SELECT vlan_ids
                         FROM trunks_access
                         WHERE device_id = :id AND int_id = :int_id
                         LIMIT 1"
                    );

                    $upsert = $pdo->prepare(
                        "INSERT INTO trunks_access
                             (device_id, int_id, mode, vlan_ids, native_vlan, updated_at)
                         VALUES (:id, :int_id, :mode, :vlan_ids, :native_vlan, NOW())
                         ON DUPLICATE KEY UPDATE
                             mode        = VALUES(mode),
                             vlan_ids    = VALUES(vlan_ids),
                             native_vlan = VALUES(native_vlan),
                             updated_at  = NOW()"
                    );

                    foreach ($devices as $device) {
                        foreach ($device['ports'] as $port) {

                            if ($mode === 'access') {
                                $finalIds = [ (string)($incomingIds[0] ?? '') ];
                            } else {
                                $readStmt->execute([
                                    ':id'     => $device['id'],
                                    ':int_id' => $port['int_id']
                                ]);
                                $existing = $readStmt->fetchColumn();
                                $current  = $existing
                                    ? array_map('trim', explode(',', $existing))
                                    : [];
                                $current = array_filter($current, fn($v) => $v !== '');

                                if ($vlanAction === 'add') {
                                    $finalIds = array_values(array_unique(
                                        array_merge($current, $incomingIds)
                                    ));
                                } elseif ($vlanAction === 'except') {
                                    $finalIds = array_values(array_diff($current, $incomingIds));
                                } else {
                                    $finalIds = array_values($incomingIds);
                                }
                            }

                            $finalIds = array_values(array_filter($finalIds, fn($v) => $v !== ''));

                            $upsert->execute([
                                ':id'          => $device['id'],
                                ':int_id'      => $port['int_id'],
                                ':mode'        => $mode,
                                ':vlan_ids'    => implode(',', $finalIds),
                                ':native_vlan' => ($mode === 'trunk' && $nativeVlan !== null)
                                                    ? (int)$nativeVlan
                                                    : null
                            ]);
                        }
                    }

                    $pdo->prepare("UPDATE jobs SET result='written' WHERE job_id=:id")
                        ->execute([':id' => $_GET['job']]);

                    $pdo->commit();
                } catch (Exception $e) {
                    $pdo->rollBack();
                    echo json_encode(["status" => "error", "message" => "db write failed 👾👾: " . $e->getMessage()]);
                    exit();
                }
            }

            echo json_encode(["status" => "success", "job_id" => $_GET['job']]);
            exit();
        }

        /* ---------- LIST BRANCH ---------- */
        $sql = "SELECT
                    t.id             AS row_pk,
                    t.device_id,
                    t.int_id,
                    t.mode,
                    t.vlan_ids,
                    t.native_vlan,
                    t.updated_at,
                    d.hostname,
                    i.int_name
                FROM trunks_access t
                LEFT JOIN devices    d ON d.device_id = t.device_id
                LEFT JOIN interfaces i ON i.int_id    = t.int_id
                ORDER BY t.device_id, t.int_id";

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
                    'ports'     => []
                ];
            }
            $grouped[$id]['ports'][] = [
                'row_pk'      => (int)$row['row_pk'],
                'int_id'      => (int)$row['int_id'],
                'int_name'    => $row['int_name'],
                'mode'        => $row['mode'],
                'vlan_ids'    => $row['vlan_ids'],
                'native_vlan' => $row['native_vlan'],
                'updated_at'  => $row['updated_at']
            ];
        }

        echo json_encode([
            "status"  => "success",
            "devices" => array_values($grouped)
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