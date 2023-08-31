<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <div id="background">
    
    <h1>Help</h1>
    <h2 id="define">(i) Define</h2>
    <p> At this stage, you define the design parameters and objectives of your problem. An example for optimising the travel for a holiday is included by default for reference which can be edited.</p>
    <p> The design parameters are limited to 2 in this current version. You must specify the name of each parameter, as well as the minimum and maximum numerical value each parameter can take. It is advised you include the units of any parameter in the name where applicable. </p>
    <p> The design objectives are limited to 2. As with the parameters, ensure you define a suitable name for each parameter and the minimum and maximum numerical values. You must also indicate whether you wish to minimise or maximise each objective. </p> 
    <p> Once you're ready, click <b>'Ready'</b> to proceed to the next stage where you confirm your choices. An error will be raised if any fields are left blank, if any of the minimum or maximum values are not numbers and/or if the minimum value is larger than or equal to the maximum value.</p>
    <div style="text-align: center;">
        <button class="button" id="back-button" onclick="history.back()" style="width: 20%;">Go Back</button>    
    </div>
    
    <h2 id="existing-solutions">(ii) Existing solutions</h2>
    <p> Before proceeding to the optimisation stage, you can include any exisitng solutions that you know are bad. The AI will not propose any solutions that are within 5% of the listed bad solutions.</p>
    <p> If there are no bad solutions that you are aware of, you can proceed directly to the optimisation stage by click 'No let's start'.</p> 
    <p> To include a bad solution, click the button <b>'Yes, some'</b>. You will then be presented with a table of the design parameters where, by clicking <b>'Add Bad Solution'</b>, you are able to insert the parameter values of such solutions.</p> 
    <p> Once you have included all the bad solutions, click <b>'Finish'</b> to proceed. An error will be raised if any entry is blank and/or if any entry is not a number within the specified parameter range defined previously. You are able to delete any entry by clicking the red trash button on the right column of the table.</p> 
    <p><i>Note: It is possible to click <b>'Finish'</b> with no entries in the table.</i></p>
    <div style="text-align: center;">
        <button class="button" id="back-button" onclick="history.back()" style="width: 20%;">Go Back</button>    
    </div>
    
    <h2 id="optimisation">(iii) Optimisation</h2>
    <p> The AI will propose possible solution ideas. There are two possible options: </p>
    <p> <b>1. Skip:</b> By clicking <b>'Skip, I know it's not good'</b>, the AI will propose a new solution. The solution that had been proposed will be automatically saved as a <i>'bad solution'</i> so that the AI does not propose the same solution again. </p>
    <p> <b>2. Evaluate:</b> By clicking <b>'I want to evaluate this'</b> you will be tasked with inputting the objective values obtained that correspond to the proposed solution idea. You can also give a name of your choice to the solution (the naming is automatically set as <i>'Solution #'</i> where # is the solution number). After evaluating there are two options: </p>
    <p style="text-indent: 1em"> <b>(a) 'Give me the next one':</b> This will lead the AI to propose the next solution based off the previous solutions. </p>
    <p style="text-indent: 1em"> <b>(b) 'I want to refine this':</b> The AI will propose the next solution to be within 5% of the current solution. </p>
    <p> To proceed to the final results, at least 3 solutions must be evaluated. The <b>'I'm done'</b> button will then appear on the bottom right which you can click to move on to the results section. </p>
    <div style="text-align: center;">
        <button class="button" id="back-button" onclick="history.back()" style="width: 20%;">Go Back</button>    
    </div>

    <h2 id="results">(iv) Results</h2>
    <p>The results page will summarise the three best solutions that the AI has determined based off the objective values found: </p> 
    <ul>
        <li><b>'Option 1'</b> gives the best solution that optimises the 1st objective</li>
        <li><b>'Option 2'</b> gives the best solution that optimises the 2nd objective</li>
        <li><b>'Option 3'</b> gives the best average solution that balances both objectives</li>
    </ul>
    <p> Each solution will be different to provide three unique solutions. If you wish to return and optimise the solutions further, click the button <b>'Go Back'</b>, otherwise click <b>'Restart'</b> to return to the problem definition page, where you can define a new problem to optimise.</p>
    <div style="text-align: center;">
        <button class="button" id="back-button" onclick="history.back()" style="width: 20%;">Go Back</button>    
    </div>
    
    </div>
</body>
</html>
    

