<?php
header("Content-Type: application/json");

ini_set('display_errors', '0');
error_reporting(0);

$method = $_SERVER['REQUEST_METHOD'];

$host     = "localhost";
$dbname   = "sharnam_db";
$username = "root";
$password = "";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($method === "GET") {
        $site     = isset($_GET['site'])     ? $_GET['site']     : "";
        $type     = isset($_GET['type'])     ? $_GET['type']     : "";
        $role     = isset($_GET['role'])     ? $_GET['role']     : "";
        $platform = isset($_GET['platform']) ? $_GET['platform'] : "";
        $hostname = isset($_GET['hostname']) ? $_GET['hostname'] : "";

        // Base query — always filter by site (required)
        $sql = "SELECT device_id, hostname, device_type FROM devices WHERE site_id = :site";
        $params = [':site' => $site];

        if ($type !== "")     { $sql .= " AND device_type = :type";  $params[':type'] = $type; }
        if ($role !== "")     { $sql .= " AND device_role = :role";  $params[':role'] = $role; }
        if ($platform !== "") { $sql .= " AND platform    = :plat";  $params[':plat'] = $platform; }
        if ($hostname !== "") { $sql .= " AND hostname    = :host";  $params[':host'] = $hostname; }

        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Fetch interfaces per device
        $ifStmt = $pdo->prepare("SELECT int_id, int_name FROM interfaces WHERE device_id = :did");

        $devices = [];
        foreach ($rows as $row) {
            $ifParams = [':did' => $row['device_id']];
            $ifStmt->execute($ifParams);
            $ifaces = $ifStmt->fetchAll(PDO::FETCH_ASSOC);

            $intfs = array_map(function ($i) {
                return [
                    'id'   => $i['int_id'],
                    'name' => $i['int_name']
                ];
            }, $ifaces);

            $devices[] = [
                'id'         => $row['device_id'],
                'name'       => $row['hostname'],
                'type'       => $row['device_type'],
                'interfaces' => $intfs
            ];
        }

        echo json_encode([
            "status"  => "success",
            "message" => $devices
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

?>