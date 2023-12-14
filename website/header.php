<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prison IoT Dashboard</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0; /* Background color for the body */
        }

        header {
            width: 100%;
            height: auto;
            overflow: hidden;
        }

        header img {
            width: 100%;
            height: 50px;
        }

        nav {
            background-color: #333; /* Background color for the navigation bar */
            color: white;
            text-align: center;
            padding: 10px;
            width: 100%;
            box-sizing: border-box;
        }

        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        li {
            display: inline-block;
            margin-right: 20px;
        }

        a {
            text-decoration: none;
            color: white;
            font-weight: bold;
            font-size: 16px;
        }

        a:hover {
            color: #ffd700; /* Change color on hover */
        }

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
            text-align: center; /* Center-align content in table cells */
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
    <header>
        <img src="jail.webp" alt="Prison Header Image">
    </header>

    <nav>
        <ul>
            <li><a href="dashboard.php">Dashboard</a></li>
            <li><a href="index.php">Control Center</a></li>
            <li><a href="view-guards.php">View Guards</a></li>
            <li><a href="view-cells.php">View All Cells</a></li>
        </ul>
    </nav>
</body>

</html>
