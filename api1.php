<?php
header("Content-Type: application/json");

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
        if (empty($devicedata['prof_name']) || empty($devicedata['username']) || empty($devicedata['password'])) {
            echo json_encode([
                "status" => "error",
                "message" => "invalid credentials, all fields must exists!!!👾👾"
            ]);
            exit();
        }

        $sql = "insert into credentials_profiles (profile_name, username, password_cipher) values (:prof, :user, :pass)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':prof' => htmlspecialchars($devicedata['prof_name']),
            ':user' => htmlspecialchars($devicedata['username']),
            ':pass' => htmlspecialchars($devicedata['password'])
        ]);
        echo json_encode(["status" => "success"]);
        exit();
    }

    if ($method === "GET") {
        $sql = "select cred_id as profile_id, profile_name, username from credentials_profiles";
        $stmt = $pdo->query($sql);
        $profs = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode([
            "status" => "success",
            "profiles" => $profs
        ]);
        exit();
    }

    if ($method === "DELETE") {
        if (empty($devicedata['id'])) {
            echo json_encode(["status" => "error", "message" => "missing id"]);
            exit();
        }

        $sql = "delete from credentials_profiles where cred_id = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':id' => $devicedata['id']]);
        echo json_encode(["status" => "success"]);
        exit();
    }

} catch (PDOException $e) {
    echo json_encode([
        "status" => "error",
        "message" => "database failure!!👾👾 : $e.message"
    ]);
}

?>