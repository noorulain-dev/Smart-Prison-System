<?php
include 'db_connection.php';
include 'header.php';
include 'functions.php';

$recentCellEntries = getAllCellEntries($conn);
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cell Information</title>
</head>

<body>

    <h2>Cell Information</h2>
    <table border="1">
        <tr>
            <th>Cell Number</th>
            <th>Buzz</th>
            <th>Open Door</th>
            <th>Cell Information</th>
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
</body>

</html>