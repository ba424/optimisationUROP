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

expectedArgs = ['parameter-names', 'parameter-bounds', 'objective-names', 'objective-bounds', 'objective-min-max']
formValuesDefined = checkFormData(formData, expectedArgs)

if not formValuesDefined:
    success = False
    message = "Form values not defined."
else:
    conn = sqlite3.connect("../Data/database.db")
    c = conn.cursor()

    createFunctionTableQuery_1 = '''CREATE TABLE IF NOT EXISTS definitions_parameters (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        param_name TEXT, 
        param_lower_bound INTEGER,
        param_upper_bound INTEGER  
        )'''

    c.execute(createFunctionTableQuery_1)
    conn.commit()

    createFunctionTableQuery_2 = '''CREATE TABLE IF NOT EXISTS definitions_objectives (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        obj_name TEXT, 
        obj_lower_bound INTEGER,
        obj_upper_bound INTEGER,
        obj_min_max TEXT 
        )'''

    c.execute(createFunctionTableQuery_2)
    conn.commit()

    parameterNames = (formData['parameter-names'].value).split(',')
    parameterBounds = (formData['parameter-bounds'].value).split(',')
    objectiveNames = (formData['objective-names'].value).split(',')
    objectiveBounds = (formData['objective-bounds'].value).split(',')
    objectiveMinMax = (formData['objective-min-max'].value).split(',')

    # typeStr = "start"
    # timeStr = str(time.time())

    for i in range(len(parameterNames)):
        query = '''INSERT INTO definitions_parameters (param_name,param_lower_bound,param_upper_bound) VALUES (?, ?, ?)'''
        c.execute(query, (parameterNames[i], parameterBounds[2*i], parameterBounds[2*i+1]))

        if (i<2):
            query = '''INSERT INTO definitions_objectives (obj_name,obj_lower_bound,obj_upper_bound,obj_min_max) VALUES (?, ?, ?, ?)'''
            c.execute(query, (objectiveNames[i], objectiveBounds[2*i], objectiveBounds[2*i+1], objectiveBounds[i]))

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