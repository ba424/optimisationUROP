#! C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe
import sys
import json
import cgi
import sqlite3
import requests

from import_all import *

# Initialize the basic reply message
message = "Necessary objects imported."
success = True

# Read provided formData
formData = cgi.FieldStorage()

parameterNames = (formData['parameter-names'].value).split(',')
parameterBounds = (formData['parameter-bounds'].value).split(',')
objectiveNames = (formData['objective-names'].value).split(',')
objectiveBounds = (formData['objective-bounds'].value).split(',')
objectiveMinMax = (formData['objective-min-max'].value).split(',')
savedSolutions = (formData['saved-solutions'].value).split(',')
savedObjectives = (formData['saved-objectives'].value).split(',')
# objectivesInput = (formData['objectives-input'].value).split(',')

num_parameters = len(parameterNames)
parameter_bounds = torch.zeros(2, num_parameters)
parameter_bounds_normalised = torch.zeros(2, num_parameters)
for i in range(num_parameters):
    parameter_bounds[0][i] = float(parameterBounds[2*i])
    parameter_bounds[1][i] = float(parameterBounds[2*i + 1])
    parameter_bounds_normalised[0][i] = float(0)
    parameter_bounds_normalised[1][i] = float(1)

objective_bounds = torch.zeros(2, 2)
for i in range(2):
    objective_bounds[0][i] = float(objectiveBounds[2*i])
    objective_bounds[1][i] = float(objectiveBounds[2*i + 1])

def normalise_objectives(obj_tensor_actual):
    objectives_min_max = objectiveMinMax
    obj_tensor_norm = torch.zeros(obj_tensor_actual.size(), dtype=torch.float64)
    for j in range(obj_tensor_actual.size()[0]):
        for i in range (obj_tensor_actual.size()[1]):
            if (objectives_min_max[i] == "minimise"): # MINIMISE (SMALLER VALUES CLOSER TO 1)
                obj_tensor_norm[j][i] = -2*((obj_tensor_actual[j][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) + 1
            elif (objectives_min_max[i] == "maximise"): # MAXIMISE (LARGER VALUES CLOSER TO -1)
                obj_tensor_norm[j][i] =  2*((obj_tensor_actual[j][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) - 1
    return obj_tensor_norm

objectivesInputPlaceholder = []
for i in range(int(len(savedObjectives)/2)):
    objectivesInputPlaceholder.append([float(savedObjectives[2*i]), float(savedObjectives[2*i+1])])
savedObjectives = objectivesInputPlaceholder
train_obj_actual = torch.tensor(savedObjectives, dtype=torch.float64)
train_obj = normalise_objectives(train_obj_actual)

best_solutions = []
best_obj_1_normalised = -100
best_obj_2_normalised = -100
best_obj_balance_normalised = -100
objectives_list_normalised = train_obj.tolist()

obj_1_normalised = []
obj_2_normalised = []
obj_balance_normalised = []

for i in range(int(len(objectives_list_normalised))):
    obj_1_normalised.append(objectives_list_normalised[i][0])
    obj_2_normalised.append(objectives_list_normalised[i][1])
    obj_balance_normalised.append(objectives_list_normalised[i][0] + objectives_list_normalised[i][1])

best_obj_1_index = np.argsort(obj_1_normalised)
best_obj_2_index = np.argsort(obj_2_normalised)
best_obj_balance_index = np.argsort(obj_balance_normalised)

if (best_obj_2_index[-1] == best_obj_1_index[-1]):
    best_obj_2_index = best_obj_2_index[:-1] # remove last element
while (best_obj_balance_index[-1] == best_obj_1_index[-1] or best_obj_balance_index[-1] == best_obj_2_index[-1]):
    best_obj_balance_index = best_obj_balance_index[:-1]

# Placeholders / Dummy variables for conditioning to avoid same solution being proposed twice
# best_obj_1_index, best_obj_2_index, best_obj_balance_index = [], [], []
# best_obj_2_index = 101
# best_obj_balance_index = 102

# for i in range(len(objectives_list_normalised)):
#     if (objectives_list_normalised[i][0] > best_obj_1_normalised and best_obj_1_index != best_obj_2_index and best_obj_1_index != best_obj_balance_index):
#         best_obj_1_normalised = objectives_list_normalised[i][0]
#         best_obj_1_index = i
#     if (objectives_list_normalised[i][1] > best_obj_2_normalised and best_obj_2_index != best_obj_1_index and best_obj_2_index != best_obj_balance_index):
#         best_obj_2_normalised = objectives_list_normalised[i][1]
#         best_obj_2_index = i
#     if (objectives_list_normalised[i][0] + objectives_list_normalised[i][1] > best_obj_balance_normalised):
#         best_obj_balance_normalised = objectives_list_normalised[i][0] + objectives_list_normalised[i][1]
#         best_obj_balance_index = i
# best_solutions.append(savedSolutions[best_obj_1_index*num_parameters:best_obj_1_index*num_parameters+num_parameters])
# best_solutions.append(savedSolutions[best_obj_2_index*num_parameters:best_obj_2_index*num_parameters+num_parameters])
# best_solutions.append(savedSolutions[best_obj_balance_index*num_parameters:best_obj_balance_index*num_parameters+num_parameters])

best_solutions.append(savedSolutions[best_obj_1_index[-1]*num_parameters:best_obj_1_index[-1]*num_parameters+num_parameters])
best_solutions.append(savedSolutions[best_obj_2_index[-1]*num_parameters:best_obj_2_index[-1]*num_parameters+num_parameters])
best_solutions.append(savedSolutions[best_obj_balance_index[-1]*num_parameters:best_obj_balance_index[-1]*num_parameters+num_parameters])

reply = {}

reply['success'] = True
reply['message'] = message
# reply['objectives'] = objectivesInput
reply['saved_solutions'] = savedSolutions
reply['saved_objectives'] = savedObjectives
reply['objectives_normalised'] = train_obj.tolist()
reply['best_solutions'] = best_solutions

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

sys.stdout.write(json.dumps(reply,indent=1))
sys.stdout.write("\n")

sys.stdout.close()