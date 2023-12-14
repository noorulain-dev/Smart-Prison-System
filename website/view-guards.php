<?php
include 'db_connection.php';
include 'header.php';
include 'functions.php';

$recentGuardEntries = getAllGuardEntries($conn);
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



    <h2>Guard Information</h2>
    <table border="1">
        <tr>
            <th>Guard ID</th>
            <th>Guard Name</th>
            <th>Action</th>
        </tr>
        <?php while ($row = $recentGuardEntries->fetch_assoc()): ?>
            <tr>
                <td>
                    <?php echo $row['guardID']; ?>
                </td>
                <td>
                    <?php echo $row['guardName']; ?>
                </td>
                <td>
                    <button onclick="viewGuardDetails('<?php echo $row['guardID']; ?>')">View Details</button>
                </td>
            </tr>
        <?php endwhile; ?>
    </table>

    <script>
        function viewGuardDetails(guardID) {
            console.log('Clicked on guardID:', guardID);
            window.location.href = 'guard.php?guardID=' + guardID;
        }
    </script>


</body>

</html>