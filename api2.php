<?php
header("Content-Type: application/json");

ini_set('display_errors', '0');
error_reporting(0);

$method = $_SERVER['REQUEST_METHOD'];
$rawpayload = file_get_contents("php://input");
$devicedata = json_decode($rawpayload, true);

$host = "localhost";
$dbname = "sharnam_db";
$username = "root";
$password = "";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($method === "POST") {
        if (empty($devicedata['type']) || empty($devicedata['platform']) || empty($devicedata['site_id']) || empty($devicedata['hostname']) || empty($devicedata['management_ip'])) {
            echo json_encode([
                "status" => "error",
                "message" => "invalid device, all fields must exist!!!👾👾"
            ]);
            exit();
        }

        $sql = "insert into devices (device_type, device_role, platform, hostname, management_ip, site_id, cred_id) values (:type, :role, :plat, :host, :mgmt, :site, :cred)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':type' => $devicedata['type'],
            ':role' => isset($devicedata['role']) ? $devicedata['role'] : null,
            ':plat' => $devicedata['platform'],
            ':host' => $devicedata['hostname'],
            ':mgmt' => $devicedata['management_ip'],
            ':site' => $devicedata['site_id'],
            ':cred' => isset($devicedata['cred_id']) ? $devicedata['cred_id'] : null
        ]);
        echo json_encode(["status" => "success"]);
        exit();
    }

    if ($method === "GET") {
        $sql = "select device_id, device_type, device_role, platform, hostname, management_ip, site_id, cred_id from devices";
        $stmt = $pdo->query($sql);
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode([
            "status" => "success",
            "devices" => $rows
        ]);
        exit();
    }

    if ($method === "DELETE") {
        if (empty($devicedata['id'])) {
            echo json_encode(["status" => "error", "message" => "missing id"]);
            exit();
        }

        $sql = "delete from devices where device_id = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':id' => $devicedata['id']]);
        echo json_encode(["status" => "success"]);
        exit();
    }

} catch (PDOException $e) {
    echo json_encode([
        "status" => "error",
        "message" => "database failure!!👾👾 : " . $e->getMessage()
    ]);
}

?>