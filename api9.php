<?php
header("Content-Type: application/json");

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

$fastapi_url = "http://127.0.0.1:8000/add_stacks";

try {

    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    /* ============================================================
       POST — stacking operations
       Families: front-panel | back-panel | dad
       Exactly ONE family per request.
       ============================================================ */
    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (empty($devicedata['cred_id'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])
            || empty($devicedata['operation'])) {
            echo json_encode(["status" => "error", "message" => "cred_id, operation and devices[] are required!!👾👾"]);
            exit();
        }

        $credId    = $devicedata['cred_id'];
        $operation = $devicedata['operation'];
        $devices   = $devicedata['devices'];
        $details   = $devicedata['details'] ?? [];

        if (!in_array($operation, ['front-panel','back-panel','dad'], true)) {
            echo json_encode(["status" => "error", "message" => "operation must be front-panel / back-panel / dad!!👾👾"]);
            exit();
        }

        /* ---------- 2. OPERATION-SPECIFIC VALIDATION ---------- */
        if ($operation === 'front-panel') {
            if (count($devices) !== 2) {
                echo json_encode(["status" => "error", "message" => "front-panel requires exactly 2 devices!!👾👾"]);
                exit();
            }
            if (empty($details['master_device_id'])) {
                echo json_encode(["status" => "error", "message" => "master_device_id is required!!👾👾"]);
                exit();
            }
            if (!isset($details['virtual_domain_id']) ||
                !is_numeric($details['virtual_domain_id']) ||
                $details['virtual_domain_id'] < 1 || $details['virtual_domain_id'] > 255) {
                echo json_encode(["status" => "error", "message" => "virtual_domain_id must be 1-255!!👾👾"]);
                exit();
            }
            if (!isset($details['master_chassis_priority']) ||
                !is_numeric($details['master_chassis_priority']) ||
                $details['master_chassis_priority'] < 1 || $details['master_chassis_priority'] > 15) {
                echo json_encode(["status" => "error", "message" => "master_chassis_priority must be 1-15!!👾👾"]);
                exit();
            }
            // every device must carry exactly 2 ports
            foreach ($devices as $d) {
                if (empty($d['ports']) || !is_array($d['ports']) || count($d['ports']) !== 2) {
                    echo json_encode(["status" => "error", "message" => "each front-panel device needs exactly 2 ports!!👾👾"]);
                    exit();
                }
            }
        }

        if ($operation === 'back-panel') {
            if (count($devices) !== 1) {
                echo json_encode(["status" => "error", "message" => "back-panel requires exactly 1 master device!!👾👾"]);
                exit();
            }
            if (empty($details['master_device_id'])) {
                echo json_encode(["status" => "error", "message" => "master_device_id is required!!👾👾"]);
                exit();
            }
            if (!isset($details['master_priority']) ||
                !is_numeric($details['master_priority']) ||
                $details['master_priority'] < 1 || $details['master_priority'] > 15) {
                echo json_encode(["status" => "error", "message" => "master_priority must be 1-15!!👾👾"]);
                exit();
            }
            if (empty($details['members']) || !is_array($details['members'])) {
                echo json_encode(["status" => "error", "message" => "members[] is required!!👾👾"]);
                exit();
            }
            if (count($details['members']) < 1 || count($details['members']) > 8) {
                echo json_encode(["status" => "error", "message" => "members must be 1-8!!👾👾"]);
                exit();
            }
            foreach ($details['members'] as $i => $m) {
                if (empty($m['sku_designation']) || !isset($m['switch_number']) ||
                    !is_numeric($m['switch_number']) ||
                    $m['switch_number'] < 1 || $m['switch_number'] > 8) {
                    echo json_encode(["status" => "error", "message" => "members[$i] needs sku_designation and switch_number 1-8!!👾👾"]);
                    exit();
                }
            }
        }

        if ($operation === 'dad') {
            if (count($devices) !== 1) {
                echo json_encode(["status" => "error", "message" => "DAD requires exactly 1 device!!👾👾"]);
                exit();
            }
            foreach ($devices as $d) {
                if (empty($d['ports']) || !is_array($d['ports']) || count($d['ports']) !== 2) {
                    echo json_encode(["status" => "error", "message" => "DAD device needs exactly 2 ports!!👾👾"]);
                    exit();
                }
            }
        }

        /* ---------- 3. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found 👾👾"]);
            exit();
        }

        /* ---------- 4. VALIDATE EVERY DEVICE ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );

        $intStmt = $pdo->prepare(
            "SELECT int_id, int_name
             FROM interfaces
             WHERE device_id = :dev AND int_id = :int
             LIMIT 1"
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

            if (empty($devRow['management_ip'])) {
                $errors[] = "device $devId: no management_ip (required!!👾👾)";
                continue;
            }

            $entry = [
                'id'            => $devId,
                'management_ip' => $devRow['management_ip'],
                'platform'      => $devRow['platform'],
                'version'       => $devRow['ver'],
                'family'        => $devRow['family'],
            ];

            // Validate ports (front-panel and dad)
            if ($operation === 'front-panel' || $operation === 'dad') {
                $validatedPorts = [];
                foreach ($device['ports'] as $j => $port) {
                    $intId = $port['int_id'] ?? null;
                    if (empty($intId)) {
                        $errors[] = "device $devId: ports[$j] missing int_id👾👾";
                        continue;
                    }
                    $intStmt->execute([':dev' => $devId, ':int' => (int)$intId]);
                    $intRow = $intStmt->fetch(PDO::FETCH_ASSOC);
                    if (!$intRow) {
                        $errors[] = "device $devId: int_id $intId not found as interface👾👾";
                        continue;
                    }
                    $validatedPorts[] = [
                        'int_id'   => (int)$intRow['int_id'],
                        'int_name' => $intRow['int_name']
                    ];
                }
                $entry['ports'] = $validatedPorts;
            }

            $validated[] = $entry;
        }

        if (!empty($errors)) {
            echo json_encode([
                "status"  => "error",
                "message" => "validation failed — nothing was configured 👾👾",
                "errors"  => $errors
            ]);
            exit();
        }

        /* ---------- 5. CREATE JOB ---------- */
        $jobId = bin2hex(random_bytes(16));

        $jobPayload = [
            'operation' => $operation,
            'details'   => $details,
            'devices'   => $validated
        ];

        $jobStmt = $pdo->prepare(
            "INSERT INTO jobs (job_id, status, payload)
             VALUES (:id, 'pending', :payload)"
        );
        $jobStmt->execute([
            ':id'      => $jobId,
            ':payload' => json_encode($jobPayload)
        ]);

        /* ---------- 6. NOTIFY FASTAPI ---------- */
        $remotePayload = [
            'action'    => 'configure',
            'job_id'    => $jobId,
            'profile'   => $profile,
            'operation' => $operation,
            'details'   => $details,
            'devices'   => $validated,
            'async'     => true
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
       GET — polling (?job=<id>) or list stacks
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
                $operation  = $jobPayload['operation'];
                $details    = $jobPayload['details'];
                $devices    = $jobPayload['devices'];

                $pdo->beginTransaction();
                try {
                    // Idempotency guard
                    $chk = $pdo->prepare("SELECT result FROM jobs WHERE job_id = :id FOR UPDATE");
                    $chk->execute([':id' => $_GET['job']]);
                    $cur = $chk->fetchColumn();

                    if ($cur === 'written') {
                        $pdo->commit();
                        echo json_encode(["status" => "success", "job_id" => $_GET['job']]);
                        exit();
                    }

                    /* ==============================================
                       Prepare statements
                       ============================================== */

                    // Find any existing stack this device belongs to (other than the target)
                    $findDevStack = $pdo->prepare(
                        "SELECT stack_no FROM stacked_devices WHERE device_id = :dev LIMIT 1"
                    );

                    // Remove device from any other stack (its row in stacked_devices)
                    $delDevFromOther = $pdo->prepare(
                        "DELETE FROM stacked_devices WHERE device_id = :dev AND stack_no <> :target"
                    );

                    // Remove stray ports for a device that's leaving a stack
                    $delPortsForDev = $pdo->prepare(
                        "DELETE FROM stack_ports WHERE device_id = :dev AND stack_no <> :target"
                    );

                    // Upsert stacked_devices
                    $upsertSd = $pdo->prepare(
                        "INSERT INTO stacked_devices (device_id, stack_no, role)
                         VALUES (:dev, :stack, :role)
                         ON DUPLICATE KEY UPDATE
                             stack_no = VALUES(stack_no),
                             role     = VALUES(role),
                             updated_at = NOW()"
                    );

                    // Upsert stack_ports
                    $upsertPort = $pdo->prepare(
                        "INSERT INTO stack_ports (stack_no, device_id, int_id)
                         VALUES (:stack, :dev, :int)
                         ON DUPLICATE KEY UPDATE int_id = VALUES(int_id)"
                    );

                    // Insert stack header (master row)
                    $insertStack = $pdo->prepare(
                        "INSERT INTO stack (stack_type, master_id, std_id)
                         VALUES (:type, :master, :std)"
                    );

                    // Update stack header (for existing stacks, e.g. DAD)
                    $updateStack = $pdo->prepare(
                        "UPDATE stack SET std_id = :std WHERE stack_no = :sn"
                    );

                    // Look up stack_no by master
                    $stackByMaster = $pdo->prepare(
                        "SELECT stack_no FROM stack WHERE master_id = :master LIMIT 1"
                    );

                    // Look up stack_no by any device
                    $stackByDevice = $pdo->prepare(
                        "SELECT stack_no FROM stacked_devices WHERE device_id = :dev LIMIT 1"
                    );

                    /* ==============================================
                       6.1  FRONT-PANEL
                       ============================================== */
                    if ($operation === 'front-panel') {

                        $masterId = $details['master_device_id'];
                        $stackNo  = null;

                        // If master already owns a stack row, reuse it; otherwise create
                        $stackByMaster->execute([':master' => $masterId]);
                        $existing = $stackByMaster->fetchColumn();

                        if ($existing !== false) {
                            $stackNo = (int)$existing;
                            $updateStack->execute([':std' => null, ':sn' => $stackNo]);
                        } else {
                            $insertStack->execute([
                                ':type'   => 'front-panel',
                                ':master' => $masterId,
                                ':std'    => null
                            ]);
                            $stackNo = (int)$pdo->lastInsertId();
                        }

                        // For each device: remove from any other stack, then upsert + ports
                        foreach ($devices as $device) {
                            $devId = $device['id'];
                            $role  = ($devId === $masterId) ? 'master' : 'member';

                            $delDevFromOther->execute([':dev' => $devId, ':target' => $stackNo]);
                            $delPortsForDev->execute([':dev' => $devId, ':target' => $stackNo]);
                            $upsertSd->execute([':dev' => $devId, ':stack' => $stackNo, ':role' => $role]);

                            foreach ($device['ports'] as $p) {
                                $upsertPort->execute([
                                    ':stack' => $stackNo,
                                    ':dev'   => $devId,
                                    ':int'   => $p['int_id']
                                ]);
                            }
                        }
                    }

                    /* ==============================================
                       6.2  BACK-PANEL
                       ============================================== */
                    if ($operation === 'back-panel') {

                        $masterId = $details['master_device_id'];
                        $stackNo  = null;

                        $stackByMaster->execute([':master' => $masterId]);
                        $existing = $stackByMaster->fetchColumn();

                        if ($existing !== false) {
                            $stackNo = (int)$existing;
                            $updateStack->execute([':std' => null, ':sn' => $stackNo]);
                        } else {
                            $insertStack->execute([
                                ':type'   => 'back-panel',
                                ':master' => $masterId,
                                ':std'    => null
                            ]);
                            $stackNo = (int)$pdo->lastInsertId();
                        }

                        // Master row
                        $delDevFromOther->execute([':dev' => $masterId, ':target' => $stackNo]);
                        $delPortsForDev->execute([':dev' => $masterId, ':target' => $stackNo]);
                        $upsertSd->execute([':dev' => $masterId, ':stack' => $stackNo, ':role' => 'master']);

                        // Members are logical (SKU + switch_number); no physical device_id yet.
                        // They are recorded in stack header only via members[] payload in jobs.
                        // If you later want to map SKU -> device_id, extend here.
                    }

                    /* ==============================================
                       6.3  DAD  — 1 device, 2 ports
                       ============================================== */
                    if ($operation === 'dad') {

                        // DAD operates on an EXISTING stack this device belongs to.
                        $devId = $devices[0]['id'];

                        $stackByDevice->execute([':dev' => $devId]);
                        $existing = $stackByDevice->fetchColumn();

                        if ($existing === false) {
                            throw new Exception("DAD: device $devId is not in any stack. Create a stack first.");
                        }

                        $stackNo = (int)$existing;

                        // Single device, two DAD ports.
                        // Role is 'master'; std_id is cleared because there is no second physical device.
                        $delDevFromOther->execute([':dev' => $devId, ':target' => $stackNo]);
                        $delPortsForDev->execute([':dev' => $devId, ':target' => $stackNo]);
                        $upsertSd->execute([':dev' => $devId, ':stack' => $stackNo, ':role' => 'master']);

                        foreach ($devices[0]['ports'] as $p) {
                            $upsertPort->execute([
                                ':stack' => $stackNo,
                                ':dev'   => $devId,
                                ':int'   => $p['int_id']
                            ]);
                        }

                        // Update stack header: type becomes 'dad', master set, std cleared
                        $pdo->prepare(
                            "UPDATE stack
                             SET stack_type = 'dad', master_id = :m, std_id = NULL
                             WHERE stack_no = :sn"
                        )->execute([
                            ':m'  => $devId,
                            ':sn' => $stackNo
                        ]);
                    }

                    /* ==============================================
                       STACK-READINESS CHECK before marking written
                       ============================================== */
                    if ($operation === 'front-panel') {
                        $masterId = $details['master_device_id'];
                        $stackByMaster->execute([':master' => $masterId]);
                        $sn = $stackByMaster->fetchColumn();
                        if ($sn === false) throw new Exception("front-panel: no stack row for master $masterId");

                        // All device_ids in payload must be in stacked_devices for this stack
                        foreach ($devices as $device) {
                            $stackByDevice->execute([':dev' => $device['id']]);
                            $ds = $stackByDevice->fetchColumn();
                            if ($ds === false || (int)$ds !== (int)$sn) {
                                throw new Exception("front-panel: device {$device['id']} not registered in stack $sn");
                            }
                        }
                    }

                    if ($operation === 'back-panel') {
                        $masterId = $details['master_device_id'];
                        $stackByDevice->execute([':dev' => $masterId]);
                        $ds = $stackByDevice->fetchColumn();
                        if ($ds === false) throw new Exception("back-panel: master $masterId not registered in stacked_devices");
                    }

                    if ($operation === 'dad') {
                        // Both the device and its 2 DAD ports must be recorded
                        $dadDev = $devices[0]['id'];

                        $stackByDevice->execute([':dev' => $dadDev]);
                        $ds = $stackByDevice->fetchColumn();
                        if ($ds === false) throw new Exception("dad: device $dadDev not registered");

                        $chkPorts = $pdo->prepare(
                            "SELECT COUNT(*) FROM stack_ports WHERE stack_no = :sn AND device_id = :dev"
                        );
                        $chkPorts->execute([':sn' => $stackNo, ':dev' => $dadDev]);
                        if ((int)$chkPorts->fetchColumn() !== 2) {
                            throw new Exception("dad: device $dadDev does not have exactly 2 DAD ports in stack $stackNo");
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
                    s.stack_no,
                    s.stack_type,
                    s.master_id,
                    s.std_id,
                    s.updated_at,
                    d.hostname       AS master_hostname,
                    sd.device_id     AS member_id,
                    sd.role          AS member_role,
                    GROUP_CONCAT(sp.int_id ORDER BY sp.int_id SEPARATOR ',') AS port_ids
                FROM stack s
                LEFT JOIN devices d         ON d.device_id  = s.master_id
                LEFT JOIN stacked_devices sd ON sd.stack_no = s.stack_no
                LEFT JOIN stack_ports sp     ON sp.stack_no = s.stack_no AND sp.device_id = sd.device_id
                GROUP BY s.stack_no, s.stack_type, s.master_id, s.std_id, s.updated_at,
                         d.hostname, sd.device_id, sd.role
                ORDER BY s.stack_no, sd.role";

        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $grouped = [];
        foreach ($rows as $row) {
            $sn = (int)$row['stack_no'];
            if (!isset($grouped[$sn])) {
                $grouped[$sn] = [
                    'stack_no'    => $sn,
                    'stack_type'  => $row['stack_type'],
                    'master_id'   => $row['master_id'],
                    'std_id'      => $row['std_id'],
                    'hostname'    => $row['master_hostname'],
                    'updated_at'  => $row['updated_at'],
                    'devices'     => []
                ];
            }
            if ($row['member_id'] !== null) {
                $grouped[$sn]['devices'][] = [
                    'device_id' => $row['member_id'],
                    'role'      => $row['member_role'],
                    'port_ids'  => $row['port_ids']
                ];
            }
        }

        echo json_encode([
            "status"  => "success",
            "stacks"  => array_values($grouped)
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