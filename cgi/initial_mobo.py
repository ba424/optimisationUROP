#! C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe
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

# Define function for checking that required parameters have been submitted
def checkFormData(data, expectedArgs):
    argsDefined = True
    for i in range(0,len(expectedArgs)):
        if expectedArgs[i] not in data:
            argsDefined = False
            break
    return argsDefined

# expectedArgs = ['parameter-names', 'parameter-bounds', 'objective-names', 'objective-bounds', 'objective-min-max', 'good-solutions', 'bad-solutions']
# formValuesDefined = checkFormData(formData, expectedArgs)

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

newSolution = (formData['new-solution'].value).split(',')
nextEvaluation = (formData['next-evaluation'].value).split(',')

if (nextEvaluation[0] == "true"):
    pass

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
    parameter_bounds[0][i] = float(parameterBounds[2*i])
    parameter_bounds[1][i] = float(parameterBounds[2*i + 1])

if (newSolution[0] == "true"):
    solutionsList = []

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
solutionsList.append(train_x_actual.tolist()[0])
reply = {}
reply['solution'] = solutionsList
reply['newSolution'] = newSolution

def initialize_model(train_x, train_obj):
    # define models for objective and constraint
    model = SingleTaskGP(train_x, train_obj, outcome_transform=Standardize(m=train_obj.shape[-1]))
    mll = ExactMarginalLogLikelihood(model.likelihood, model)
    return mll, model

def optimize_qehvi(model, train_obj, sampler):
    """Optimizes the qEHVI acquisition function, and returns a new candidate and observation."""
    # partition non-dominated space into disjoint rectangles
    partitioning = NondominatedPartitioning(ref_point=ref_point, Y=train_obj)
    acq_func = qExpectedHypervolumeImprovement(
        model=model,
        ref_point=ref_point.tolist(),  # use known reference point
        partitioning=partitioning,
        sampler=sampler,
    )
    # optimize
    candidates, _ = optimize_acqf(
        acq_function=acq_func,
        bounds=problem_bounds,
        q=BATCH_SIZE,
        num_restarts=NUM_RESTARTS,
        raw_samples=RAW_SAMPLES,  # used for intialization heuristic
        options={"batch_limit": 5, "maxiter": 200, "nonnegative": True},
        sequential=True,
    )
    # observe new values
    new_x =  unnormalize(candidates.detach(), bounds=problem_bounds)
    new_x_actual = unnormalise_parameters(new_x)
    print("Next solution: ", new_x_actual)
    new_obj, new_obj_actual = objective_function(new_x_actual)

    return new_x, new_x_actual, new_obj, new_obj_actual

def mobo_execute(seed, iterations, initial_samples):
    torch.manual_seed(seed)

    hv = Hypervolume(ref_point=ref_point)
    # Hypervolumes
    hvs_qehvi = []

    # Initial Samples
    # train_x_qehvi, train_obj_qehvi = load_data()
    train_x_qehvi, train_x_actual_qehvi, train_obj_qehvi, train_obj_actual_qehvi = generate_initial_data()

    # Initialize GP models
    mll_qehvi, model_qehvi = initialize_model(train_x_qehvi, train_obj_qehvi)

    # Compute Pareto front and hypervolume
    pareto_mask = is_non_dominated(train_obj_qehvi)
    pareto_y = train_obj_qehvi[pareto_mask]
    volume = hv.compute(pareto_y)
    hvs_qehvi.append(volume)
    # save_xy(train_x_qehvi, train_obj_qehvi, hvs_qehvi)

    # Go through the iterations

    for iteration in range(1, iterations + 1):
        # Fit Models
        fit_gpytorch_model(mll_qehvi)

        # Define qEI acquisition modules using QMC sampler
        qehvi_sampler = SobolQMCNormalSampler(num_samples=MC_SAMPLES)

        # Optimize acquisition functions and get new observations
        new_x_qehvi, new_x_actual_qehvi, new_obj_qehvi, new_obj_actual_qehvi = optimize_qehvi(model_qehvi, train_obj_qehvi, qehvi_sampler)
        # new_obj_qehvi = objective_function(new_x_qehvi[0])

        # Update training points
        train_x_qehvi = torch.cat([train_x_qehvi, new_x_qehvi])
        train_x_actual_qehvi = torch.cat([train_x_actual_qehvi, new_x_actual_qehvi])
        train_obj_qehvi = torch.cat([train_obj_qehvi, new_obj_qehvi])
        train_obj_actual_qehvi = torch.cat([train_obj_actual_qehvi, new_obj_actual_qehvi])

        # Compute hypervolumes
        pareto_mask = is_non_dominated(train_obj_qehvi)
        pareto_y = train_obj_qehvi[pareto_mask]
        volume = hv.compute(pareto_y)
        hvs_qehvi.append(volume)

        # save_xy(train_x_qehvi, train_obj_qehvi, hvs_qehvi)
        print("training x actual", train_x_actual_qehvi[-1])
        print("training x", train_x_qehvi[-1])
        print("training obj actual", train_obj_actual_qehvi[-1])
        print("training obj", train_obj_qehvi[-1])
        print("mask", pareto_mask)
        print("pareto y", pareto_y[-1])
        print("volume", volume)
        print("\n")
        mll_qehvi, model_qehvi = initialize_model(train_x_qehvi, train_obj_qehvi)

    return hvs_qehvi, train_x_qehvi, train_x_actual_qehvi, train_obj_qehvi, train_obj_actual_qehvi

# hvs_qehvi, train_x_qehvi, train_x_actual_qehvi, train_obj_qehvi, train_obj_actual_qehvi = mobo_execute(SEED, 35, 1)


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

