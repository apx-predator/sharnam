<?php
header("Content-Type: application/json");

$fastapi_url = "http://127.0.0.1:8000/configure";

$payload = [
    "action"  => "configure",
    "job_id"  => "debug-".bin2hex(random_bytes(4)),
    "profile" => ["username" => "test", "password" => "test"],
    "devices" => [[
        "id"            => 1,
        "mode"          => "svi",
        "management_ip" => "10.0.0.1",
        "platform"      => "cisco_iosxe",
        "version"       => "17.9",
        "family"        => "9200",
        "interfaces"    => [["name" => "vlan10", "desc" => "10.1.1.1/24"]]
    ]],
    "async" => true
];

$json_payload = json_encode($payload);

$ch = curl_init($fastapi_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $json_payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "Content-Length: " . strlen($json_payload)
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);

$response = curl_exec($ch);
$curlErr  = curl_error($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$errno    = curl_errno($ch);
curl_close($ch);

echo json_encode([
    "sent_payload" => $payload,
    "sent_json"    => $json_payload,
    "curl_errno"   => $errno,
    "curl_error"   => $curlErr,
    "http_code"    => $httpCode,
    "raw_response" => $response,
    "response_parsed" => json_decode($response, true)
], JSON_PRETTY_PRINT);