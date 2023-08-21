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

try:
    goodSolutions = (formData['good-solutions'].value).split(',')
except:
    pass
try:
    badSolutions = (formData['bad-solutions'].value).split(',')
except:
    badSolutions = []
try:
    currentSolutions = (formData['current-solutions'].value).split(',')
except:
    currentSolutions = []
try:
    objectivesInput = (formData['objectives-input'].value).split(',')
except:
    objectivesInput = []

newSolution = (formData['new-solution'].value).split(',')
nextEvaluation = (formData['next-evaluation'].value).split(',')
refineSolution = (formData['refine-solution'].value).split(',')

try:
    solutionName = (formData['solution-name'].value).split(',')
except:
    pass
try: 
    obj1 = float((formData['objective-1'].value))
except:
    pass
try:
    obj2 = float((formData['objective-2'].value))
except:
    pass


num_parameters = len(parameterNames)
parameter_bounds = torch.zeros(2, num_parameters)
parameter_bounds_normalised = torch.zeros(2, num_parameters)
parameter_bounds_range = []
for i in range(num_parameters):
    parameter_bounds[0][i] = float(parameterBounds[2*i])
    parameter_bounds[1][i] = float(parameterBounds[2*i + 1])
    parameter_bounds_normalised[0][i] = float(0)
    parameter_bounds_normalised[1][i] = float(1)
    parameter_bounds_range.append(float(parameterBounds[2*i + 1]) - float(parameterBounds[2*i]))

bad_solutions = []
for i in range(int(len(badSolutions)/num_parameters)):
    bad_solutions.append(badSolutions[i*num_parameters:i*num_parameters+num_parameters])

obj_ref_point = torch.tensor([-1., -1.])
objective_bounds = torch.zeros(2, 2)
for i in range(2):
    objective_bounds[0][i] = float(objectiveBounds[2*i])
    objective_bounds[1][i] = float(objectiveBounds[2*i + 1])

def unnormalise_parameters(x_tensor):
    x_bounds = parameter_bounds
    x_actual = torch.zeros(1, num_parameters)
    for i in range(num_parameters):
        x_actual[0][i] = x_tensor[0][i]*(x_bounds[1][i] - x_bounds[0][i]) + x_bounds[0][i]
    return x_actual

def normalise_parameters(x_tensor):
    x_bounds = parameter_bounds
    x_norm = torch.zeros(x_tensor.size(), dtype=torch.float64)
    for j in range(x_tensor.size()[0]): # TESTING INDEX ERROR
        for i in range(x_tensor.size()[1]):
            x_norm[j][i] = (x_tensor[j][i] - x_bounds[0][i])/(x_bounds[1][i] - x_bounds[0][i]) 
    return x_norm

