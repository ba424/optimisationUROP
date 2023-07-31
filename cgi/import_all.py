#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe
#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\python.exe

import sys
import json
import cgi
import numpy as np
import sqlite3
import os

import torch
#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe
os.environ['HOME'] = 'C:/Users/user/AppData/Local/Microsoft/WindowsApps/python.exe'

# Initialize the basic reply message
message = "Necessary objects imported."
success = True

# Read provided formData
formData = cgi.FieldStorage()
reply = {}
reply['success'] = True
reply['message'] = message

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

sys.stdout.write(json.dumps(reply,indent=1))
sys.stdout.write("\n")

sys.stdout.close()

import numpy as np
# import torch
# import os
# from botorch.test_functions.multi_objective import BraninCurrin
# from botorch.models.gp_regression import SingleTaskGP
# from botorch.models.transforms.outcome import Standardize
# from gpytorch.mlls.exact_marginal_log_likelihood import ExactMarginalLogLikelihood
# from botorch.utils.transforms import unnormalize
# from botorch.utils.sampling import draw_sobol_samples
# from botorch.optim.optimize import optimize_acqf, optimize_acqf_list
# from botorch.acquisition.objective import GenericMCObjective
# from botorch.utils.multi_objective.scalarization import get_chebyshev_scalarization
# from botorch.utils.multi_objective.box_decompositions.non_dominated import NondominatedPartitioning
# from botorch.acquisition.multi_objective.monte_carlo import qExpectedHypervolumeImprovement
# from botorch.utils.sampling import sample_simplex
# from botorch import fit_gpytorch_model
# from botorch.acquisition.monte_carlo import qExpectedImprovement, qNoisyExpectedImprovement
# # from botorch.sampling.samplers import SobolQMCNormalSampler
# from botorch.exceptions import BadInitialCandidatesWarning
# from botorch.utils.multi_objective.pareto import is_non_dominated
# from botorch.utils.multi_objective.hypervolume import Hypervolume

# tkwargs = {
#     "dtype": torch.double,
#     #"device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
#     "device": torch.device("cuda"),
# }

# Global Variables 

BATCH_SIZE = 1 # Number of design parameter points to query at next iteration
NUM_RESTARTS = 10 # Used for the acquisition function number of restarts in optimization
RAW_SAMPLES = 1024 # Initial restart location candidates
N_ITERATIONS = 35 # Number of optimization iterations
MC_SAMPLES = 512 # Number of samples to approximate acquisition function
N_INITIAL = 5
SEED = 2 # Seed to initialize the initial samples obtained