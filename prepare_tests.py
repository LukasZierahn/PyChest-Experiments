import sys

from Distributions.bernoulli import Bernoulli
from Distributions.rotary import Rotary
from Distributions.markov_chain import MarkovChain
from Distributions.hidden import Hidden

import os
import shutil
import Distributions.markov_arguments as markov_arguments
import numpy as np


if __name__ == "__main__":
    min_distance_between_changepoints = 0.28

    step_size = int(sys.argv[3])
    start_length = int(sys.argv[1])
    end_length = int(sys.argv[2]) + step_size
    total_steps = (end_length - start_length) // step_size

    iterations = int(sys.argv[4])
    
    distributions = []

    # Bernoulli Figure 3
    # distributions += [Bernoulli([0.8, 0.5])]

    # Hidden Irrational Rotation Figure 3
    # distributions += [Hidden(Rotary([0.452341643253462432, 0.6345354645623456234234]))]

    # Irrational Rotation and Bernoulli Table 1
    distributions += [Rotary([0.452341643253462432, 0.6345354645623456234234, 0.452341643253462432])]
    distributions += [Bernoulli([0.8, 0.5, 0.8])]
    
    print("Steps: ", start_length, end_length, step_size, "min distance", min_distance_between_changepoints, "Distributions: ", [dist.name for dist in distributions])

    if os.path.exists("sequences"):
        shutil.rmtree("sequences")

    error_log = open("error_log.csv", "w")
    error_log.write("Iteration,Distribution,Algorithm,Length,Actual_Length,Count,Changepoints_abs,Changepoints_rel,Estimates,Error,time_used\n")
    error_log.close()

    os.mkdir("sequences")
    info = open("sequences/info.txt", "w")
    info.write(f"Steps: {start_length} {end_length} {step_size}, Iterations: {iterations}, Distributions: {[dist.name for dist in distributions]}")
    info.close()

    for distribution_index, dist in enumerate(distributions):
        os.mkdir(f"sequences/{dist.name}")
        np.random.seed(int(sys.argv[5]) + distribution_index)
        dist.prepare_distribution(min_distance_between_changepoints)

        for iteration in range(iterations):
            np.random.seed(int(sys.argv[5]) + iteration + len(distributions))
            print(f"iteration: {iteration}, seed: {int(sys.argv[5]) + iteration}, changepoints: {dist.changepoints}")

            os.mkdir(f"sequences/{dist.name}/{iteration}")

            for _, length in enumerate(range(start_length, end_length, step_size)):
                os.mkdir(f"sequences/{dist.name}/{iteration}/{length}")
                open(f"sequences/{dist.name}/{iteration}/{length}/algorithms.csv", "w")

                dist.get_distribution(length)
                print("Length:", len(dist.sequence))

                np.savetxt(f"sequences/{dist.name}/{iteration}/{length}/data.csv", dist.sequence, delimiter=',')
                np.savetxt(f"sequences/{dist.name}/{iteration}/{length}/changepoints.csv", dist.changepoints, delimiter=',')
                np.savetxt(f"sequences/{dist.name}/{iteration}/{length}/min_distance.csv", [dist.min_distance], delimiter=',')
                np.savetxt(f"sequences/{dist.name}/{iteration}/{length}/process_count.csv", [dist.process_count], delimiter=',')
