<?php
header("Content-Type: application/json");

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

$fastapi_url = "http://127.0.0.1:8000/add_port_channels";

try {

    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    /* ============================================================
       POST — port-channel operations
       Families: portcreation | membercreation | l3portchannel
                 l3subinterfaces | portabolish
       Exactly ONE family per request.
       ============================================================ */
    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (empty($devicedata['cred_id'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])) {
            echo json_encode(["status" => "error", "message" => "cred_id and devices[] are required!!👾👾"]);
            exit();
        }

        $credId  = $devicedata['cred_id'];
        $devices = $devicedata['devices'];

        /* ---------- 2. DETERMINE WHICH OPERATION ---------- */
        $families = ['portcreation', 'membercreation', 'l3portchannel',
                     'l3subinterfaces', 'portabolish'];
        $present  = [];
        foreach ($families as $f) {
            if (!empty($devicedata[$f]) && is_array($devicedata[$f])) {
                $present[] = $f;
            }
        }

        if (count($present) === 0) {
            echo json_encode(["status" => "error", "message" => "one of portcreation / membercreation / l3portchannel / l3subinterfaces / portabolish is required!!👾👾"]);
            exit();
        }
        if (count($present) > 1) {
            echo json_encode(["status" => "error", "message" => "only one operation family per request!!👾👾", "detected" => $present]);
            exit();
        }
        $operation = $present[0];

        /* ---------- 3. VALIDATE THE OPERATION PAYLOAD ---------- */
        $op = $devicedata[$operation];

        if ($operation === 'portcreation') {
            if (empty($op['portchannel_name'])) {
                echo json_encode(["status" => "error", "message" => "portchannel_name is required!!👾👾"]);
                exit();
            }
            if (!isset($op['mode']) || !in_array($op['mode'], ['trunk','access'], true)) {
                echo json_encode(["status" => "error", "message" => "mode must be trunk or access!!👾👾"]);
                exit();
            }
            if ($op['mode'] === 'trunk') {
                if (empty($op['vlans']) || !is_array($op['vlans'])) {
                    echo json_encode(["status" => "error", "message" => "vlans[] required for trunk!!👾👾"]);
                    exit();
                }
                $vlanAction = $op['vlan_action'] ?? 'replace';
                if (!in_array($vlanAction, ['add','except','replace'], true)) {
                    echo json_encode(["status" => "error", "message" => "vlan_action must be add/except/replace!!👾👾"]);
                    exit();
                }
                if (!empty($op['native_vlan']) &&
                    (!is_numeric($op['native_vlan']) || $op['native_vlan'] < 1 || $op['native_vlan'] > 4094)) {
                    echo json_encode(["status" => "error", "message" => "native_vlan must be 1-4094!!👾👾"]);
                    exit();
                }
            }
            if ($op['mode'] === 'access') {
                if (empty($op['access_vlan']) ||
                    !is_numeric($op['access_vlan']) ||
                    $op['access_vlan'] < 1 || $op['access_vlan'] > 4094) {
                    echo json_encode(["status" => "error", "message" => "access_vlan required and must be 1-4094!!👾👾"]);
                    exit();
                }
            }
        }

        if ($operation === 'membercreation') {
            if (empty($op['portchannel_name'])) {
                echo json_encode(["status" => "error", "message" => "portchannel_name is required!!👾👾"]);
                exit();
            }
            if (!isset($op['mode']) || !in_array($op['mode'], ['active','passive','desirable','auto','on'], true)) {
                echo json_encode(["status" => "error", "message" => "mode must be active/passive/desirable/auto/on!!👾👾"]);
                exit();
            }
        }

        if ($operation === 'l3portchannel') {
            if (empty($op['portchannel_name'])) {
                echo json_encode(["status" => "error", "message" => "portchannel_name is required!!👾👾"]);
                exit();
            }
            if (empty($op['primary_ip']) || empty($op['primary_mask'])) {
                echo json_encode(["status" => "error", "message" => "primary_ip and primary_mask are required!!👾👾"]);
                exit();
            }
            if (!empty($op['secondary_ip']) && empty($op['secondary_mask'])) {
                echo json_encode(["status" => "error", "message" => "secondary_mask required with secondary_ip!!👾👾"]);
                exit();
            }
        }

        if ($operation === 'l3subinterfaces') {
            if (empty($op['portchannel_name'])) {
                echo json_encode(["status" => "error", "message" => "portchannel_name is required!!👾👾"]);
                exit();
            }
            if (empty($op['subinterfaces']) || !is_array($op['subinterfaces'])) {
                echo json_encode(["status" => "error", "message" => "subinterfaces[] required!!👾👾"]);
                exit();
            }
            foreach ($op['subinterfaces'] as $i => $si) {
                if (empty($si['vlan']) || !is_numeric($si['vlan']) ||
                    $si['vlan'] < 1 || $si['vlan'] > 4094) {
                    echo json_encode(["status" => "error", "message" => "subinterfaces[$i].vlan must be 1-4094!!👾👾"]);
                    exit();
                }
                if (empty($si['ip']) || empty($si['netmask'])) {
                    echo json_encode(["status" => "error", "message" => "subinterfaces[$i] needs ip and netmask!!👾👾"]);
                    exit();
                }
            }
        }

        if ($operation === 'portabolish') {
            if (empty($op['portchannel_name'])) {
                echo json_encode(["status" => "error", "message" => "portchannel_name is required for abolish!!👾👾"]);
                exit();
            }
        }

        /* ---------- 4. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare("SELECT username, password_cipher FROM credentials_profiles WHERE cred_id = :id LIMIT 1");
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error", "message" => "cred_id $credId not found 👾👾"]);
            exit();
        }

        /* ---------- 5. VALIDATE EVERY DEVICE ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );

        $intStmt = $pdo->prepare(
            "SELECT int_id, int_name
             FROM interfaces
             WHERE device_id = :dev AND int_id = :int
               AND int_type = 'physical'
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

            $mgmtIp = $devRow['management_ip'];
            if (empty($mgmtIp)) {
                $errors[] = "device $devId: no management_ip (required!!👾👾)";
                continue;
            }

            $entry = [
                'id'            => $devId,
                'management_ip' => $mgmtIp,
                'platform'      => $devRow['platform'],
                'version'       => $devRow['ver'],
                'family'        => $devRow['family'],
            ];

            if ($operation === 'membercreation') {
                if (empty($device['interfaces']) || !is_array($device['interfaces'])) {
                    $errors[] = "device $devId: interfaces[] required for membercreation👾👾";
                    continue;
                }

                $members = [];
                foreach ($device['interfaces'] as $j => $iface) {
                    $intId = $iface['int_id'] ?? null;
                    if (empty($intId)) {
                        $errors[] = "device $devId: interfaces[$j] missing int_id👾👾";
                        continue;
                    }

                    $intStmt->execute([':dev' => $devId, ':int' => (int)$intId]);
                    $intRow = $intStmt->fetch(PDO::FETCH_ASSOC);

                    if (!$intRow) {
                        $errors[] = "device $devId: int_id $intId not found as physical interface👾👾";
                        continue;
                    }

                    $members[] = [
                        'int_id'   => (int)$intRow['int_id'],
                        'int_name' => $intRow['int_name']
                    ];
                }

                if (empty($members)) {
                    $errors[] = "device $devId: no valid members selected👾👾";
                    continue;
                }

                $entry['interfaces'] = $members;
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

        /* ---------- 6. CREATE JOB ---------- */
        $jobId = bin2hex(random_bytes(16));

        $jobPayload = [
            'operation' => $operation,
            'details'   => $op,
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

        /* ---------- 7. NOTIFY FASTAPI ---------- */
        $remotePayload = [
            'action'    => 'configure',
            'job_id'    => $jobId,
            'profile'   => $profile,
            'operation' => $operation,
            'details'   => $op,
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
       GET — polling (?job=<id>) or list port-channels
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
                    $chk = $pdo->prepare("SELECT result FROM jobs WHERE job_id = :id FOR UPDATE");
                    $chk->execute([':id' => $_GET['job']]);
                    $cur = $chk->fetchColumn();

                    if ($cur === 'written') {
                        $pdo->commit();
                        echo json_encode(["status" => "success", "job_id" => $_GET['job']]);
                        exit();
                    }

                    /* ==============================================
                       Prepared statements shared across branches
                       ============================================== */

                    // ---- port_channels ----
                    $pcUpsert = $pdo->prepare(
                        "INSERT INTO port_channels
                             (device_id, po_number, mode, description, vlan_ids, native_vlan, min_links, updated_at)
                         VALUES (:id, :po, :mode, :desc, :vlans, :native, :min_links, NOW())
                         ON DUPLICATE KEY UPDATE
                             mode        = VALUES(mode),
                             description = VALUES(description),
                             vlan_ids    = VALUES(vlan_ids),
                             native_vlan = VALUES(native_vlan),
                             min_links   = VALUES(min_links),
                             updated_at  = NOW()"
                    );

                    // ---- port_channel_members ----
                    $memUpsert = $pdo->prepare(
                        "INSERT INTO port_channel_members
                             (device_id, po_number, int_id, int_name, channel_mode, updated_at)
                         VALUES (:id, :po, :int_id, :int_name, :mode, NOW())
                         ON DUPLICATE KEY UPDATE
                             po_number    = VALUES(po_number),
                             int_name     = VALUES(int_name),
                             channel_mode = VALUES(channel_mode),
                             updated_at   = NOW()"
                    );

                    // ---- l3_port_channels ----
                    $l3Upsert = $pdo->prepare(
                        "INSERT INTO l3_port_channels
                             (device_id, po_number, primary_ip, primary_mask,
                              secondary_ip, secondary_mask, updated_at)
                         VALUES (:id, :po, :pip, :pmask, :sip, :smask, NOW())
                         ON DUPLICATE KEY UPDATE
                             primary_ip     = VALUES(primary_ip),
                             primary_mask   = VALUES(primary_mask),
                             secondary_ip   = VALUES(secondary_ip),
                             secondary_mask = VALUES(secondary_mask),
                             updated_at     = NOW()"
                    );

                    // ---- l3_pc_subinterfaces ----
                    $subUpsert = $pdo->prepare(
                        "INSERT INTO l3_pc_subinterfaces
                             (device_id, po_number, vlan_id, ip, netmask, updated_at)
                         VALUES (:id, :po, :vlan, :ip, :mask, NOW())
                         ON DUPLICATE KEY UPDATE
                             ip         = VALUES(ip),
                             netmask    = VALUES(netmask),
                             updated_at = NOW()"
                    );

                    // ---- interfaces: upsert for parent PO ----
                    $ifUpsert = $pdo->prepare(
                        "INSERT INTO interfaces
                             (device_id, int_name, int_type, link_type,
                              description, ip, netmask)
                         VALUES (:dev, :name, :itype, :ltype, :desc, :ip, :mask)
                         ON DUPLICATE KEY UPDATE
                             int_type    = VALUES(int_type),
                             link_type   = VALUES(link_type),
                             description = VALUES(description),
                             ip          = VALUES(ip),
                             netmask     = VALUES(netmask)"
                    );

                    // ---- interfaces: upsert for subinterface (with parent id) ----
                    $ifSubUpsert = $pdo->prepare(
                        "INSERT INTO interfaces
                             (device_id, int_name, int_type, link_type,
                              parent_interface_id, description, ip, netmask)
                         VALUES (:dev, :name, :itype, :ltype, :pid, :desc, :ip, :mask)
                         ON DUPLICATE KEY UPDATE
                             int_type            = VALUES(int_type),
                             link_type           = VALUES(link_type),
                             parent_interface_id = VALUES(parent_interface_id),
                             ip                  = VALUES(ip),
                             netmask             = VALUES(netmask)"
                    );

                    // ---- lookup parent int_id ----
                    $ifParentId = $pdo->prepare(
                        "SELECT int_id FROM interfaces
                         WHERE device_id = :dev AND int_name = :name LIMIT 1"
                    );

                    /* ---------- 6.1  portcreation ---------- */
                    if ($operation === 'portcreation') {

                        $vlanStr = '';
                        if ($details['mode'] === 'trunk' && !empty($details['vlans'])) {
                            $vlanStr = implode(',', array_map(
                                fn($v) => (string)($v['id'] ?? ''),
                                $details['vlans']
                            ));
                        }

                        foreach ($devices as $device) {
                            $pcUpsert->execute([
                                ':id'        => $device['id'],
                                ':po'        => $details['portchannel_name'],
                                ':mode'      => $details['mode'],
                                ':desc'      => $details['description'] ?? '',
                                ':vlans'     => $vlanStr,
                                ':native'    => $details['native_vlan'] ?? null,
                                ':min_links' => $details['min_links'] ?? null
                            ]);

                            // Interfaces row — L2 port-channel
                            $ifUpsert->execute([
                                ':dev'   => $device['id'],
                                ':name'  => 'Port-channel' . $details['portchannel_name'],
                                ':itype' => 'port-channel',
                                ':ltype' => 'port-channel',
                                ':desc'  => substr((string)($details['description'] ?? ''), 0, 50),
                                ':ip'    => null,
                                ':mask'  => null
                            ]);
                        }
                    }

                    /* ---------- 6.2  membercreation ---------- */
                    if ($operation === 'membercreation') {
                        foreach ($devices as $device) {
                            foreach ($device['interfaces'] as $m) {
                                $memUpsert->execute([
                                    ':id'       => $device['id'],
                                    ':po'       => $details['portchannel_name'],
                                    ':int_id'   => $m['int_id'],
                                    ':int_name' => $m['int_name'],
                                    ':mode'     => $details['mode']
                                ]);
                            }
                        }
                    }

                    /* ---------- 6.3  l3portchannel ---------- */
                    if ($operation === 'l3portchannel') {
                        foreach ($devices as $device) {
                            $l3Upsert->execute([
                                ':id'    => $device['id'],
                                ':po'    => $details['portchannel_name'],
                                ':pip'   => $details['primary_ip'],
                                ':pmask' => $details['primary_mask'],
                                ':sip'   => $details['secondary_ip'] ?? null,
                                ':smask' => $details['secondary_mask'] ?? null
                            ]);

                            // Interfaces row — L3 routed port-channel
                            $ifUpsert->execute([
                                ':dev'   => $device['id'],
                                ':name'  => 'Port-channel' . $details['portchannel_name'],
                                ':itype' => 'port-channel',
                                ':ltype' => 'routed',
                                ':desc'  => substr((string)($details['description'] ?? ''), 0, 50),
                                ':ip'    => $details['primary_ip'],
                                ':mask'  => $details['primary_mask']
                            ]);
                        }
                    }

                    /* ---------- 6.4  l3subinterfaces ---------- */
                    if ($operation === 'l3subinterfaces') {
                        foreach ($devices as $device) {

                            // Resolve parent PO int_id (must exist — subif requires parent)
                            $ifParentId->execute([
                                ':dev'  => $device['id'],
                                ':name' => 'Port-channel' . $details['portchannel_name']
                            ]);
                            $parentIntId = $ifParentId->fetchColumn();
                            if ($parentIntId === false) {
                                $parentIntId = null; // leave orphan if parent absent
                            }

                            foreach ($details['subinterfaces'] as $si) {
                                $subUpsert->execute([
                                    ':id'   => $device['id'],
                                    ':po'   => $details['portchannel_name'],
                                    ':vlan' => (int)$si['vlan'],
                                    ':ip'   => $si['ip'],
                                    ':mask' => $si['netmask']
                                ]);

                                $ifSubUpsert->execute([
                                    ':dev'   => $device['id'],
                                    ':name'  => 'Port-channel' . $details['portchannel_name'] . '.' . (int)$si['vlan'],
                                    ':itype' => 'subinterface',
                                    ':ltype' => 'routed',
                                    ':pid'   => $parentIntId,
                                    ':desc'  => '',
                                    ':ip'    => $si['ip'],
                                    ':mask'  => $si['netmask']
                                ]);
                            }
                        }
                    }

                    /* ---------- 6.5  portabolish ---------- */
                    if ($operation === 'portabolish') {

                        $po    = $details['portchannel_name'];
                        $poLbl = 'Port-channel' . $po;

                        // Delete interfaces: parent + all subinterfaces (dotted)
                        $delIf = $pdo->prepare(
                            "DELETE FROM interfaces
                             WHERE device_id = :id
                               AND (int_name = :parent
                                    OR int_name LIKE :subpattern)"
                        );

                        $delPc  = $pdo->prepare(
                            "DELETE FROM port_channels WHERE device_id=:id AND po_number=:po"
                        );
                        $delMem = $pdo->prepare(
                            "DELETE FROM port_channel_members WHERE device_id=:id AND po_number=:po"
                        );
                        $delL3  = $pdo->prepare(
                            "DELETE FROM l3_port_channels WHERE device_id=:id AND po_number=:po"
                        );
                        $delSub = $pdo->prepare(
                            "DELETE FROM l3_pc_subinterfaces WHERE device_id=:id AND po_number=:po"
                        );

                        foreach ($devices as $device) {
                            $delIf->execute([
                                ':id'         => $device['id'],
                                ':parent'     => $poLbl,
                                ':subpattern' => $poLbl . '.%'
                            ]);
                            $delPc->execute ([':id' => $device['id'], ':po' => $po]);
                            $delMem->execute([':id' => $device['id'], ':po' => $po]);
                            $delL3->execute ([':id' => $device['id'], ':po' => $po]);
                            $delSub->execute([':id' => $device['id'], ':po' => $po]);
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
                    pc.id           AS row_pk,
                    pc.device_id,
                    pc.po_number,
                    pc.mode,
                    pc.description,
                    pc.vlan_ids,
                    pc.native_vlan,
                    pc.min_links,
                    pc.updated_at,
                    d.hostname
                FROM port_channels pc
                LEFT JOIN devices d ON d.device_id = pc.device_id
                ORDER BY pc.device_id, pc.po_number";

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
                    'port_channels' => []
                ];
            }
            $grouped[$id]['port_channels'][] = [
                'row_pk'      => (int)$row['row_pk'],
                'po_number'   => (int)$row['po_number'],
                'mode'        => $row['mode'],
                'description' => $row['description'],
                'vlan_ids'    => $row['vlan_ids'],
                'native_vlan' => $row['native_vlan'],
                'min_links'   => $row['min_links'],
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