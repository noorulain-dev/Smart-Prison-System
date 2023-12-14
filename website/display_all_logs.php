<?php
include 'db_connection.php';
include 'header.php';
include 'functions.php';

// Assuming you have a function to establish a database connection, e.g., getDBConnection()


// Function to display all logs for the specified type
function displayAllLogs($conn, $logType)
{
    $table = ($logType === 'patrol') ? 'patrol' : 'turretLog';

    $query = "SELECT * FROM $table";
    $result = $conn->query($query);

    echo "<h2>All $logType Logs</h2>";
    echo "<table>";
    echo "<tr>";

    // Display table headers dynamically based on the retrieved columns
    while ($row = $result->fetch_assoc()) {
        foreach ($row as $column => $value) {
            echo "<th>$column</th>";
        }
        break; // Display only one row of headers
    }
    echo "</tr>";

    // Display all logs
    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        foreach ($row as $value) {
            echo "<td>$value</td>";
        }
        echo "</tr>";
    }

    echo "</table>";
}

// Check if 'type' is set in the query parameters
if (isset($_GET['type'])) {
    $logType = $_GET['type'];
    
    // Check if the specified type is either 'patrol' or 'turretLog'
    if ($logType === 'patrol' || $logType === 'turretLog') {
        displayAllLogs($conn, $logType);
    } else {
        echo "Invalid log type specified.";
    }
} else {
    echo "Log type not specified.";
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display All Logs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }

        h2 {
            color: #333;
        }

        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }

        table,
        th,
        td {
            border: 1px solid #333;
            text-align: center;
        }

        th,
        td {
            padding: 10px;
        }
    </style>
</head>

<body>
    <!-- ... (any additional content you want to include) ... -->

</body>

</html>
