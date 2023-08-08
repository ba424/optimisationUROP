#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe
import sys
import json
import cgi
import numpy as np
import sqlite3
import requests

import os
import torch
from import_all import *
from botorch.models.gp_regression import FixedNoiseGP
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from botorch.utils.transforms import unnormalize, normalize
from botorch.utils.sampling import draw_sobol_samples

# os.environ['HOMEPATH'] = 'C:/Users/user/AppData/Local/Microsoft/WindowsApps'
# os.environ['HOME'] = 'C:/Users/user/AppData/Local/Microsoft/WindowsApps'
# os.environ['USERPROFILE'] = 'C:/Users/user/AppData/Local/Microsoft/WindowsApps/python.exe'

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

expectedArgs = ['parameter-names', 'parameter-bounds', 'objective-names', 'objective-bounds', 'objective-min-max', 'good-solutions', 'bad-solutions']
formValuesDefined = checkFormData(formData, expectedArgs)

# if not formValuesDefined:
#     success = False
#     message = "Form values not defined."
# else:
parameterNames = (formData['parameter-names'].value).split(',')
parameterBounds = (formData['parameter-bounds'].value).split(',')
objectiveNames = (formData['objective-names'].value).split(',')
objectiveBounds = (formData['objective-bounds'].value).split(',')
objectiveMinMax = (formData['objective-min-max'].value).split(',')
# goodSolutions = (formData['good-solutions'].value).split(',')
# badSolutions = (formData['bad-solutions'].value).split(',')


num_parameters = len(parameterNames)
parameter_bounds = torch.zeros(2, num_parameters)
parameter_bounds_normalised = torch.zeros(2, num_parameters)

for i in range(num_parameters):
    parameter_bounds[0][i] = float(parameterBounds[2*i])
    parameter_bounds[1][i] = float(parameterBounds[2*i + 1])
    parameter_bounds_normalised[0][i] = float(0)
    parameter_bounds_normalised[1][i] = float(1)

def unnormalise_parameters(x_tensor):
    x_bounds = parameter_bounds
    x_actual = torch.zeros(1, num_parameters)
    for i in range(num_parameters):
        x_actual[0][i] = x_tensor[0][i]*(x_bounds[1][i] - x_bounds[0][i]) + x_bounds[0][i]
    return x_actual

# generate training data
def generate_initial_data(n_samples=1):
    # generate training data
    train_x = draw_sobol_samples(
        bounds=parameter_bounds_normalised, n=1, q=n_samples, seed=torch.randint(1000000, (1,)).item()
    ).squeeze(0)
    train_x = train_x.type(torch.DoubleTensor)
    train_x_actual = torch.round(unnormalise_parameters(train_x))
    #print("Initial solution: ", train_x_actual)
    #train_obj_actual, train_obj = objective_function(train_x_actual)

    return train_x, train_x_actual

train_x, train_x_actual = generate_initial_data()

reply = {}
reply['solution'] = train_x_actual.tolist()
reply['success'] = True
reply['message'] = message

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

sys.stdout.write(json.dumps(reply,indent=1))
sys.stdout.write("\n")

sys.stdout.close()

    # while True:
    #     train_obj_1 = input("Enter Cost ($): ")
    #     try:
    #         train_obj_1 = float(train_obj_1)
    #         if (train_obj_1 >= 100 and train_obj_1 <= 1000):
    #             break
    #         else:
    #             raise ValueError
    #     except ValueError:
    #         print("Error. Please enter a valid measurement, within the objective bounds.")
    # while True:
    #     train_obj_2 = input("Enter Travel Time (hrs): ")
    #     try:
    #         train_obj_2 = float(train_obj_2)
    #         if (train_obj_2 >= 2 and train_obj_2 <= 10):
    #             break
    #         else:
    #             raise ValueError
    #     except ValueError:
    #         print("Error. Please enter a valid measurement, within the objective bounds.")

    # train_obj = torch.tensor([[float(train_obj_1), float(train_obj_2)]], dtype=torch.float64)
    # return train_x, train_obj


    # def initialize_model(train_x, train_obj):
    #     # define models for objective and constraint
    #     train_x = normalize(train_x, parameters)
    #     models = []
    #     for i in range(train_obj.shape[-1]):
    #         train_y = train_obj[..., i : i + 1]
    #         train_yvar = torch.full_like(train_y, NOISE_SE[i] ** 2)
    #         models.append(
    #             FixedNoiseGP(
    #                 train_x, train_y, train_yvar, outcome_transform=Standardize(m=1)
    #             )
    #         )
    #     model = ModelListGP(*models)
    #     mll = SumMarginalLogLikelihood(model.likelihood, model)
    #     return mll, model

