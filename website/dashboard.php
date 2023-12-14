<?php
include 'db_connection.php';
include 'header.php';
include 'functions.php';
// Fetch data from the database
$recentCellEntries = getRecentCellEntries($conn);
$recentGuardEntries = getRecentGuardEntries($conn);
$recentPatrolEntries = getRecentPatrolEntries($conn);
$recentEnvEntries = getRecentEnvEntries($conn);
$recentTurretLogEntries = getRecentTurretLogEntries($conn);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $cellID = $_POST["cellID"];
    $action = $_POST["action"];

    switch ($action) {
        case "buzzAll":
            buzzAllCells($conn);
            break;
        case "openAll":
            openAllDoors($conn);
            break;
        case "reverseBuzzAll":
            reverseBuzzAllCells($conn);
            break;
        case "reverseOpenAll":
            reverseOpenAllDoors($conn);
            break;
        case "buzzCell":
            buzzCell($conn, $cellID);
            break;
        case "openDoorCell":
            openDoorCell($conn, $cellID);
            break;
        case "reverseBuzzCell":
            reverseBuzzCell($conn, $cellID);
            break;
        case "reverseOpenDoorCell":
            reverseOpenDoorCell($conn, $cellID);
            break;
        // Add other cases as needed
    }
}

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prison IoT Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }

        h1,
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
            /* Center-align content in table cells */
        }

        th,
        td {
            padding: 10px;
        }

        button {
            padding: 10px;
            margin: 5px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        select,
        input[type="hidden"] {
            padding: 10px;
            margin: 5px;
        }
    </style>
</head>

<body>
    <h1>Prison IoT Dashboard</h1>

    <!-- Display data from the recent patrol entries -->
    <h2>Recent Patrol Activities</h2>
    <table>
        <tr>
            <th>Cell ID</th>
            <th>Guard ID</th>
            <th>Activity Name</th>
            <th>Activity Time</th>
        </tr>
        <?php
        while ($row = $recentPatrolEntries->fetch_assoc()) {
            echo "<tr>";
            echo "<td>{$row['cellID']}</td>";
            echo "<td>{$row['guardID']}</td>";
            echo "<td>{$row['activityName']}</td>";
            echo "<td>{$row['activityTime']}</td>";
            echo "</tr>";
        }
        ?>
    </table>

    <button onclick="window.location.href='display_all_logs.php?type=patrol'">Display All Patrol Logs</button>


    <!-- Display data from the recent turretLog entries -->
    <h2>Recent Turret Log Activities</h2>
    <table>
        <tr>
            <th>Activity</th>
            <th>Time</th>
        </tr>
        <?php
        while ($row = $recentTurretLogEntries->fetch_assoc()) {
            echo "<tr>";
            echo "<td>{$row['activity']}</td>";
            echo "<td>{$row['timeAct']}</td>";
            echo "</tr>";
        }
        ?>
    </table>

    <button onclick="window.location.href='display_all_logs.php?type=turretLog'">Display All Turret Logs</button>



</body>

</html>