def normalise_objectives(obj_tensor_actual):
    objectives_min_max = objectiveMinMax
    obj_tensor_norm = torch.zeros(obj_tensor_actual.size(), dtype=torch.float64)
    for j in range(obj_tensor_actual.size()[0]):
        for i in range (obj_tensor_actual.size()[1]):
            if (objectives_min_max[i] == "minimise"): # MINIMISE (SMALLER VALUES CLOSER TO 1)
                obj_tensor_norm[j][i] = -2*((obj_tensor_actual[0][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) + 1
            elif (objectives_min_max[i] == "maximise"): # MAXIMISE (LARGER VALUES CLOSER TO -1)
                obj_tensor_norm[j][i] =  2*((obj_tensor_actual[0][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) - 1
    return obj_tensor_norm

def checkForbiddenRegions(bad_solutions, proposed_solution): # +/- 5% of bad solution parameters  
  for i in range(len(bad_solutions)):
    # print(proposed_solution[0][1])
    # print(bad_solutions[i][0])
    if (proposed_solution[0][0] < float(bad_solutions[i][0])+parameter_bounds_range[0]*0.05 and proposed_solution[0][0] > float(bad_solutions[i][0])-parameter_bounds_range[0]*0.05 and proposed_solution[0][1] < float(bad_solutions[i][1])+parameter_bounds_range[1]*0.05 and proposed_solution[0][1] > float(bad_solutions[i][1])-parameter_bounds_range[1]*0.05):
      return False
    # if (proposed_solution[0][0] < float(bad_solutions[i][0])*1.05 and proposed_solution[0][0] > float(bad_solutions[i][0])*0.95 and proposed_solution[0][1] < float(bad_solutions[i][1])*1.05 and proposed_solution[0][1] > float(bad_solutions[i][1])*0.95):
    #   return False
  return True

# generate training data
def generate_initial_data(n_samples=1):
    # generate training data
    train_x = draw_sobol_samples(
        bounds=parameter_bounds_normalised, n=1, q=n_samples, seed=torch.randint(1000000, (1,)).item()
    ).squeeze(0)
    train_x = train_x.type(torch.DoubleTensor)
    train_x_actual = torch.round(unnormalise_parameters(train_x))
    # print("Initial solution: ", train_x_actual)
    if (badSolutions != []):
        while (checkForbiddenRegions(bad_solutions, train_x_actual) == False):
            # print("Proposed solution in forbidden region")
            train_x = draw_sobol_samples(
                bounds=problem_bounds, n=1, q=n_samples, seed=torch.randint(1000000, (1,)).item()
            ).squeeze(0)
            train_x = train_x.type(torch.DoubleTensor)
            train_x_actual = unnormalise_parameters(train_x)
            # train_x_actual_placeholder = []
            # for i in range(num_parameters):
            #     train_x_actual_placeholder.append(np.random.randint(float(parameterBounds[2*i]), float(parameterBounds[2*i+1])))
            # train_x_actual = torch.tensor([train_x_actual_placeholder], dtype=torch.float64)
            # train_x = normalise_parameters(train_x_actual)
            # print("Initial solution: ", train_x_actual)
        # train_obj_actual, train_obj = objective_function(train_x_actual)

    return train_x, train_x_actual

def initialize_model(train_x, train_obj):
    # define models for objective and constraint
    model = SingleTaskGP(train_x, train_obj, outcome_transform=Standardize(m=train_obj.shape[-1]))
    mll = ExactMarginalLogLikelihood(model.likelihood, model)
    return mll, model

def optimize_qehvi(model, train_obj, sampler):
    """Optimizes the qEHVI acquisition function, and returns a new candidate and observation."""
    # partition non-dominated space into disjoint rectangles
    partitioning = NondominatedPartitioning(ref_point=obj_ref_point, Y=train_obj)
    acq_func = qExpectedHypervolumeImprovement(
        model=model,
        ref_point=obj_ref_point.tolist(),  # use known reference point
        partitioning=partitioning,
        sampler=sampler,
    )
    # optimize
    candidates, _ = optimize_acqf(
        acq_function=acq_func,
        bounds=parameter_bounds_normalised,
        q=BATCH_SIZE,
        num_restarts=NUM_RESTARTS,
        raw_samples=RAW_SAMPLES,  # used for intialization heuristic
        options={"batch_limit": 5, "maxiter": 200, "nonnegative": True},
        sequential=True,
    )
    # observe new values
    new_x =  unnormalize(candidates.detach(), bounds=parameter_bounds_normalised)
    new_x_actual = unnormalise_parameters(new_x)
    if (badSolutions != []):
        while (checkForbiddenRegions(bad_solutions, new_x_actual) == False):
            # print("Solution proposed within forbidden region")
            # new_x =  unnormalize(candidates.detach(), bounds=problem_bounds)
            # new_x_actual = unnormalise_parameters(new_x)
            # new_x, new_x_actual = generate_initial_data()
            new_x_actual = torch.tensor([[np.random.randint(float(parameterBounds[0]), float(parameterBounds[1])), np.random.randint(float(parameterBounds[2]), float(parameterBounds[3]))]])
            new_x = normalise_objectives(new_x_actual)
            # print("Next solution: ", new_x_actual)
    return new_x, new_x_actual

if (newSolution[0]=="true"):
    bad_solutions.append(currentSolutions[-1*num_parameters:])
    currentSolutions = []
    train_x, train_x_actual = generate_initial_data()
    currentSolutions.append(train_x_actual.tolist()[0])
    reply = {}
    reply['solution'] = currentSolutions
    # reply['newSolution'] = newSolution
    reply['objectives'] = objectivesInput
    reply['bad_solutions'] = bad_solutions

if (nextEvaluation[0] == "true"):
    for i in range(len(currentSolutions)):
        currentSolutions[i] = float(currentSolutions[i])

    # train_obj_actual = torch.tensor([[obj1, obj2]], dtype=torch.float64)
    if (len(objectivesInput) != 0):
        objectivesInputPlaceholder = []
        for i in range(int(len(objectivesInput)/2)):
            objectivesInputPlaceholder.append([float(objectivesInput[2*i]), float(objectivesInput[2*i+1])])
        objectivesInput = objectivesInputPlaceholder
    objectivesInput.append([obj1, obj2])
    train_obj_actual = torch.tensor(objectivesInput, dtype=torch.float64)
    train_obj = normalise_objectives(train_obj_actual)
   
    parametersPlaceholder = []
    for i in range(int(len(currentSolutions)/num_parameters)):
        parametersPlaceholder.append(currentSolutions[i*num_parameters:i*num_parameters+num_parameters])
    train_x_actual = torch.tensor(parametersPlaceholder, dtype=torch.float64)
    # train_x_actual = torch.zeros(1,num_parameters, dtype=torch.float64)
    # for i in range(1, num_parameters+1):
    #     train_x_actual[0][-1*i] = float(currentSolutions[-1*i])
    train_x = normalise_parameters(train_x_actual)

    torch.manual_seed(SEED)

    hv = Hypervolume(ref_point=obj_ref_point)
    # Hypervolumes
    hvs_qehvi = []
    # Initialize GP models
    mll, model = initialize_model(train_x, train_obj)
    # Compute Pareto front and hypervolume
    pareto_mask = is_non_dominated(train_obj)
    pareto_y = train_obj[pareto_mask]
    volume = hv.compute(pareto_y)
    hvs_qehvi.append(volume)
    
    # Fit Models
    fit_gpytorch_model(mll)
    # Define qEI acquisition modules using QMC sampler
    qehvi_sampler = SobolQMCNormalSampler(num_samples=MC_SAMPLES)
    # Optimize acquisition functions and get new observations
    new_x, new_x_actual = optimize_qehvi(model, train_obj, qehvi_sampler)
    new_x_actual = torch.round(new_x_actual)
    
    # Update training points
    train_x = torch.cat([train_x, new_x])
    train_x_actual = torch.cat([train_x_actual, new_x_actual])
    # train_obj = torch.cat([train_obj, new_obj])
    # train_obj_actual = torch.cat([train_obj_actual, new_obj_actual])
    
    currentSolutions.append(train_x_actual.tolist()[-1])
    reply = {}
    reply['solution'] = currentSolutions
    reply['objectives'] = objectivesInput
    reply['solution_normalised'] = train_x.tolist()
    reply['bad_solutions'] = bad_solutions

def mobo_execute(seed, iterations, initial_samples):
    torch.manual_seed(seed)

    hv = Hypervolume(ref_point=obj_ref_point)
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