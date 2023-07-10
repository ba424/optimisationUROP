<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>

<body>
    <div id="background">
    
    <h1>One question before we start…</h1>
    <p><i>Are there known good/bad solutions we should include?</i></p>

    <div id="buttons" style="display:block">
        <div class="add-existing-solutions">
            <button id="add-existing-solutions" onclick="addExistingSolutions()">Yes, some</button>
        </div>

        <div class="start-button">
            <form action="/Demo/optimise.php" id="start-form">
                <button id="start" type="submit">No, let's start</button>
            </form>
        </div>

        <div class="clearfix"></div>
    </div>

    <div id="add-solutions" style="display:none">
        <table id="known-solutions-table" class="known-solutions-table" width="100%">
            <caption><h4>Known Solutions</h4></caption>
            <thead>  
                <tr>  
                <th id="variable-1"> Variable 1: [] </th>  
                <th id="varibale-2"> Variable 2: [] </th>  
                <th id="good-bad"> Good or Bad </th> 
                <th id="good-bad"> Delete </th>   
                </tr>  
            </thead>  
            <tbody>
            </tbody>
        </table>
        <br>

        <div style="text-align: center;">
            <button class="button" id="add-record-button" onclick="addSolutionsTable()">Add Solution</button>
        </div>
        <br>

        <div style="display: flex; justify-content: space-between;">
            <button class="button" id="back-button" onclick="addExistingSolutions()">Back</button>
            <button class="button" id="finish-solutions-button" onclick="finishSolutions()">Finish</button>
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
    
        .add-existing-solutions{
            width:20%;
            margin-right:2%;
            float: left;
        }
        .start-button {
            width:30%;
            float: left;
        }
        .clearfix{
            clear:both
        }

        #start, #add-existing-solutions, #finish-solutions-button, #back-button {
            background-color: #70ad47;
            font-family: 'Calibri';
            font-size: medium;
            color: white;
            cursor:pointer;
            border-radius: 12px;
            border-width: 1.5px;
            padding: 16px 16px;
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
        function addExistingSolutions() {
            var x = document.getElementById('add-solutions');
            var y = document.getElementById('buttons')
            if (x.style.display == 'none') {
                x.style.display = 'block';
                y.style.display = 'none';
            }
            else {
                x.style.display = 'none';
                y.style.display = 'block';
            }
        }

        function addSolutionsTable(){
            var htmlNewRow = ""
            htmlNewRow += "<tr>"
            htmlNewRow += "<td contenteditable='true' class='record-data' id='variable-1'></td>"

            htmlNewRow += "<td contenteditable='true' class='record-data' id='variable-2'></td>"

            htmlNewRow += "<td contenteditable='true' class='record-data' id='good-bad'></td>"
            
            htmlNewRow += "<td id='record-data-buttons'>"
            htmlNewRow += "<button class='record-delete' id='record-delete'><img src='./Pictures/delete.png' style='width: 20px'></button>"
            htmlNewRow += "</td></tr>"
            $("#known-solutions-table", window.document).append(htmlNewRow);  

            $(window.document).on('click', ".record-delete", deleteParameterTable);
        }

        function deleteParameterTable(){
            $(this).parents('tr').remove();
        }

        function finishSolutions() {
            $.ajax({
                /* url: "./cgi/start_log.py",
                type: "post",
                datatype: "json",
                data: { 'participant_id'    :String(participantID),
                        'application_id'    :String(applicationID),
                        'condition_id'      :String(conditionID) },*/
                success: function(result) {
                submitReturned = true;
                
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
    
    

