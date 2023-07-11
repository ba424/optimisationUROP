<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="background">
    
    <h1>1. Define: Objectives</h1>
    <p><i>Let us know what you want to optimize.</i></p>
    <h2>Which measurements do you want to optimize?</h2>
    <p><i>Describe your objectives. You can include also subjective measurements, even opinions. Examples: “fatigue”, “fuel efficiency”, “price”.</i></p>
    
    <div id="objective-table-div" style="text-align: center;">
        <table id="objective-table" class="objective-table" width="100%">
            <caption><h4>Design Objectives</h4></caption>
            <thead>  
                <tr>  
                <th id="record-objective-name" width="40%"> Name </th>  
                <th id="record-objective-type"> Categ or Cont </th>  
                <th id="record-objective-units"> Units </th>  
                <th id="record-objective-min-max"> Min or Max </th>  
                </tr>  
            </thead>  
            <tbody>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name"></td>
                <td contenteditable="true" class="record-data" id="record-objective-type">
                    <!--<select style="font-family: 'Calibri';">
                        <option value="none" selected disabled hidden><i>Select</i></option>        
                        <option value="categorical">Categ</option>
                        <option value="continuous">Cont</option>
                    </select>*/-->
                </td>
                <td contenteditable="true" class="record-data" id="record-objective-units"></td>
                <td contenteditable="true" class="record-data" id="record-objective-min-max">
                    <!--<select style="font-family: 'Calibri';">
                        <option value="none" selected disabled hidden><i>Select</i></option>        
                        <option value="min">Minimise</option>
                        <option value="max">Maximise</option>
                    </select>-->
                </td>
            </tr>
            <tr>
                <td contenteditable="true" class="record-data" id="record-objective-name"></td>
                <td contenteditable="true" class="record-data" id="record-objective-type">
                    <!--<select style="font-family: 'Calibri';">
                        <option value="none" selected disabled hidden><i>Select</i></option>        
                        <option value="categorical">Categ</option>
                        <option value="continuous">Cont</option>
                    </select>-->
                </td>
                <td contenteditable="true" class="record-data" id="record-objective-units"></td>
                <td contenteditable="true" class="record-data" id="record-objective-min-max">
                    <!--<select style="font-family: 'Calibri';">
                        <option value="none" selected disabled hidden><i>Select</i></option>            
                        <option value="min">Min</option>
                        <option value="max">Max</option>
                    </select>--> 
                </td>
            </tr></tbody>
        </table>
        <br>
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
            padding: 16px 16px;
            margin: 4px 4px;
            border-radius: 12px;
            display: inline-block;
            border:1px solid black;
            width: 500px;
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
            var objectiveNames = [];
            var objectiveTypes = [];
            var objectiveUnits = [];
            var objectiveBounds = [];
    
            /* var participantID = localStorage.getItem("id");
            var conditionID = localStorage.getItem("exp-condition");
            var applicationID = localStorage.getItem("app"); */
    
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
                
                var objType = objRowEntries[1];
                if (objType == "Categ" || objType == "Cont"){
                    objectiveTypes.push(objType);
                }
                else {
                    noError = false;
                }
                
                var objUnit = objRowEntries[2];
                if (/^[A-Za-z0-9]+$/.test(objUnit)){
                    objectiveUnits.push(objUnit);
                }
                else {
                    noError = false;
                }
    
                var objBound = objRowEntries[3];
                if (objBound == "Min" || objBound == "Max"){
                    objectiveBounds.push(objBound);
                }
                else {
                    noError = false;
                }
            });
            
            if (objectiveBounds.length != objectiveNames.length){
                noError = false;
            }
    
            if (noError){
                localStorage.setItem("objective-names", objectiveNames);
                localStorage.setItem("objective-types", objectiveTypes);
                localStorage.setItem("objective-units", objectiveUnits);
                localStorage.setItem("objective-bounds", objectiveBounds);
    
                localStorage.setItem("tutorial-done", true);
    
                $.ajax({
                    /* url: "./cgi/start_log.py",
                    type: "post",
                    datatype: "json",
                    data: { 'participant_id'    :String(participantID),
                            'application_id'    :String(applicationID),
                            'condition_id'      :String(conditionID) },*/
                    success: function(result) {
                    submitReturned = true;
                    
                    var url = "pre-optimise.php";
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


