# Optimise Anything: UROP 2023

## Introduction
The purpose of this project is to develop a program to perform multi-objective Bayesian optimisation (MOBO) aimed at the every day person. It includes the ability to define design paramters and design objectives to be minimised and/or maximised. The user is also able to define solutions that are already known to not be satisfactory. 

## Front-end
The PHP files represent the front-end of the program. The sequence of pages is:
1. `welcome.php`: Welcome page
2. `how-it-works.php`: Brief overview of how the AI-user guided optimisation works
3. `define.php`: Page to define design parameters and design objectives
4. `confirm-definitions.php`: Confirmation of design definitions
5. `existing-solutions.php`: Known bad solutions can be added here
6. `optimise.php`: Solutions proposed by AI and evaluated by user
7. `results.php`: Summary of best solutions evaluated
