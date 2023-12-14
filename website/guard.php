<?php
// guard.php

// Include the database connection file
include('db_connection.php');
include 'header.php';


// Get the guardID from the URL
$guardID = $_GET['guardID'];

// Fetch guard details from the database
$sql = "SELECT * FROM guard WHERE guardID = '$guardID'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Guard details found, display them
    $guardDetails = $result->fetch_assoc();
    echo "<h2>Guard Details</h2>";
    echo "<p>Guard ID: " . $guardDetails['guardID'] . "</p>";
    echo "<p>Guard Name: " . $guardDetails['guardName'] . "</p>";

    // Fetch patrol activities for the specific guard
    $sqlPatrol = "SELECT * FROM patrol WHERE guardID = '$guardID'";
    $resultPatrol = $conn->query($sqlPatrol);

    if ($resultPatrol->num_rows > 0) {
        // Display patrol activities
        echo "<h2>Patrol Activities</h2>";
        echo "<table border='1'>";
        echo "<tr><th>Activity ID</th><th>Cell ID</th><th>Activity Name</th><th>Activity Time</th></tr>";

        while ($rowPatrol = $resultPatrol->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $rowPatrol['activityID'] . "</td>";
            echo "<td>" . $rowPatrol['cellID'] . "</td>";
            echo "<td>" . $rowPatrol['activityName'] . "</td>";
            echo "<td>" . $rowPatrol['activityTime'] . "</td>";
            echo "</tr>";
        }

        echo "</table>";
    } else {
        echo "<p>No patrol activities found for this guard.</p>";
    }
} else {
    // Guard not found
    echo "<p>Guard not found.</p>";
}

// Close the database connection
$conn->close();
?>
