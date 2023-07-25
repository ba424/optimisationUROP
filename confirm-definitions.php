<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="background">
    
    <h1>1. Define</h1>
    <p><i>Let us know what you want to optimize.</i></p>

    <h2>Confirmation</h2>
    <p><i>Please confirm your design parameters and objectives are defined correctly.</i></p>
    
    <div id="parameter-table-div" style="text-align: center;">
        <table id="parameter-table" class="parameter-table" width="100%">
            <caption><b>Design Parameters</b></caption>
            <thead>  
                <tr>  
                <th id="check-parameter-name" width="40%"> Name </th>   
                <th id="check-parameter-lower-bound"> Lower Bound </th>  
                <th id="check-parameter-upper-bound"> Upper Bound </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="check-data" id="check-parameter-name-1"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-lower-bound-1"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-upper-bound-1"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="check-data" id="check-parameter-name-2"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-lower-bound-2"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-upper-bound-2"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="check-data" id="check-parameter-name-3"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-lower-bound-3"></td>
                <td contenteditable="true" class="check-data" id="check-parameter-upper-bound-3"></td>
            </tr>
            </tbody>
        </table>
    </div>
    <br>
    <div id="objective-table-div" style="text-align: center;">
        <table id="objective-table" class="objective-table" width="100%">
            <caption><b>Design Objectives<b></caption>
            <thead>  
                <tr>  
                <th id="check-objective-name" width="40%"> Name </th>   
                <th id="check-objective-lower-bound"> Lower Bound </th>  
                <th id="check-objective-upper-bound"> Upper Bound </th>
                <th id="check-objective-min-max"> Minimise or Maximise </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="check-data" id="check-objective-name-1"></td>
                <td contenteditable="true" class="check-data" id="check-objective-lower-bound-1"></td>
                <td contenteditable="true" class="check-data" id="check-objective-upper-bound-1"></td>
                <td contenteditable="true" class="check-data" id="check-objective-min-max-1"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="check-data" id="check-objective-name-2"></td>
                <td contenteditable="true" class="check-data" id="check-objective-lower-bound-2"></td>
                <td contenteditable="true" class="check-data" id="check-objective-upper-bound-2"></td>
                <td contenteditable="true" class="check-data" id="check-objective-min-max-2"></td>
            </tr></tbody>
        </table>
    </div>
    <br>

    <!-- <div style="text-align: right;">
        <button class="finish-objectives-button" id="finish-objectives-button" onclick="finishObjs()">Ready</button>
    </div> -->
    
    <div style="display: flex; justify-content: space-between;">
        <button class="button" id="back-button" onclick="history.back()">Go Back</button>
        <button class="button" id="confirm-definitions-button" onclick="confirmDefinitions()">Confirm</button>
    </div>

    </div>
    
    
    <style>
        body {
            font-family: calibri;
        }
    
        #background {
            background-color: #f2f2f2;
            padding: 0px 16px;
            margin: 0px 0px;
            border-radius: 12px;
            display: inline-block;
            border:1px solid black;
            width: 650px;
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
            width: 20%;
            cursor:pointer;
        }
    
        table, th, td {
            border: 1px solid;
            border-collapse: collapse;
            text-align: center;
        }
        th {
            background-color: #D6EEEE;
        }
    
    </style>
    
    <script>
        var parameterNames = localStorage.getItem("parameter-names").split(",");
        var parameterBoundsRaw = localStorage.getItem("parameter-bounds").split(",");
        var objectiveNames = localStorage.getItem("objective-names").split(",");
        var objectiveBoundsRaw = localStorage.getItem("objective-bounds").split(",");
        var objectiveMinMax = localStorage.getItem("objective-min-max").split(",");

        var parameterBounds = [];
        var objectiveBounds = [];

        for (var i = 0; i<parameterNames.length; i++) {
            parameterBounds.push([parameterBoundsRaw[2*i], parameterBoundsRaw[2*i+1]])
            if (i<2) {
                objectiveBounds.push([objectiveBoundsRaw[2*i], objectiveBoundsRaw[2*i+1]])
            }
        }

        for (var i = 0; i<parameterNames.length; i++) {
            document.getElementById("check-parameter-name-" + (i+1)).innerHTML = parameterNames[i];
            document.getElementById("check-parameter-lower-bound-" + (i+1)).innerHTML = parameterBounds[i][0];
            document.getElementById("check-parameter-upper-bound-" + (i+1)).innerHTML = parameterBounds[i][1];
        
            if (i<2) {
                document.getElementById("check-objective-name-" + (i+1)).innerHTML = objectiveNames[i];
                document.getElementById("check-objective-lower-bound-" + (i+1)).innerHTML = objectiveBounds[i][0];
                document.getElementById("check-objective-upper-bound-" + (i+1)).innerHTML = objectiveBounds[i][1];
                document.getElementById("check-objective-min-max-" + (i+1)).innerHTML = objectiveMinMax[i];
            }
        }

        function confirmDefinitions() {
            localStorage.setItem("parameter-names", parameterNames);
            localStorage.setItem("parameter-bounds", parameterBounds);
            localStorage.setItem("objective-names", objectiveNames);
            localStorage.setItem("objective-bounds", objectiveBounds);
            localStorage.setItem("objective-min-max", objectiveMinMax);

            // localStorage.setItem("tutorial-done", true);

            $.ajax({
                url: "../Demo/cgi/log-definitions.py",
                type: "post",
                datatype: "json",
                data: { 'parameter-names'    :String(parameterNames),
                        'parameter-bounds'   :String(parameterBounds),
                        'objective-names'    :String(objectiveNames), 
                        'objective-bounds'   :String(objectiveBounds),
                        'objective-min-max'  :String(objectiveMinMax)},
                
                success: function(result) {
                    submitReturned = true;
                    console.log("Success");
                    var url = "existing-solutions.php";
                    location.href = url;
                },
                error: function(result){
                    console.log("Error");
                }
            });
        }  
        
    </script>
    
    </body>
</html>


