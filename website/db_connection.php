<?php
$host = "localhost"; // e.g., "localhost" or "127.0.0.1"
$username = "root";
$password = "";
$database = "iot";


$conn = new mysqli($host, $username, $password, $database);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


?>
