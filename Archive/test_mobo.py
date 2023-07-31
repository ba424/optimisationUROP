import os
import torch


tkwargs = {
    "dtype": torch.double,
    "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
}
SMOKE_TEST = os.environ.get("SMOKE_TEST")

from botorch.test_functions.multi_objective import BraninCurrin

problem = BraninCurrin(negate=True).to(**tkwargs)

from botorch.models.gp_regression import FixedNoiseGP
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.models.transforms.outcome import Standardize
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from botorch.utils.transforms import unnormalize, normalize
from botorch.utils.sampling import draw_sobol_samples

NOISE_SE = torch.tensor([15.19, 0.63], **tkwargs)

# PART 1: INITIALIZE

def generate_initial_data(n=6):
    # generate training data
    train_x = draw_sobol_samples(bounds=problem.bounds, n=n, q=1).squeeze(1)
    train_obj_true = problem(train_x)
    train_obj = train_obj_true + torch.randn_like(train_obj_true) * NOISE_SE
    return train_x, train_obj, train_obj_true


def initialize_model(train_x, train_obj):
    # define models for objective and constraint
    train_x = normalize(train_x, parameters)
    models = []
    for i in range(train_obj.shape[-1]):
        train_y = train_obj[..., i : i + 1]
        train_yvar = train_y
        models.append(
            FixedNoiseGP(
                train_x, train_y, train_yvar, outcome_transform=Standardize(m=1)
            )
        )
    model = ModelListGP(*models)
    mll = SumMarginalLogLikelihood(model.likelihood, model)
    return mll, model

# print(problem.bounds)
# print(generate_initial_data())

# train_x: intital random sample
parameters = torch.tensor([[500., 3., 0.], [3000., 14., 3.]])
# parameters = torch.tensor([[0., 0.], [1., 1.]])
print(parameters)
train_x = torch.round(draw_sobol_samples(bounds=parameters, n=1, q=1).squeeze(1))
print(train_x)

# Code to input data: will eventually use data inputted into web page

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

train_obj_1, train_obj_2 = 500, 5
train_obj = torch.tensor([[float(train_obj_1), float(train_obj_2)]])
print(train_obj)

mll, model = initialize_model(train_x, train_obj)
# print(mll, model)

# PART 2: ACQUISITION FUNCTION STAGE

from botorch.optim.optimize import optimize_acqf, optimize_acqf_list
from botorch.acquisition.objective import GenericMCObjective
from botorch.utils.multi_objective.scalarization import get_chebyshev_scalarization
from botorch.utils.multi_objective.box_decompositions.non_dominated import (
    FastNondominatedPartitioning,
)
from botorch.acquisition.multi_objective.monte_carlo import (
    qExpectedHypervolumeImprovement,
    qNoisyExpectedHypervolumeImprovement,
)
from botorch.utils.sampling import sample_simplex


BATCH_SIZE = 4
NUM_RESTARTS = 10 if not SMOKE_TEST else 2
RAW_SAMPLES = 512 if not SMOKE_TEST else 4

standard_bounds = torch.zeros(2, parameters.size(dim=1), **tkwargs)
standard_bounds[1] = 1


def optimize_qehvi_and_get_observation(model, train_x, train_obj, sampler):
    """Optimizes the qEHVI acquisition function, and returns a new candidate and observation."""
    # partition non-dominated space into disjoint rectangles
    with torch.no_grad():
        pred = model.posterior(normalize(train_x, parameters)).mean
    partitioning = FastNondominatedPartitioning(
        ref_point=parameters_ref_point,
        Y=pred,
    )
    acq_func = qExpectedHypervolumeImprovement(
        model=model,
        ref_point=parameters_ref_point,
        partitioning=partitioning,
        sampler=sampler,
    )
    # optimize
    candidates, _ = optimize_acqf(
        acq_function=acq_func,
        bounds=standard_bounds,
        q=BATCH_SIZE,
        num_restarts=NUM_RESTARTS,
        raw_samples=RAW_SAMPLES,  # used for intialization heuristic
        options={"batch_limit": 5, "maxiter": 200},
        sequential=True,
    )
    # observe new values
    new_x = unnormalize(candidates.detach(), bounds=parameters)
    new_obj_true = problem(new_x)
    new_obj = new_obj_true + torch.randn_like(new_obj_true) * NOISE_SE
    return new_x, new_obj, new_obj_true

print(parameters.size(dim=1))

# Reference point: slightly worse than the lower bound of objective values, where the lower bound is the minimum acceptable value of interest for each objective
parameters_ref_point = torch.tensor([100, 2], dtype=torch.float64)
print(parameters_ref_point)
print(problem.ref_point)