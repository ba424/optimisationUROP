<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <?php
    // $one = htmlspecialchars($_GET["one"]);
    // $two = htmlspecialchars($_GET["two"]);
    
    // echo "one: $one two: $two";
    ?>

    <div id="background">
    
    <h1>2. Optimise</h1>
    <p><i>Let AI suggest solutions with you</i></p>
    
    <p><b>Solution idea</b><p>
    <!-- <div style="display: flex; justify-content: left;">
        <p class="parameter_1_mobo"></p><p id="solution_1"></p>
    </div>
    <div style="display: flex; justify-content: left;">
        <p class="parameter_2_mobo"></p><p id="solution_2"></p>
    </div>
    <div style="display: flex; justify-content: left;">
        <p class="parameter_3_mobo"></p><p id="solution_3"></p>
    </div> -->

    <p class="parameter_1_mobo"></p>
    <p class="parameter_2_mobo"></p>
    <p class="parameter_3_mobo"></p>

    
    <div id="options" style="display: inline-block; margin: 0 auto;">
        <button class="button" id="evaluate-button" style="width: 40%;" onclick="evaluateSolution()">I want to evaluate this</button>
        <button class="button" id="skip-button" style="width: 40%;" onclick="nextSolution()">Skip. I know it's not good</button>
    </div>
    
    <div id="evaluate-solution" style="display: none;">
        <form action="">
            <input size="40" placeholder="Give a memorable name to this idea" style="font-family: calibri; font-size: medium;"><br><br>
            <label for="obj1" class="objective_1_measure"></label>
            <input type="text" id="obj1" name="obj1" placeholder="Enter measurement" style="font-family: calibri; font-size: medium;"><br>
            <label for="obj2" class="objective_2_measure"></label>
            <input type="text" id="obj2" name="obj2" placeholder="Enter measurement" style="font-family: calibri; font-size: medium;"><br>
            
            <div id="form-options" style="display: inline-block; margin: 0 auto;">
                <button type="submit" class="button" id="next-button" onclick="nextSolution()">Give me the next one</button>
                <button type="submit" class="button" id="skip-button" formaction="" onclick="refineSolution()">I want to refine this</button>
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
        var parameterNames = localStorage.getItem("parameter-names").split(",");
        var parameterBounds = localStorage.getItem("parameter-bounds").split(",");
        var objectiveNames = localStorage.getItem("objective-names").split(",");
        var objectiveBounds = localStorage.getItem("objective-bounds").split(",");
        var objectiveMinMax = localStorage.getItem("objective-min-max").split(",");
        var goodSolutions = localStorage.getItem("good-solutions").split(",");
        var badSolutions = localStorage.getItem("bad-solutions").split(",");
        var solution = localStorage.getItem("solution").split(",");
        
        var paras1 = document.getElementsByClassName("parameter_1_mobo");
        var paras2 = document.getElementsByClassName("parameter_2_mobo");
        var paras3 = document.getElementsByClassName("parameter_3_mobo");
        
        for (i = 0; i < paras1.length; i++) {
            paras1[i].innerHTML = parameterNames[0] + " =  " + solution[0];
            paras2[i].innerHTML = parameterNames[1] + " =  " + solution[1];
            paras3[i].innerHTML = parameterNames[2] + " =  " + solution[2];
        }
        
        // Individual solutions
        // document.getElementById("solution_1").innerHTML = solution[0];
        // document.getElementById("solution_2").innerHTML = solution[1];
        // document.getElementById("solution_3").innerHTML = solution[2];

        function evaluateSolution() {
            var obj1 = document.getElementsByClassName("objective_1_measure");
            var obj2 = document.getElementsByClassName("objective_2_measure");

            for (i = 0; i < paras1.length; i++) {
                obj1[i].innerHTML = objectiveNames[0] + " = ";
                obj2[i].innerHTML = objectiveNames[1] + " = ";
            }
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

        function nextSolution() {
            $.ajax({
                url: "../Demo/cgi/initial_mobo.py",
                type: "post",
                datatype: "json",
                data: { 'parameter-names'    :String(parameterNames),
                        'parameter-bounds'   :String(parameterBounds),
                        'objective-names'    :String(objectiveNames), 
                        'objective-bounds'   :String(objectiveBounds),
                        'objective-min-max'  :String(objectiveMinMax),
                        'good-solutions'     :String(goodSolutions),
                        'bad-solutions'      :String(badSolutions)},
                success: function(result) {
                    submitReturned = true;
                    solution = result.solution
                    localStorage.setItem("solution", solution);
                    console.log("Success");
                    var url = "optimise.php";
                    location.href = url;
                },
                error: function(result){
                    console.log("Error in finishing experiment: " + result.message);
                }
            });
        }

    </script>
</body>
</html>


