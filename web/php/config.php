<?php
session_start();
header('Content-Type: application/json');

$servername = "localhost";
$username = "admin";
$password = "123";
$dbname = "admin";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    echo json_encode(array('error' => 'Connection failed: ' . $conn->connect_error));
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);

if ($data === null) {
    echo json_encode(array('error' => 'Invalid JSON input'));
    exit;
}

$userId = $conn->real_escape_string($data['userId']);
$userName = $conn->real_escape_string($data['userName']);
$messageContent = $conn->real_escape_string($data['messageContent']);

$sql = "INSERT INTO messages (user_id, user_name, message_content) VALUES ('$userId', '$userName', '$messageContent')";

if ($conn->query($sql) === TRUE) {
    echo json_encode(array('success' => true, 'messageContent' => $messageContent));
} else {
    echo json_encode(array('error' => 'Error: ' . $sql . ' - ' . $conn->error));
}

$conn->close();
?>
