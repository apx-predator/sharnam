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
        if (empty($devicedata['site_name'])) {
            echo json_encode([
                "status" => "error",
                "message" => "site_name is required!!!👾👾"
            ]);
            exit();
        }

        $sql = "insert into sites (site_name) values (:name)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':name' => $devicedata['site_name']
        ]);
        echo json_encode(["status" => "success"]);
        exit();
    }

    if ($method === "GET") {
        $sql = "select site_id, site_name from sites";
        $stmt = $pdo->query($sql);
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode([
            "status" => "success",
            "sites" => $rows
        ]);
        exit();
    }

    if ($method === "DELETE") {
        if (empty($devicedata['id'])) {
            echo json_encode(["status" => "error", "message" => "missing id"]);
            exit();
        }

        $sql = "delete from sites where site_id = :id";
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