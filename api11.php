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

