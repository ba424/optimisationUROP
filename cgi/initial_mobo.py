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
    savedSolutions = (formData['saved-solutions'].value).split(',')
except:
    savedSolutions = []
try:
    savedObjectives = (formData['saved-objectives'].value).split(',')
except:
    savedObjectives = []
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

def unnormalise_parameters(x_tensor, x_bounds = parameter_bounds):
    x_actual = torch.zeros(1, num_parameters)
    for i in range(num_parameters):
        x_actual[0][i] = x_tensor[0][i]*(x_bounds[1][i] - x_bounds[0][i]) + x_bounds[0][i]
    return x_actual

def normalise_parameters(x_tensor, x_bounds = parameter_bounds):
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
                obj_tensor_norm[j][i] = -2*((obj_tensor_actual[j][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) + 1
            elif (objectives_min_max[i] == "maximise"): # MAXIMISE (LARGER VALUES CLOSER TO -1)
                obj_tensor_norm[j][i] =  2*((obj_tensor_actual[j][i] - objective_bounds[0][i])/(objective_bounds[1][i] - objective_bounds[0][i])) - 1
    return obj_tensor_norm

def checkForbiddenRegions(bad_solutions, proposed_solution): # +/- 5% of bad solution parameters  
  for i in range(int(len(badSolutions)/num_parameters)):
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
    return train_x, train_x_actual

def initialize_model(train_x, train_obj):
    # define models for objective and constraint
    model = SingleTaskGP(train_x, train_obj, outcome_transform=Standardize(m=train_obj.shape[-1]))
    mll = ExactMarginalLogLikelihood(model.likelihood, model)
    return mll, model

def optimize_qehvi(model, train_obj, sampler, parameter_bounds=parameter_bounds):
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
    new_x_actual = unnormalise_parameters(new_x, parameter_bounds)

    if (badSolutions != []):
        while (checkForbiddenRegions(bad_solutions, new_x_actual) == False):
            new_x_actual = torch.tensor([[np.random.randint(parameter_bounds[0][0], parameter_bounds[1][0]), np.random.randint(parameter_bounds[0][1], parameter_bounds[1][1])]])
            new_x = normalise_objectives(new_x_actual)
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
    reply['saved_solutions'] = savedSolutions
    reply['saved_objectives'] = savedObjectives

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
    savedObjectives.append([obj1, obj2])
    train_obj_actual = torch.tensor(objectivesInput, dtype=torch.float64)
    train_obj = normalise_objectives(train_obj_actual)
   
    parametersPlaceholder = []
    for i in range(int(len(currentSolutions)/num_parameters)):
        parametersPlaceholder.append(currentSolutions[i*num_parameters:i*num_parameters+num_parameters])
    train_x_actual = torch.tensor(parametersPlaceholder, dtype=torch.float64)
    savedSolutions.append(train_x_actual.tolist()[-1])
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
    #savedSolutions.append(train_x_actual.tolist()[-1])
    reply = {}
    reply['solution'] = currentSolutions
    reply['objectives'] = objectivesInput
    reply['solution_normalised'] = train_x.tolist()
    reply['bad_solutions'] = bad_solutions
    reply['saved_solutions'] = savedSolutions
    reply['saved_objectives'] = savedObjectives


if (refineSolution[0] == "true"):
    for i in range(len(currentSolutions)):
        currentSolutions[i] = float(currentSolutions[i])

    # train_obj_actual = torch.tensor([[obj1, obj2]], dtype=torch.float64)
    if (len(objectivesInput) != 0):
        objectivesInputPlaceholder = []
        for i in range(int(len(objectivesInput)/2)):
            objectivesInputPlaceholder.append([float(objectivesInput[2*i]), float(objectivesInput[2*i+1])])
        objectivesInput = objectivesInputPlaceholder
    objectivesInput.append([obj1, obj2])
    savedObjectives.append([obj1, obj2])
    train_obj_actual = torch.tensor(objectivesInput, dtype=torch.float64)
    train_obj = normalise_objectives(train_obj_actual)
   
    parametersPlaceholder = []
    for i in range(int(len(currentSolutions)/num_parameters)):
        parametersPlaceholder.append(currentSolutions[i*num_parameters:i*num_parameters+num_parameters])
    train_x_actual = torch.tensor(parametersPlaceholder, dtype=torch.float64)
    savedSolutions.append(train_x_actual.tolist()[-1])
    
    # train_x_actual = torch.zeros(1,num_parameters, dtype=torch.float64)
    # for i in range(1, num_parameters+1):
    #   train_x_actual[0][-1*i] = float(currentSolutions[-1*i])
    parameter_bounds_refined = torch.zeros(2, num_parameters)
    parameter_bounds_range_refined = []
    for i in range(num_parameters):
        parameter_bounds_refined[0][i] = currentSolutions[len(currentSolutions)-num_parameters+i] - parameter_bounds_range[i]*0.05
        if (parameter_bounds_refined[0][i] < parameter_bounds[0][i]):
            parameter_bounds_refined[0][i] = parameter_bounds[0][i]
        parameter_bounds_refined[1][i] = currentSolutions[len(currentSolutions)-num_parameters+i] + parameter_bounds_range[i]*0.05
        if (parameter_bounds_refined[1][i] > parameter_bounds[1][i]):
            parameter_bounds_refined[1][i] = parameter_bounds[1][i]
        parameter_bounds_range_refined.append(parameter_bounds_refined[1][i] - parameter_bounds_refined[0][i])
    
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
    new_x, new_x_actual = optimize_qehvi(model, train_obj, qehvi_sampler, parameter_bounds_refined)
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
    reply['saved_solutions'] = savedSolutions
    reply['saved_objectives'] = savedObjectives


reply['success'] = True
reply['message'] = message

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

sys.stdout.write(json.dumps(reply,indent=1))
sys.stdout.write("\n")

sys.stdout.close()