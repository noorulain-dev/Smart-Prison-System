<?php
include 'db_connection.php';
include 'header.php';
include 'functions.php';
// Fetch data from the database
$recentCellEntries = getRecentCellEntries($conn);
$recentGuardEntries = getRecentGuardEntries($conn);
$recentPatrolEntries = getRecentPatrolEntries($conn);
$recentEnvEntries = getRecentEnvEntries($conn);
$turretInfo = getTurretInfo($conn);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
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
            $cellID = $_POST["cellID"];
            buzzCell($conn, $cellID);
            break;
        case "openDoorCell":
            $cellID = $_POST["cellID"];
            openDoorCell($conn, $cellID);
            break;
        case "reverseBuzzCell":
            $cellID = $_POST["cellID"];
            reverseBuzzCell($conn, $cellID);
            break;
        case "reverseOpenDoorCell":
            $cellID = $_POST["cellID"];
            reverseOpenDoorCell($conn, $cellID);
            break;
        case "toggleTurret":
            toggleTurret($conn);
            break;
        case "changeTurretRange":
            $newRange = $_POST["newRange"];
            changeTurretRange($conn, $newRange);
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

    <h2>Cell Information</h2>
    <table border="1">
        <tr>
            <th>Cell Number</th>
            <th>Buzz</th>
            <th>Open Door</th>
            <th>Action</th>
        </tr>
        <?php while ($row = $recentCellEntries->fetch_assoc()): ?>
            <tr>
                <td>
                    <?php echo $row['cellNo']; ?>
                </td>
                <td>
                    <?php echo $row['buzz']; ?>
                </td>
                <td>
                    <?php echo $row['openDoor']; ?>
                </td>
                <td>
                    <button onclick="viewCellDetails('<?php echo $row['cellNo']; ?>')">View Cell</button>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>

    <script>
        function viewCellDetails(cellNumber) {
            console.log('Clicked on cellNumber:', cellNumber);
            window.location.href = 'cell.php?cellNumber=' + cellNumber;
        }
    </script>


    <!-- Dropdown to select cellNo -->
    <label for="cellSelect">Select Cell Number:</label>
    <form method="post" action="index.php">
        <select id="cellSelect" name="cellID">
            <?php
            // Fetch all cell numbers from the database
            $allCellNumbers = getAllCellNumbers($conn);

            // Populate options in the dropdown
            while ($cellRow = $allCellNumbers->fetch_assoc()) {
                echo "<option value='" . $cellRow['cellID'] . "'>" . $cellRow['cellNo'] . "</option>";
            }
            ?>
        </select>

        <!-- Add buttons and other form elements as needed -->
        <button type="submit" name="action" value="buzzCell">Buzz Cell</button>
        <button type="submit" name="action" value="openDoorCell">Open Door</button>
        <button type="submit" name="action" value="reverseBuzzCell">Reverse Buzz</button>
        <button type="submit" name="action" value="reverseOpenDoorCell">Reverse Door</button>
    </form>

    <script>
        window.onload = function () {
            document.getElementById('cellSelect').addEventListener('change', function () {
                var selectedCellID = this.value;
                document.getElementById('selectedCellID').value = selectedCellID;
            });
        };
    </script>


    <form action="index.php" method="post">
        <button type="submit" name="action" value="buzzAll">Buzz All</button>
        <button type="submit" name="action" value="openAll">Open All</button>
        <button type="submit" name="action" value="reverseBuzzAll">Reverse Buzz All</button>
        <button type="submit" name="action" value="reverseOpenAll">Reverse Open All</button>
    </form>

    <h2>Turret Information</h2>
    <table border="1">
        <tr>
            <th>Turret Active</th>
            <th>Turret Range</th>
        </tr>
        <?php while ($turretRow = $turretInfo->fetch_assoc()): ?>
            <tr>
                <td>
                    <?php echo $turretRow['turretActive']; ?>
                </td>
                <td>
                    <?php echo $turretRow['turretRange']; ?>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>
    <!-- Turret control form -->
    <form method="post" action="index.php">
        <!-- Add buttons and other form elements as needed -->
        <button type="submit" name="action" value="toggleTurret">Toggle Turret</button>
        <label for="newRange">New Turret Range (0-99):</label>
        <input type="number" id="newRange" name="newRange" min="0" max="99">
        <button type="submit" name="action" value="changeTurretRange">Change Turret Range</button>
    </form>




</body>

</html>
