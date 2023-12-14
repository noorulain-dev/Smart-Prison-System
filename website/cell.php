<?php
// cell.php

// Include the database connection file
include('db_connection.php');
include 'header.php';

// Get the cellNumber from the URL
$cellNumber = $_GET['cellNumber'];

// Fetch cell details from the database using cellNo
$sqlCell = "SELECT * FROM cell WHERE cellNo = '$cellNumber'";
$resultCell = $conn->query($sqlCell);

if ($resultCell->num_rows > 0) {
    // Cell details found, display them
    $cellDetails = $resultCell->fetch_assoc();
    echo "<h2>Cell Details</h2>";
    echo "<p>Cell Number: " . $cellDetails['cellNo'] . "</p>";

    // Fetch environmental data for the specific cell from the env table using cellID
    $sqlEnv = "SELECT * FROM env WHERE cellID = '" . $cellDetails['cellID'] . "'";
    $resultEnv = $conn->query($sqlEnv);

    if ($resultEnv->num_rows > 0) {
        // Display environmental data
        echo "<h2>Environmental Data</h2>";
        echo "<table border='1'>";
        echo "<tr><th>Environment Time</th><th>Temperature</th><th>Humidity</th><th>Noise</th></tr>";

        while ($rowEnv = $resultEnv->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $rowEnv['envTime'] . "</td>";
            echo "<td>" . $rowEnv['temp'] . "</td>";
            echo "<td>" . $rowEnv['humid'] . "</td>";
            echo "<td>" . $rowEnv['noise'] . "</td>";
            echo "</tr>";
        }

        echo "</table>";
    } else {
        echo "<p>No environmental data found for this cell.</p>";
    }
} else {
    // Cell not found
    echo "<p>Cell not found.</p>";
}

// Close the database connection
$conn->close();
?>
