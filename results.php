<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div id="background">
    
    <h1>3. Results</h1>
    <p><i>Here are the best options we found</i></p>
    
    <p><b>Option 1</b></p>
    <p>[Variable 1 = ?] [Variable 2 = ?]</p> 
    <p>This option is great in param1 and param2, but weaker in param3.</p>

    <p><b>Option 2</b></p>
    <p>[Variable 1 = ?] [Variable 2 = ?] </p>
    <p>This option is great in param1, but weaker in param2 and param3.</p>

    <br>
    <div class="restart-button" style="text-align: left;">
        <form action="/Demo/welcome.php">
            <button id="restart-button" type="submit">Restart</button>
        </form>
    </div>

    </div>
    <style>
        body {
            font-family: 'Calibri';
        }
    
        #background {
            background-color: #f2f2f2;
            padding: 16px 16px;
            margin: 4px 4px;
            border-radius: 12px;
            display: inline-block;
            border:1px solid black;
            width: 500px;
        }
    
        #restart-button {
            text-align: center;
            font-family: calibri;
            font-size: medium;
            color: white;
            background-color: #70ad47;
            padding: 8px 16px;
            margin: 4px 2px;
            border-radius: 12px;
            border-width: 1.5px;
            display: inline-block;
            width: 40%;
            cursor:pointer;
        }
    
    </style>
</body>
</html>

