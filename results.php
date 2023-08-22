<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div id="background">
    
    <h1>3. Results</h1>
    <p><i>Here are the best options we found</i></p>
    
    <p><b>Option 1</b></p>
    <p id="parameter_1_option_1"></p>
    <p id="parameter_2_option_1"></p> 
    <p id="option_1_text" style="font-style: italic"></p>

    <p><b>Option 2</b></p>
    <p id="parameter_1_option_2"></p>
    <p id="parameter_2_option_2"></p> 
    <p id="option_2_text" style="font-style: italic"></p>

    <p><b>Option 3</b></p>
    <p id="parameter_1_option_3"></p>
    <p id="parameter_2_option_3"></p> 
    <p id="option_3_text" style="font-style: italic"></p>

    <br>
    <div class="restart-button" style="text-align: left;">
        <form action="/Demo/define.php">
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
            width: 600px;
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

    <script>
        var parameterNames = localStorage.getItem("parameter-names").split(",");
        var parameterBounds = localStorage.getItem("parameter-bounds").split(",");
        var objectiveNames = localStorage.getItem("objective-names").split(",");
        var objectiveBounds = localStorage.getItem("objective-bounds").split(",");
        var objectiveMinMax = localStorage.getItem("objective-min-max").split(",");
        // var goodSolutions = localStorage.getItem("good-solutions").split(",");
        // var badSolutions = localStorage.getItem("bad-solutions").split(",");
        // var solutionList = localStorage.getItem("solution-list").split(",");
        var savedSolutions = localStorage.getItem("saved-solutions").split(",");
        var objectivesInput = localStorage.getItem("objectives-input").split(",");
        var objectivesNormalised = localStorage.getItem("objectives-normalised").split(",");
        var bestSolutions = localStorage.getItem("best-solutions").split(",");

        console.log(savedSolutions);
        console.log(objectivesInput);
        console.log(objectivesNormalised);
        console.log(bestSolutions)

        document.getElementById("parameter_1_option_1").innerHTML = parameterNames[0] + ": " + bestSolutions[0];
        document.getElementById("parameter_2_option_1").innerHTML = parameterNames[1] + ": " + bestSolutions[1];
        document.getElementById("option_1_text").innerHTML = "This option is great in <b>" + parameterNames[0] + "</b> but weaker in <b>" + parameterNames[1].bold() + "</b>.";
        
        document.getElementById("parameter_1_option_2").innerHTML = parameterNames[0] + ": " + bestSolutions[2];
        document.getElementById("parameter_2_option_2").innerHTML = parameterNames[1] + ": " + bestSolutions[3];
        document.getElementById("option_2_text").innerHTML = "This option is great in <b>" + parameterNames[1] + "</b> but weaker in <b>" + parameterNames[0].bold() + "</b>.";
        
        document.getElementById("parameter_1_option_3").innerHTML = parameterNames[0] + ": " + bestSolutions[4];
        document.getElementById("parameter_2_option_3").innerHTML = parameterNames[1] + ": " + bestSolutions[5];
        document.getElementById("option_3_text").innerHTML = "This option offers a balance between <b>" + parameterNames[0] + "</b> and <b>" + parameterNames[1].bold() + "</b>.";

    </script>
</body>
</html>

