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

parameters = torch.tensor([[500., 3., 0.], [3000., 14., 3.]])
def generate_initial_data(n=1):
    # generate training data
    train_x = torch.round(draw_sobol_samples(bounds=parameters, n=n, q=1).squeeze(1))
    train_x = train_x.type(torch.DoubleTensor)
    print("\nSolution 0: ", train_x)

    while True:
        train_obj_1 = input("Enter Cost ($): ")
        try:
            train_obj_1 = float(train_obj_1)
            if (train_obj_1 >= 100 and train_obj_1 <= 1000):
                break
            else:
                raise ValueError
        except ValueError:
            print("Error. Please enter a valid measurement, within the objective bounds.")
    while True:
        train_obj_2 = input("Enter Travel Time (hrs): ")
        try:
            train_obj_2 = float(train_obj_2)
            if (train_obj_2 >= 2 and train_obj_2 <= 10):
                break
            else:
                raise ValueError
        except ValueError:
            print("Error. Please enter a valid measurement, within the objective bounds.")

    train_obj = torch.tensor([[float(train_obj_1), float(train_obj_2)]], dtype=torch.float64)
    return train_x, train_obj


def initialize_model(train_x, train_obj):
    # define models for objective and constraint
    train_x = normalize(train_x, parameters)
    models = []
    for i in range(train_obj.shape[-1]):
        train_y = train_obj[..., i : i + 1]
        train_yvar = torch.full_like(train_y, NOISE_SE[i] ** 2)
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

# PART 2: ACQUISITION FUNCTION STAGE; NEW POINTS

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


BATCH_SIZE = 1 # WAS 4
NUM_RESTARTS = 10 if not SMOKE_TEST else 2
RAW_SAMPLES = 512 if not SMOKE_TEST else 4

standard_bounds = torch.zeros(2, parameters.size(dim=1), **tkwargs)
standard_bounds[1] = 1

# parameters_ref_point = torch.tensor([[100, 2]])
parameters_ref_point = torch.tensor([99, 1], dtype=torch.float64)

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
    new_x = new_x.type(torch.DoubleTensor)
    # print("New x: ", new_x)
    print("\nNext Solution: ", new_x)

    while True:
        new_obj_1 = input("Enter Cost ($): ")
        try:
            new_obj_1 = float(new_obj_1)
            if (new_obj_1 >= 100 and new_obj_1 <= 1000):
                break
            else:
                raise ValueError
        except ValueError:
            print("Error. Please enter a valid measurement, within the objective bounds.")

    while True:
        new_obj_2 = input("Enter Travel Time (hrs): ")
        try:
            new_obj_2 = float(new_obj_2)
            if (new_obj_2 >= 2 and new_obj_2 <= 10):
                break
            else:
                raise ValueError
        except ValueError:
            print("Error. Please enter a valid measurement, within the objective bounds.")

    new_obj = torch.tensor([[float(new_obj_1), float(new_obj_2)]], dtype=torch.float64)

    return new_x, new_obj

# PART 3: OUTPUT RESULTS

import time
import warnings

from botorch import fit_gpytorch_mll
from botorch.exceptions import BadInitialCandidatesWarning
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.utils.multi_objective.box_decompositions.dominated import (
    DominatedPartitioning,
)
from botorch.utils.multi_objective.pareto import is_non_dominated


warnings.filterwarnings("ignore", category=BadInitialCandidatesWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

N_BATCH = 20 if not SMOKE_TEST else 10
MC_SAMPLES = 128 if not SMOKE_TEST else 16

verbose = True

hvs_qehvi = []

# call helper functions to generate initial training data and initialize model
train_x_qehvi, train_obj_qehvi = generate_initial_data(n=1)
mll_qehvi, model_qehvi = initialize_model(train_x_qehvi, train_obj_qehvi)

# compute hypervolume
bd = DominatedPartitioning(ref_point=parameters_ref_point, Y=train_obj_qehvi)
volume = bd.compute_hypervolume().item()

hvs_qehvi.append(volume)

# run N_BATCH rounds of BayesOpt after the initial random batch
for iteration in range(1, 3): # N_BATCH + 1

    t0 = time.monotonic()

    # fit the models
    fit_gpytorch_mll(mll_qehvi)

    # define the qEI and qNEI acquisition modules using a QMC sampler
    qehvi_sampler = SobolQMCNormalSampler(sample_shape=torch.Size([MC_SAMPLES]))

    # optimize acquisition functions and get new observations
    new_x_qehvi, new_obj_qehvi = optimize_qehvi_and_get_observation(model_qehvi, train_x_qehvi, train_obj_qehvi, qehvi_sampler)
    # update training points

    train_x_qehvi = torch.cat([train_x_qehvi, new_x_qehvi])
    train_obj_qehvi = torch.cat([train_obj_qehvi, new_obj_qehvi])
    # print(f"\nSolution {iteration}: ", train_x_qehvi[-1])
    # # update progress
    # for hvs_list, train_obj in zip(
    #     (hvs_qehvi),
    #     (
    #         train_obj_true_qehvi,
    #     ),
    # ):
        # compute hypervolume
    bd = DominatedPartitioning(ref_point=parameters_ref_point, Y=train_obj_qehvi)
    volume = bd.compute_hypervolume().item()
    print(volume)
    hvs_qehvi.append(volume)

    # reinitialize the models so they are ready for fitting on next iteration
    # Note: we find improved performance from not warm starting the model hyperparameters
    # using the hyperparameters from the previous iteration
    mll_qehvi, model_qehvi = initialize_model(train_x_qehvi, train_obj_qehvi)

    t1 = time.monotonic()

    if verbose:
        print(
            f"\nBatch {iteration:>2}: Hypervolume qEHVI = "
            f"({hvs_qehvi[-1]:>4.2f}), "
            f"time = {t1-t0:>4.2f}.",
            end="",
        )
    else:
        print(".", end="")