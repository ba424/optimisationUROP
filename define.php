<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="background">
    
    <h1>1. Define</h1>
    <p><i>Let us know what you want to optimize. An example is shown below for optimizing the travel for a holiday, which you can edit to implement your optimization.</i></p>

    <h2>What factors do you need to decide?</h2>
    <p><i>Describe each factor that you want to decide. Examples: “destination distance”, “number of days” amd "number of flight connections".</i></p>
    
    <div id="parameter-table-div" style="text-align: center;">
        <table id="parameter-table" class="parameter-table" width="100%">
            <caption><b>Design Parameters</b></caption>
            <thead>  
                <tr>  
                <th id="record-parameter-name" width="40%"> Name </th>   
                <th id="record-parameter-lower-bound"> Minimum </th>  
                <th id="record-parameter-upper-bound"> Maximum </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name">Destination distance (km)</td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound">500</td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound">3000</td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name">Number of days</td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound">3</td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound">14</td>
            </tr>
            <!-- <tr>
                <td contenteditable="true" class="record-data" id="record-parameter-name">Number of flight connections</td>
                <td contenteditable="true" class="record-data" id="record-parameter-lower-bound">0</td>
                <td contenteditable="true" class="record-data" id="record-parameter-upper-bound">3</td>
            </tr> -->
            </tbody>
        </table>
    </div>

    <h2>Which measurements do you want to optimize?</h2>
    <p><i>Describe your objectives. You can include also subjective measurements, even opinions. Examples: “cost”, “travel time”.</i></p>
    <div id="objective-table-div" style="text-align: center;">
        <table id="objective-table" class="objective-table" width="100%">
            <caption><b>Design Objectives<b></caption>
            <thead>  
                <tr>  
                <th id="record-objective-name" width="40%"> Name </th>   
                <th id="record-objective-lower-bound"> Minimum </th>  
                <th id="record-objective-upper-bound"> Maximum </th> 
                <th id="record-objective-min-max"> Minimise or Maximise </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name">Cost ($)</td>
                <td contenteditable="true" class="record-data" id="record-objective-lower-bound">100</td>
                <td contenteditable="true" class="record-data" id="record-objective-upper-bound">1000</td>
                <td contenteditable="false" class="record-data" id="record-objective-min-max">
                    <select id="min-max-1" style="font-family: calibri; font-size: medium;">
                        <option value="minimise" selected="selected">minimise</option>
                        <option value="maximise">maximise</option>
                    </select>
                </td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name">Satisfaction (%)</td>
                <td contenteditable="true" class="record-data" id="record-objective-lower-bound">0</td>
                <td contenteditable="true" class="record-data" id="record-objective-upper-bound">100</td>
                <td contenteditable="false" class="record-data" id="record-objective-min-max">
                    <select id="min-max-2" style="font-family: calibri; font-size: medium;">
                        <option value="minimise">minimise</option>
                        <option value="maximise" selected="selected">maximise</option>
                    </select>
                </td>
            </tr></tbody>
        </table>
    </div>
    <br>

    <div style="text-align: right;">
        <button class="button" id="finish-objectives-button" style="width: 20%;" onclick="finishObjs()">Ready</button>
    </div>
    
    </div>
    
    <script>
        function finishObjs() {
            var noError = true;
            var parameterNames = [];
            var parameterBounds = [];
            var objectiveNames = [];
            var objectiveBounds = [];
            var objectiveMinMax = [];
    
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
                parameterNames.push(paramName);

                // if (/^[A-Za-z0-9]+$/.test(paramName)){
                //     parameterNames.push(paramName);
                // }
                // else {
                //     noError = false;
                // }
    
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
                objectiveNames.push(objName);

                // if (/^[A-Za-z0-9]+$/.test(objName)){
                //     objectiveNames.push(objName);
                // }
                // else {
                //     noError = false;
                // }
    
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

            // Store whether each objective is to be minimised or maximised in a list
            var min_max_1 = document.getElementById("min-max-1").value;
            var min_max_2 = document.getElementById("min-max-2").value;
            objectiveMinMax.push(min_max_1, min_max_2);

            console.log(parameterNames);
            console.log(parameterBounds);
            console.log(objectiveNames);
            console.log(objectiveBounds);
            console.log(objectiveMinMax);

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
                localStorage.setItem("objective-min-max", objectiveMinMax);
    
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
                    
                    var url = "confirm-definitions.php";
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


