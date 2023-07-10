<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div id="background">
    
    <h1>2. Optimise</h1>
    <p><i>Let AI suggest solutions with you</i></p>
    
    <p><b>1st solution idea</b><p>
    <p>[Variable 1 = ] [Variable 2 = ]</p>

    <div id="options" style="display: inline-block; margin: 0 auto;">
        <button class="button" id="evaluate-button" style="width: 40%;" onclick="evaluateSolution()">I want to evaluate this</button>
        <button class="button" id="skip-button" style="width: 40%;" onclick="">Skip. I know it's not good</button>
    </div>
    
    <div id="evaluate-solution" style="display: none;">
        <form action="">
            <input size="40" placeholder="Give a memorable name to this idea" style="font-family: calibri; font-size: medium;"><br><br>
            <label for="param1">param1 = </label>
            <input type="text" id="param1" name="param1" placeholder="Enter measurement" style="font-family: calibri; font-size: medium;"><br>
            <label for="param2">param2 = </label>
            <input type="text" id="param2" name="param2" placeholder="Enter measurement" style="font-family: calibri; font-size: medium;"><br>
            <label for="param3">param3 = </label>
            <input type="text" id="param3" name="param3" placeholder="Enter measurement" style="font-family: calibri; font-size: medium;"><br><br>
            
            <div id="form-options" style="display: inline-block; margin: 0 auto;">
                <button type="submit" class="button" id="next-button">Give me the next one</button>
                <button type="submit" class="button" id="skip-button" formaction="">I want to refine this</button>
            </div>
        </form>
    </div>
    <br>
    <div class="done-button" style="text-align: right;">
        <form action="/Demo/results.php" id="done-button">
            <button class="button" id="done" type="submit">I'm done</button>
        </form>
    </div>

    </div>
    <style>
        body {
            font-family: calibri;
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
    
        .button {
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
            cursor:pointer;
        }
    
    </style>

    <script>
        function evaluateSolution() {
            var x = document.getElementById('evaluate-solution');
            var y = document.getElementById('options')
            if (x.style.display == 'none') {
                x.style.display = 'block';
                y.style.display = 'none';
            }
            else {
                x.style.display = 'none';
                y.style.display = 'inline-block';
            }
        }
    </script>
</body>
</html>


