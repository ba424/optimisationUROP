<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>

<body>
    <div id="background">
    
    <h1>One question before we start…</h1>
    <p><i>Are there known bad solutions we should include?</i></p>
    
    <div class="tooltip">For example
        <span class="tooltiptext" style="display: flex; justify-content: space-between; padding: 0px 10px;">
                <p id="parameter1_example"></p>
                <p id="parameter2_example"></p>
                <!-- <p class="parameter3"></p><p>1</p> -->
        </span>
    </div>
    <br>
    <br>
 
    <div id="buttons" style="display:block">
        <div class="add-existing-solutions" style=" margin-right:2%; float: left;">
            <button id="add-existing-solutions" class="button" onclick="addExistingSolutions()">Yes, some</button>
        </div>

        <div class="start-button" style=" float: left;">
            <button id="start" class="button" onclick="finishSolutions()">No let's start</button>
        </div>

        <!-- <div class="start-button">
            <form action="/Demo/optimise.php" id="start-form">
                <button id="start" type="submit">No, let's start</button>
            </form>
        </div> -->

        <div class="clearfix" style="clear: both;"></div>
    </div>

    <div id="add-solutions" style="display:none">
        <!-- <table id="good-solutions-table" class="good-solutions-table" width="100%">
            <caption><b>Good Solutions</b></caption>
            <thead>  
                <tr>  
                <th class="parameter1"></th>  
                <th class="parameter2"></th> -->  
                <!-- <th class="parameter3"></th>  -->
                <!-- <th class="delete"> Delete </th>   
                </tr>  
            </thead>  
            <tbody>
            </tbody>
        </table>

        <div style="text-align: center;">
            <button class="button" id="add-record-button" onclick="addGoodSolutionsTable()">Add Good Solution</button>
        </div> 
        <br> -->
        <table id="bad-solutions-table" class="bad-solutions-table" width="100%">
            <caption><b>Bad Solutions</b></caption>
            <thead>  
                <tr>  
                <th class="parameter1"></th>  
                <th class="parameter2"></th>  
                <!-- <th class="parameter3"></th>  -->
                <th class="delete"> Delete </th>   
                </tr>  
            </thead>  
            <tbody>
            </tbody>
        </table>

        <div style="text-align: center;">
            <button class="button" id="add-record-button" onclick="addBadSolutionsTable()" style="color: black; background-color: #D6EEEE;">Add Bad Solution</button>
        </div>
        <br>

        <div style="text-align: right;">
            <button class="button" id="finish-solutions-button" onclick="finishSolutions()">Finish</button>
        </div>
        
        <!--
        <div style="display: flex; justify-content: space-between;">
            <button class="button" id="back-button" onclick="addExistingSolutions()">Back</button>
            <button class="button" id="finish-solutions-button" onclick="finishSolutions()">Finish</button>
        </div>
        -->
    </div>

    <style>
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 600px;
            background-color: #6a6e73;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            
            /* Position the tooltip */
            position: absolute;
            z-index: 1;
            top: -5px;
            left: 105%;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
        }

    </style>
    <script>
        var parameterNames = localStorage.getItem("parameter-names").split(",");
        var parameterBounds = localStorage.getItem("parameter-bounds").split(",");
        var objectiveNames = localStorage.getItem("objective-names").split(",");
        var objectiveBounds = localStorage.getItem("objective-bounds").split(",");
        var objectiveMinMax = localStorage.getItem("objective-min-max").split(",");
        
        var paras1 = document.getElementsByClassName("parameter1");
        var paras2 = document.getElementsByClassName("parameter2");
        // var paras3 = document.getElementsByClassName("parameter3");
        
        for (i = 0; i < paras1.length; i++) {
            paras1[i].innerHTML = parameterNames[0];
            paras2[i].innerHTML = parameterNames[1];
            // paras3[i].innerHTML = parameterNames[2];
        }

        document.getElementById("parameter1_example").innerHTML = parameterNames[0] +": "+parameterBounds[0];
        document.getElementById("parameter2_example").innerHTML = parameterNames[1] +": "+parameterBounds[2];

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

        // function addGoodSolutionsTable(){
        //     var htmlNewRow = ""
        //     htmlNewRow += "<tr>"
        //     htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter1'></td>"
        //     htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter2'></td>"
        //     // htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter3'></td>"
        //     htmlNewRow += "<td id='record-data-buttons'>"
        //     htmlNewRow += "<button class='record-delete' id='record-delete'><img src='./Pictures/delete.png' style='width: 20px'></button>"
        //     htmlNewRow += "</td></tr>"
        //     $("#good-solutions-table", window.document).append(htmlNewRow);  
        //     $(window.document).on('click', ".record-delete", deleteParameterTable);
        // }

        function addBadSolutionsTable(){
            var htmlNewRow = ""
            htmlNewRow += "<tr>"
            htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter1'></td>"
            htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter2'></td>"
            // htmlNewRow += "<td contenteditable='true' class='record-data' id='parameter3'></td>"
            htmlNewRow += "<td id='record-data-buttons'>"
            htmlNewRow += "<button class='record-delete' id='record-delete'><img src='./Pictures/delete.png' style='width: 20px'></button>"
            htmlNewRow += "</td></tr>"
            $("#bad-solutions-table", window.document).append(htmlNewRow);  
            $(window.document).on('click', ".record-delete", deleteParameterTable);
        }

        function deleteParameterTable(){
            $(this).parents('tr').remove();
        }

        function finishSolutions() {
            var noError = true;
            var newSolution = true;
            var nextEvaluation = false;
            var refineSolution = false;
            var goodSolutions = [];
            var badSolutions = [];
            // Register good solutions
            // var tableGoodSols = $("#good-solutions-table tbody");
            // tableGoodSols.find('tr').each(function() {
            //     var $goodSolsCols = $(this).find("td");
            //     var goodSolsRowEntries = [];
    
            //     $.each($goodSolsCols, function() {
            //         goodSolsRowEntries.push($(this).text());
            //     });
    
            //     var goodSolParam1 = goodSolsRowEntries[0];
            //     var goodSolParam2 = goodSolsRowEntries[1];
            //     // var goodSolParam3 = goodSolsRowEntries[2];
            //     console.log(goodSolParam1);
            //     var validGoodSolParam1 = (!isNaN(parseFloat(goodSolParam1)) && isFinite(goodSolParam1) && parseFloat(goodSolParam1) >= parseFloat(parameterBounds[0]) && parseFloat(goodSolParam1) <= parseFloat(parameterBounds[1]));
            //     var validGoodSolParam2 = (!isNaN(parseFloat(goodSolParam2)) && isFinite(goodSolParam2) && parseFloat(goodSolParam2) >= parseFloat(parameterBounds[2]) && parseFloat(goodSolParam2) <= parseFloat(parameterBounds[3]));
            //     // var validGoodSolParam3 = (!isNaN(parseFloat(goodSolParam3)) && isFinite(goodSolParam3));

            //     if (validGoodSolParam1 && validGoodSolParam2 /*&& validGoodSolParam3*/){
            //         var rowBounds = [parseFloat(goodSolParam1), parseFloat(goodSolParam2)/*, parseFloat(goodSolParam3)*/];
            //         goodSolutions.push(rowBounds);
            //     }
            //     else {
            //         noError = false;
            //     }
            // });
            
            // Register bad solutions
            var tableBadSols = $("#bad-solutions-table tbody");
            tableBadSols.find('tr').each(function() {
                var $badSolsCols = $(this).find("td");
                var badSolsRowEntries = [];
    
                $.each($badSolsCols, function() {
                    badSolsRowEntries.push($(this).text());
                });
    
                var badSolParam1 = badSolsRowEntries[0];
                var badSolParam2 = badSolsRowEntries[1];
                //var badSolParam3 = badSolsRowEntries[2];
                console.log(badSolParam1);

                var validBadSolParam1 = (!isNaN(parseFloat(badSolParam1)) && isFinite(badSolParam1) && parseFloat(badSolParam1) >= parseFloat(parameterBounds[0]) && parseFloat(badSolParam1) <= parseFloat(parameterBounds[1]));
                var validBadSolParam2 = (!isNaN(parseFloat(badSolParam2)) && isFinite(badSolParam2) && parseFloat(badSolParam2) >= parseFloat(parameterBounds[2]) && parseFloat(badSolParam2) <= parseFloat(parameterBounds[3]));
                //var validBadSolParam3 = (!isNaN(parseFloat(badSolParam3)) && isFinite(badSolParam3));

                if (validBadSolParam1 && validBadSolParam2 /*&& validBadSolParam3*/){
                    var rowBounds = [parseFloat(badSolParam1), parseFloat(badSolParam2)/*, parseFloat(badSolParam3)*/];
                    badSolutions.push(rowBounds);
                }
                else {
                    noError = false;
                }
            });

            //console.log(goodSolutions);
            console.log(badSolutions);

            if (noError){
                localStorage.setItem("good-solutions", goodSolutions);
                localStorage.setItem("bad-solutions", badSolutions);
                localStorage.setItem("new-solution", newSolution);
                localStorage.setItem("next-evaluation", nextEvaluation);

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
                            'bad-solutions'      :String(badSolutions),
                            'new-solution'       :String(newSolution),
                            'next-evaluation'    :String(nextEvaluation),
                            'refine-solution'    :String(refineSolution)},
                    success: function(result) {
                        submitReturned = true;
                        solution = result.solution;
                        objectivesInput = result.objectives;
                        savedSolutions = result.saved_solutions;
                        savedObjectives = result.saved_objectives
                        localStorage.setItem("solution-list", solution);
                        localStorage.setItem("objectives-input", objectivesInput);
                        localStorage.setItem("saved-solutions", savedSolutions);
                        localStorage.setItem("saved-objectives", savedObjectives);
                        console.log(solution);
                        console.log("Success");
                        var url = "optimise.php";
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
    
    

