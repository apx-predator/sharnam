<?php
header("Content-Type: application/json");

$method     = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host        = "localhost";
$dbname      = "sharnam_db";
$username    = "root";
$password    = "";
$fastapi_url = "http://127.0.0.1:8000/add_interface_features";

// Must be <= Nornir's num_workers in add_interface_features.py (currently 15).
$BATCH_SIZE = 15;

// Interface-scoped vs native-scoped classification.
$NATIVE_SCOPED = [
    'vlan_create', 'vlan_delete', 'vlan_name', 'vlan_state',
    'vlan_remote_span', 'vlan_uni',
    'pvlan_global', 'pvlan_secondary', 'svi_private_vlan_mapping',
];

function versionToTrain($ver) {
    if (empty($ver)) return "1715";
    if (!preg_match('/^(\d+)\.(\d+)/', $ver, $m)) return "1715";
    $major = (int)$m[1]; $minor = (int)$m[2];
    if ($major === 16) return "1612";
    if ($major === 17) {
        if ($minor <= 4)  return "173";
        if ($minor <= 7)  return "179";
        if ($minor <= 13) return "1712";
        return "1715";
    }
    return "1715";
}

function splitInterfaceName($intName) {
    if (preg_match('/^([A-Za-z][A-Za-z\-]+)(\d+[\/\.\d]*)$/', $intName, $m)) {
        return ["parent" => $m[1], "name" => $m[2]];
    }
    return null;
}

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($method === "POST") {

        /* ---------- 1. GLOBAL VALIDATION ---------- */
        if (empty($devicedata['cred_id'])
            || empty($devicedata['operation'])
            || empty($devicedata['devices'])
            || !is_array($devicedata['devices'])) {
            echo json_encode(["status" => "error",
                "message" => "cred_id, operation, devices[] required"]);
            exit();
        }

        $credId    = $devicedata['cred_id'];
        $operation = $devicedata['operation'];
        $devices   = $devicedata['devices'];

        if (!in_array($operation, ['feature_add', 'feature_remove'], true)) {
            echo json_encode(["status" => "error",
                "message" => "operation must be feature_add or feature_remove"]);
            exit();
        }

        /* ---------- 2. LOAD PROFILE ---------- */
        $stmt = $pdo->prepare(
            "SELECT username, password_cipher FROM credentials_profiles
             WHERE cred_id = :id LIMIT 1"
        );
        $stmt->execute([':id' => $credId]);
        $profile = $stmt->fetch(PDO::FETCH_ASSOC);
        if (!$profile) {
            echo json_encode(["status" => "error",
                "message" => "cred_id $credId not found"]);
            exit();
        }

        /* ---------- 3. PER-DEVICE PREPARE ---------- */
        $devStmt = $pdo->prepare(
            "SELECT device_id, management_ip, platform, ver, family
             FROM devices WHERE device_id = :id LIMIT 1"
        );
        $intStmt = $pdo->prepare(
            "SELECT int_id, int_name FROM interfaces
             WHERE device_id = :dev AND int_id = :int LIMIT 1"
        );

        $prepared = [];
        $errors   = [];

        foreach ($devices as $i => $d) {
            $devId = $d['id'] ?? null;
            if (empty($devId)) {
                $errors[] = ["device_id" => null, "error" => "devices[$i]: missing id"];
                continue;
            }

            $devStmt->execute([':id' => $devId]);
            $devRow = $devStmt->fetch(PDO::FETCH_ASSOC);
            if (!$devRow) {
                $errors[] = ["device_id" => $devId, "error" => "device not found"];
                continue;
            }
            if (empty($devRow['management_ip'])) {
                $errors[] = ["device_id" => $devId, "error" => "no management_ip"];
                continue;
            }

            $train = versionToTrain($devRow['ver']);

            $nativeFeatures = [];
            $badNative = false;
            foreach (($d['native_features'] ?? []) as $nf) {
                if (empty($nf['feature']) || !is_string($nf['feature'])) {
                    $errors[] = ["device_id" => $devId,
                                 "error" => "native_features[] entry missing 'feature'"];
                    $badNative = true; break;
                }
                $nativeFeatures[] = $nf;
            }
            if ($badNative) continue;

            $ifaceEntries = $d['interfaces'] ?? [];
            $resolvedInterfaces = [];
            $ifaceFailed = false;
            foreach ($ifaceEntries as $j => $ie) {
                $intId = $ie['int_id'] ?? null;
                $feats = $ie['features'] ?? [];

                if (empty($intId)) {
                    $errors[] = ["device_id" => $devId,
                                 "error" => "interfaces[$j]: int_id required"];
                    $ifaceFailed = true; break;
                }
                if (empty($feats) || !is_array($feats)) {
                    $errors[] = ["device_id" => $devId,
                                 "error" => "interfaces[$j]: features[] required"];
                    $ifaceFailed = true; break;
                }

                $intStmt->execute([':dev' => $devId, ':int' => (int)$intId]);
                $intRow = $intStmt->fetch(PDO::FETCH_ASSOC);
                if (!$intRow) {
                    $errors[] = ["device_id" => $devId,
                                 "error" => "interfaces[$j]: int_id $intId not found"];
                    $ifaceFailed = true; break;
                }
                $split = splitInterfaceName($intRow['int_name']);
                if ($split === null) {
                    $errors[] = ["device_id" => $devId,
                                 "error" => "cannot parse interface name '{$intRow['int_name']}'"];
                    $ifaceFailed = true; break;
                }

                $ifaceFeats = [];
                foreach ($feats as $f) {
                    if (empty($f['feature']) || !is_string($f['feature'])) {
                        $errors[] = ["device_id" => $devId,
                                     "error" => "interfaces[$j].features[] entry missing 'feature'"];
                        $ifaceFailed = true; break 2;
                    }
                    if (in_array($f['feature'], $NATIVE_SCOPED, true)) {
                        $nativeFeatures[] = $f;
                    } else {
                        $ifaceFeats[] = $f;
                    }
                }

                $resolvedInterfaces[] = [
                    'interface' => [
                        'parent' => $split['parent'],
                        'name'   => $split['name'],
                    ],
                    'features' => $ifaceFeats,
                ];
            }
            if ($ifaceFailed) continue;

            if (empty($resolvedInterfaces) && empty($nativeFeatures)) {
                $errors[] = ["device_id" => $devId,
                             "error" => "no interface or native features supplied"];
                continue;
            }

            $prepared[] = [
                'job_id'          => bin2hex(random_bytes(16)),
                'device'          => [
                    'id'            => $devId,
                    'management_ip' => $devRow['management_ip'],
                    'platform'      => $devRow['platform'],
                    'version'       => $devRow['ver'],
                    'family'        => $devRow['family'],
                    'interfaces'    => [],
                ],
                'train'           => $train,
                'interfaces'      => $resolvedInterfaces,
                'native_features' => $nativeFeatures,
                'operation'       => $operation,
            ];
        }

        if (empty($prepared)) {
            echo json_encode([
                "status"  => "error",
                "message" => "no device could be prepared",
                "errors"  => $errors,
            ]);
            exit();
        }

        /* ---------- 4. INSERT JOBS + DISPATCH IN BATCHES ---------- */
        $insertJob = $pdo->prepare(
            "INSERT INTO jobs (job_id, status, payload)
             VALUES (:id, 'pending', :p)"
        );
        $failJob = $pdo->prepare(
            "UPDATE jobs SET status='failed', result=:r
             WHERE job_id=:id AND status='pending'"
        );

        $allJobs    = [];
        $dispatched = 0;

        foreach (array_chunk($prepared, $BATCH_SIZE) as $batchIndex => $batch) {

            $mh      = curl_multi_init();
            $handles = [];

            foreach ($batch as $p) {
                $jobId = $p['job_id'];
                $devId = $p['device']['id'];

                $insertJob->execute([
                    ':id' => $jobId,
                    ':p'  => json_encode([
                        'operation'       => $p['operation'],
                        'train'           => $p['train'],
                        'device_id'       => $devId,
                        'interfaces'      => $p['interfaces'],
                        'native_features' => $p['native_features'],
                    ]),
                ]);

                $remotePayload = [
                    'action'    => 'configure',
                    'job_id'    => $jobId,
                    'profile'   => $profile,
                    'operation' => $p['operation'],
                    'details'   => [
                        'change' => [
                            'train'           => $p['train'],
                            'interfaces'      => $p['interfaces'],
                            'native_features' => $p['native_features'],
                        ],
                    ],
                    'devices'   => [$p['device']],
                    'async'     => true,
                ];

                $json = json_encode($remotePayload);

                $ch = curl_init($fastapi_url);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
                curl_setopt($ch, CURLOPT_HTTPHEADER, [
                    'Content-Type: application/json',
                    'Content-Length: ' . strlen($json),
                ]);
                curl_setopt($ch, CURLOPT_TIMEOUT, 10);

                curl_multi_add_handle($mh, $ch);

                $handles[(int)$ch] = [
                    'handle'    => $ch,
                    'prepared'  => $p,
                    'device_id' => $devId,
                    'job_id'    => $jobId,
                    'json_len'  => strlen($json),
                ];
            }

            $running = null;
            do {
                $mrc = curl_multi_exec($mh, $running);
            } while ($mrc === CURLM_CALL_MULTI_PERFORM);

            while ($running && $mrc === CURLM_OK) {
                if (curl_multi_select($mh, 1.0) === -1) {
                    usleep(100000);
                }
                do {
                    $mrc = curl_multi_exec($mh, $running);
                } while ($mrc === CURLM_CALL_MULTI_PERFORM);
            }

            foreach ($handles as $key => $h) {
                $ch       = $h['handle'];
                $p        = $h['prepared'];
                $devId    = $h['device_id'];
                $jobId    = $h['job_id'];
                $response = curl_multi_getcontent($ch);
                $curlErr  = curl_error($ch);
                $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

                curl_multi_remove_handle($mh, $ch);
                curl_close($ch);

                error_log(sprintf(
                    "IF-FEATURES DISPATCH [batch %d] [%s] HTTP %d, %d bytes, err=%s",
                    $batchIndex + 1, $devId, $httpCode, $h['json_len'],
                    $curlErr ?: "-"
                ));

                if ($curlErr !== '' || $httpCode < 200 || $httpCode >= 300) {
                    error_log("IF-FEATURES FASTAPI ERROR [$devId]: " . $response);
                    $failJob->execute([
                        ':r'  => "dispatch failed: " . ($curlErr ?: "HTTP $httpCode"),
                        ':id' => $jobId,
                    ]);
                    $allJobs[] = [
                        "device_id" => $devId,
                        "job_id"    => $jobId,
                        "status"    => "failed",
                        "error"     => "dispatch failed: " . ($curlErr ?: "HTTP $httpCode"),
                    ];
                } else {
                    $dispatched++;
                    $allJobs[] = [
                        "device_id" => $devId,
                        "job_id"    => $jobId,
                        "status"    => "accepted",
                    ];
                }
            }

            curl_multi_close($mh);
        }

        /* ---------- 5. RESPONSE ---------- */
        $response = [
            "status"       => $dispatched > 0 ? "accepted" : "error",
            "dispatched"   => $dispatched,
            "total"        => count($prepared),
            "batch_size"   => $BATCH_SIZE,
            "batches"      => (int)ceil(count($prepared) / $BATCH_SIZE),
            "jobs"         => $allJobs,
        ];
        if (!empty($errors)) {
            $response["skipped"] = $errors;
        }
        echo json_encode($response);
        exit();
    }

    /* ---------- GET ---------- */
    if ($method === "GET") {

        /* ---------- RECENT JOBS (for left panel) ---------- */
        if (!empty($_GET['recent'])) {
            $limit = max(1, min(50, (int)$_GET['recent']));

            // Filter to feature jobs only. Stacking jobs use operation
            // front-panel / back-panel / dad — we want feature_add/feature_remove.
            $stmt = $pdo->prepare(
                "SELECT job_id, status, result, payload, created_at, updated_at
                 FROM jobs
                 WHERE payload LIKE '%\"operation\":\"feature_%'
                 ORDER BY updated_at DESC LIMIT :lim"
            );
            $stmt->bindValue(':lim', $limit, PDO::PARAM_INT);
            $stmt->execute();
            $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

            $jobs = [];
            foreach ($rows as $r) {
                $p = json_decode($r['payload'] ?? '{}', true);
                $jobs[] = [
                    'job_id'     => $r['job_id'],
                    'status'     => $r['status'],
                    'result'     => $r['result'],
                    'device_id'  => $p['device_id']  ?? null,
                    'operation'  => $p['operation']  ?? null,
                    'train'      => $p['train']      ?? null,
                    'created_at' => $r['created_at'] ?? null,
                ];
            }
            echo json_encode(['status' => 'success', 'jobs' => $jobs]);
            exit();
        }

        /* ---------- SINGLE JOB POLLING ---------- */
        if (empty($_GET['job'])) {
            echo json_encode(["status" => "error",
                "message" => "job or recent parameter required"]);
            exit();
        }

        $stmt = $pdo->prepare(
            "SELECT status, result, payload FROM jobs WHERE job_id = :id"
        );
        $stmt->execute([':id' => $_GET['job']]);
        $job = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$job) {
            echo json_encode(["status" => "error", "message" => "unknown job"]);
            exit();
        }

        $payload = json_decode($job['payload'] ?? '{}', true);

        $out = [
            "job_id"    => $_GET['job'],
            "status"    => $job['status'],
            "device_id" => $payload['device_id'] ?? null,
        ];

        if ($job['status'] === 'pending' || $job['status'] === 'running') {
            $out["status"] = "pending";
        } elseif ($job['status'] === 'failed') {
            $out["status"]  = "error";
            $out["message"] = $job['result'] ?: "job failed";
        } else {
            $out["status"] = "success";
        }

        echo json_encode($out);
        exit();
    }

} catch (PDOException $e) {
    echo json_encode([
        "status"  => "error",
        "message" => "database failure: " . $e->getMessage(),
    ]);
    exit();
}