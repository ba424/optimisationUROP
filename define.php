<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="background">
    
    <h1>1. Define</h1>
    <p><i>Let us know what you want to optimize.</i></p>

    <h2>What factors do you need to decide?</h2>
    <p><i>Describe each factor that you want to decide. Examples: “saddle height”, “material thickness”.</i></p>
    
    <div id="parameter-table-div" style="text-align: center;">
        <table id="parameter-table" class="parameter-table" width="100%">
            <caption><b>Design Parameters</b></caption>
            <thead>  
                <tr>  
                <th id="record-parameter-name" width="40%"> Name </th>   
                <th id="record-parameter-lower-bound"> Lower Bound </th>  
                <th id="record-parameter-upper-bound"> Upper Bound </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound"></td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound"></td>
            </tr>
            </tbody>
        </table>
    </div>

    <h2>Which measurements do you want to optimize?</h2>
    <p><i>Describe your objectives. You can include also subjective measurements, even opinions. Examples: “fatigue”, “fuel efficiency”, “price”.</i></p>
    <div id="objective-table-div" style="text-align: center;">
        <table id="objective-table" class="objective-table" width="100%">
            <caption><b>Design Objectives<b></caption>
            <thead>  
                <tr>  
                <th id="record-objective-name" width="40%"> Name </th>   
                <th id="record-objective-lower-bound"> Lower Bound </th>  
                <th id="record-objective-upper-bound"> Upper Bound </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name"></td>
                <td contenteditable="true" class="record-data" id="record-objective-lower-bound"></td>
                <td contenteditable="true" class="record-data" id="record-objective-upper-bound"></td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name"></td>
                <td contenteditable="true" class="record-data" id="record-objective-lower-bound"></td>
                <td contenteditable="true" class="record-data" id="record-objective-upper-bound"></td>
            </tr></tbody>
        </table>
    </div>
    <br>

    <div style="text-align: right;">
        <button class="finish-objectives-button" id="finish-objectives-button" onclick="finishObjs()">Ready</button>
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
    
        #finish-objectives-button {
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
            background-color: white;
            text-align: center;
        }
        th {
            background-color: #D6EEEE;
        }
    
    </style>
    
    <script>
        function finishObjs() {
            var noError = true;
            var parameterNames = [];
            var parameterBounds = [];
            var objectiveNames = [];
            var objectiveBounds = [];
    
            /* var participantID = localStorage.getItem("id");
            var conditionID = localStorage.getItem("exp-condition");
            var applicationID = localStorage.getItem("app"); */
            
            var tableParam = $("#parameter-table tbody");
                
            tableParam.find('tr').each(function() {
                var $paramCols = $(this).find("td");
                var paramRowEntries = [];
    
                $.each($paramCols, function() {
                    paramRowEntries.push($(this).text());
                });
                
                var paramName = paramRowEntries[0];
                if (/^[A-Za-z0-9]+$/.test(paramName)){
                    parameterNames.push(paramName);
                }
                else {
                    noError = false;
                }
    
                var paramLowerBound = paramRowEntries[1];
                var paramUpperBound = paramRowEntries[2];
                var validLowerBound = (!isNaN(parseFloat(paramLowerBound)) && isFinite(paramLowerBound));
                var validUpperBound = (!isNaN(parseFloat(paramUpperBound)) && isFinite(paramUpperBound));

                if (validLowerBound && validUpperBound){
                    if (parseFloat(paramLowerBound) < parseFloat(paramUpperBound)){
                        var rowBounds = [parseFloat(paramLowerBound), parseFloat(paramUpperBound)];
                        parameterBounds.push(rowBounds);
                    }
                    else {
                       noError = false;
                    }
                }
                else {
                    noError = false;
                }
            });

            // Find all the objective names and bounds
            var tableObjs = $("#objective-table tbody");
                
            tableObjs.find('tr').each(function() {
                var $objCols = $(this).find("td");
                var objRowEntries = [];
    
                $.each($objCols, function() {
                    objRowEntries.push($(this).text());
                });
                
                var objName = objRowEntries[0];
                if (/^[A-Za-z0-9]+$/.test(objName)){
                    objectiveNames.push(objName);
                }
                else {
                    noError = false;
                }
    
                var objLowerBound = objRowEntries[1];
                var objUpperBound = objRowEntries[2];
                var validLowerBound = (!isNaN(parseFloat(objLowerBound)) && isFinite(objLowerBound));
                var validUpperBound = (!isNaN(parseFloat(objUpperBound)) && isFinite(objUpperBound));

                if (validLowerBound && validUpperBound){
                    if (parseFloat(objLowerBound) < parseFloat(objUpperBound)){
                        var rowBounds = [parseFloat(objLowerBound), parseFloat(objUpperBound)];
                        objectiveBounds.push(rowBounds);
                    }
                    else {
                       noError = false;
                    }
                }
                else {
                    noError = false;
                }
            });
            
            console.log(parameterNames);
            console.log(parameterBounds);
            console.log(objectiveNames);
            console.log(objectiveBounds);

            if (parameterBounds.length != parameterNames.length && parameterBounds.length <= 1){
                noError = false;
            }

            if (objectiveBounds.length != objectiveNames.length){
                noError = false;
            }
    
            if (noError){
                localStorage.setItem("parameter-names", parameterNames);
                localStorage.setItem("parameter-bounds", parameterBounds);
                localStorage.setItem("objective-names", objectiveNames);
                localStorage.setItem("objective-bounds", objectiveBounds);
    
                // localStorage.setItem("tutorial-done", true);
    
                $.ajax({
                    /* url: "./cgi/start_log.py",
                    type: "post",
                    datatype: "json",
                    data: { 'participant_id'    :String(participantID),
                            'application_id'    :String(applicationID),
                            'condition_id'      :String(conditionID) },*/
                    success: function(result) {
                    submitReturned = true;
                    
                    var url = "existing-solutions.php";
                    location.href = url;
                    },
                    error: function(result){
                        console.log("Error in finishing experiment: " + result.message);
                    }
                });
            }
            else {
                alert("Invalid entry");
            }    
        }
    </script>
    
    </body>
</html>


