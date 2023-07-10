#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\python.exe
import sys
import json
import cgi
import numpy as np
import sqlite3

# Initialize the basic reply message
message = "Necessary objects imported."
success = True

# Read provided formData
formData = cgi.FieldStorage()

# Define function for checking that required parameters have been submitted
def checkFormData(data, expectedArgs):
    argsDefined = True
    for i in range(0,len(expectedArgs)):
        if expectedArgs[i] not in data:
            argsDefined = False
            break
    return argsDefined

# Define function for converting param points to csv string
def arrayToCsv(values):
    csv_string = ""
    n = values.shape[0]
    for i in range(0,n):
        if (i > 0):
            csv_string += ","
        csv_string += str(values[i])
    return csv_string

expectedArgs = ['project_id', 'parameter_name', 'parameter_unit', 'parameter_lower_bound', 'parameter_upper_bound']
formValuesDefined = checkFormData(formData, expectedArgs)

if not formValuesDefined:
    success = False
    message = "Form values not defined."
else:
    conn = sqlite3.connect("Data/database.db")
    c = conn.cursor()

    createFunctionTableQuery = '''CREATE TABLE IF NOT EXISTS parameters (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        project_id INTEGER, 
        param_name TEXT, 
        param_unit TEXT, 
        param_lower_bound INTEGER, 
        param_upper_bound INTEGER
        )'''

    c.execute(createFunctionTableQuery)
    conn.commit()
    
    projectID = (formData['project_id'].value)
    parameterName = str(formData['parameter_name'].value)
    parameterUnit = str(formData['parameter_unit'].value)
    parameterLowerBound = (formData['parameter_lower_bound'].value)
    parameterUpperBound = (formData['parameter_upper_bound'].value)
    # typeStr = "start"
    # timeStr = str(time.time())
    
    # for i in range(len(projectID)):
    query = '''INSERT INTO parameters (project_id,param_name,param_unit,param_lower_bound,param_upper_bound) VALUES (?, ?, ?, ?, ?)'''
    # c.execute(query, (int(projectID[i]), parameterName[i], parameterUnit[i], int(parameterLowerBound[i]), int(parameterUpperBound[i])))
    c.execute(query, (int(projectID), parameterName, parameterUnit, int(parameterLowerBound), int(parameterUpperBound)))

    conn.commit()
    conn.close()

    message = json.dumps("success")

reply = {}
reply['success'] = True
reply['message'] = message

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

sys.stdout.write(json.dumps(reply,indent=1))
sys.stdout.write("\n")

sys.stdout.close()