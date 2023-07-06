<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>
<body>
    <div id="background">
    
    <h1>1. Define: Decisions</h1>
    <p><i>Let us know what you want to optimize.</i></p>
    <h2>What factors do you need to decide?</h2>
    <p><i>Describe each factor that you want to decide. Examples: “saddle height”, “material thickness”, “lamp color”.</i></p>
    
    <div id="parameter-table-div" style="text-align: center;">
        <table id="parameter-table" class="parameter-table" width="100%">
            <caption><h4>Design Parameters</h4></caption>
            <thead>  
                <tr>  
                <th id="record-parameter-name" width="40%"> Name </th>  
                <th id="record-parameter-unit"> Units </th>  
                <th id="record-parameter-lower"> Min </th>  
                <th id="record-parameter-upper"> Max </th>
                <th id='record-parameter-trash'> Delete </th>  
                </tr>  
            </thead>  
            <tbody>
            </tbody>
        </table>
        <br>
        <div>
            <button class="button" id="add-record-button" onclick="addParameterTable()">Add Parameter</button>
        </div>
    </div>
    <br>
    <div style="text-align: right;">
        <button class="button" id="finish-parameters-button" onclick="finishParams()">Finish</button>
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
    
        #finish-parameters-button {
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
        #add-record-button {
            text-align: center;
            font-family: calibri;
            font-size: medium;
            background-color: #D6EEEE;
            padding: 8px 16px;
            margin: 4px 2px;
            border-radius: 12px;
            border-width: 1.5px;
            display: inline-block;
            cursor:pointer;
        }
    
    </style>
    
    <script>
        function addParameterTable(){
            var htmlNewRow = ""
            htmlNewRow += "<tr>"
            htmlNewRow += "<td contenteditable='true' class='record-data' id='record-parameter-name'></td>"

            htmlNewRow += "<td contenteditable='true' class='record-data' id='record-parameter-unit'></td>"

            htmlNewRow += "<td contenteditable='true' class='record-data' id='record-parameter-lower'></td>"
            
            htmlNewRow += "<td contenteditable='true' class='record-data' id='record-parameter-upper'></td>"
            
            htmlNewRow += "<td id='record-data-buttons'>"
            htmlNewRow += "<button class='record-delete' id='record-delete'><img src='./Pictures/delete.png' style='width: 20px'></button>"
            htmlNewRow += "</td></tr>"
            $("#parameter-table", window.document).append(htmlNewRow);  

            $(window.document).on('click', ".record-delete", deleteParameterTable);
        }

        function deleteParameterTable(){
            $(this).parents('tr').remove();
        }

        function finishParams() {
            var noError = true;
            var parameterNames = [];
            var parameterUnits = [];
            var parameterBounds = [];
    
            /* var participantID = localStorage.getItem("id");
            var conditionID = localStorage.getItem("exp-condition");
            var applicationID = localStorage.getItem("app"); */
    
            // Find all the objective names and bounds
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
                
                var paramUnit = paramRowEntries[1];
                if (/^[A-Za-z0-9]+$/.test(paramUnit)){
                    parameterUnits.push(paramUnit);
                }
                else {
                    noError = false;
                }
    
                var parameterLowerBound = paramRowEntries[2];
                var parameterUpperBound = paramRowEntries[3];
                var validLowerBound = (!isNaN(parseFloat(parameterLowerBound)) && isFinite(parameterLowerBound));
                var validUpperBound = (!isNaN(parseFloat(parameterUpperBound)) && isFinite(parameterUpperBound));

                if (validLowerBound && validUpperBound){
                    if (parseFloat(parameterLowerBound) < parseFloat(parameterUpperBound)){
                        var rowBounds = [parseFloat(parameterLowerBound), parseFloat(parameterUpperBound)];
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
            
            if (parameterBounds.length != parameterNames.length){
                noError = false;
            }
    
            if (noError){
                localStorage.setItem("parameter_name", parameterNames);
                localStorage.setItem("parameter_unit", parameterUnits);
                localStorage.setItem("parameter_bounds", parameterBounds);
    
                localStorage.setItem("tutorial-done", true);
    
                $.ajax({
                    url: "./start-log-decisions.py",
                    type: "post",
                    datatype: "json",
                    data: { 'parameter_name'    :String(parameterNames),
                            'parameter_unit'    :String(parameterUnits),
                            'parameter_bounds'  :String(parameterBounds) },
                    success: function(result) {
                    submitReturned = true;
                    
                    var url = "define-objectives.php";
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


