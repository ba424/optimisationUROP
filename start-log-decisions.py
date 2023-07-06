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

expectedArgs = ['parameter_name', 'parameter_unit', 'parameter_bounds']
formValuesDefined = checkFormData(formData, expectedArgs)

if not formValuesDefined:
    success = False
    message = "Form values not defined."
else:
    conn = sqlite3.connect("Data/database.db")
    c = conn.cursor()

    createFunctionTableQuery = '''CREATE TABLE IF NOT EXISTS time (param_name TEXT, param_unit TEXT, param_bounds TEXT)'''
    c.execute(createFunctionTableQuery)
    conn.commit()

    parameterName = str(formData['parameter_name'].value)
    parameterUnit = str(formData['parameter_unit'].value)
    parameterBounds = str(formData['parameter_bounds'].value)
    # typeStr = "start"
    # timeStr = str(time.time())

    query = ''' INSERT INTO time VALUES (?, ?, ?)'''
    c.execute(query, (parameterName, parameterUnit, parameterBounds))

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