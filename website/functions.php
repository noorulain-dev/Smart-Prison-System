<?php

include 'db_connection.php';

function getRecentCellEntries($conn)
{
    $query = "SELECT cellNo, buzz, openDoor FROM cell ORDER BY cellID DESC LIMIT 5";
    return $conn->query($query);
}

function getRecentGuardEntries($conn)
{
    $query = "SELECT guardID, guardName FROM guard ORDER BY guardID DESC LIMIT 5";
    return $conn->query($query);
}

function getRecentPatrolEntries($conn)
{
    $query = "SELECT cellID, guardID, activityName, activityTime FROM patrol ORDER BY activityID DESC LIMIT 5";
    return $conn->query($query);
}

function getRecentEnvEntries($conn)
{
    $query = "SELECT cellID, temp, humid, noise, envTime FROM env ORDER BY envID DESC LIMIT 5";
    return $conn->query($query);
}

function getAllCellNumbers($conn)
{
    $query = "SELECT cellID, cellNo FROM cell"; // Replace 'your_cell_table' with the actual table name

    // Execute the query
    $result = $conn->query($query);

    // Check for errors
    if (!$result) {
        die("Error fetching cell numbers: " . $conn->error);
    }

    return $result;
}

function buzzAllCells($conn)
{
    // Buzz all cells by setting 'buzz' to 1
    $query = "UPDATE cell SET buzz = 1";
    $conn->query($query);
    header("Location: index.php");
}

function openAllDoors($conn)
{
    // Open all doors by setting 'openDoor' to 1
    $query = "UPDATE cell SET openDoor = 1";
    $conn->query($query);
    header("Location: index.php");
}


function reverseBuzzAllCells($conn)
{
    // Set the 'buzz' value to 0 for all cells
    $query = "UPDATE cell SET buzz = 0";
    $conn->query($query);
    header("Location: index.php");
}

function reverseOpenAllDoors($conn)
{
    // Set the 'openDoor' value to 0 for all cells
    $query = "UPDATE cell SET openDoor = 0";
    $conn->query($query);
    header("Location: index.php");
}

// Function to buzz a specific cell
function buzzCell($conn, $cellID)
{
    // Prepare the statement
    $query = $conn->prepare("UPDATE cell SET buzz = 1 WHERE cellID = ?");
    $query->bind_param("i", $cellID); // Use "i" for integers
    $query->execute();

    // Check for errors
    if ($query->error) {
        die("Error updating cell: " . $query->error);
    }

    // Close the statement
    $query->close();

    // Redirect to dashboard.php
    header("Location: index.php");
}

// Function to open the door of a specific cell
function openDoorCell($conn, $cellID)
{
    $query = $conn->prepare("UPDATE cell SET openDoor = 1 WHERE cellID = ?");
    $query->bind_param("i", $cellID);
    $query->execute();

    if ($query->error) {
        die("Error updating cell door: " . $query->error);
    }

    $query->close();
    header("Location: index.php");
}

// Function to reverse the buzz status of a specific cell
function reverseBuzzCell($conn, $cellID)
{
    $query = $conn->prepare("UPDATE cell SET buzz = 0 WHERE cellID = ?");
    $query->bind_param("i", $cellID);
    $query->execute();

    if ($query->error) {
        die("Error reversing buzz: " . $query->error);
    }

    $query->close();
    header("Location: index.php");
}

// Function to reverse the door status of a specific cell
function reverseOpenDoorCell($conn, $cellID)
{
    $query = $conn->prepare("UPDATE cell SET openDoor = 0 WHERE cellID = ?");
    $query->bind_param("i", $cellID);
    $query->execute();

    if ($query->error) {
        die("Error reversing door: " . $query->error);
    }

    $query->close();
    header("Location: index.php");
}

function getAllCellEntries($conn)
{
    $query = "SELECT cellNo, buzz, openDoor FROM cell ORDER BY cellID DESC";
    return $conn->query($query);
}

function getAllGuardEntries($conn)
{
    $query = "SELECT guardID, guardName FROM guard ORDER BY guardID DESC";
    return $conn->query($query);
}


// Function to get recent turretLog entries
function getRecentTurretLogEntries($conn)
{
    $query = "SELECT activity, timeAct FROM turretLog ORDER BY timeAct DESC LIMIT 5";
    return $conn->query($query);
}

function toggleTurret($conn)
{
    // Implement the logic to toggle the turret state in the database
    // For example, if you have a 'turretActive' field in your database, you can toggle its value (0 or 1)
    // Make sure to update the query based on your database schema

    // Assuming you have a 'turretActive' field in a 'turret' table
    $query = "UPDATE turret SET turretActive = 1 - turretActive";

    if ($conn->query($query) === TRUE) {
        echo "Turret state toggled successfully.";
    } else {
        echo "Error toggling turret state: " . $conn->error;
    }
}

function changeTurretRange($conn, $newRange)
{

    $newRange = (int) $newRange; // Convert to integer for safety
    $query = "UPDATE turret SET turretRange = $newRange";

    if ($conn->query($query) === TRUE) {
        echo "Turret range changed successfully.";
    } else {
        echo "Error changing turret range: " . $conn->error;
    }
}

function getTurretInfo($conn)
{
    // Implement the logic to fetch turret information from the database
    // For example, if you have a 'turret' table, retrieve 'turretActive' and 'turretRange' values
    // Make sure to update the query based on your database schema

    // Assuming you have a 'turret' table
    $query = "SELECT turretActive, turretRange FROM turret";
    $result = $conn->query($query);

    if (!$result) {
        die("Error retrieving turret information: " . $conn->error);
    }


    return $result;
}



?>
