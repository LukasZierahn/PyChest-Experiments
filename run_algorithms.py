from error_computer import ErrorComputer

from Algorithms.base import prepare_R, shutdown_R

from Algorithms.find_changepoints import FindChangepoints
from Algorithms.list_estimator import ListEstimator
from Algorithms.pelt import Pelt
from Algorithms.wbs_R import WbsR

import os
import numpy as np


class DistributionStruct:
    sequence = []
    changepoints = []
    count = 0
    min_distance = 0.0


if __name__ == "__main__":
    error_log = open("error_log.csv", "a")

    errorComputer = ErrorComputer()

    R_connection = prepare_R()
    algorithms = [FindChangepoints(), WbsR(R_connection)]

    distributions = os.listdir("sequences")
    distributions.sort()
    iterations = os.listdir(f"sequences/{distributions[0]}")
    iterations.sort()

    for iteration in iterations:

        for algorithm in algorithms:
            for dist_name in distributions:
                if dist_name == "info.txt":
                    continue

                lengths = os.listdir(f"sequences/{dist_name}/{iteration}")
                for length in lengths:

                    already_visited = open(f"sequences/{dist_name}/{iteration}/{length}/algorithms.csv", "r").read().split("\n")
                    if algorithm.name in already_visited:
                        print(f"Already Visited: {iteration} {algorithm.name} {dist_name} {length}")
                        continue

                    print(f"Computing: {iteration} {algorithm.name} {dist_name} {length}")
                    distribution = DistributionStruct()
                    distribution.sequence = np.genfromtxt(f"sequences/{dist_name}/{iteration}/{length}/data.csv")
                    distribution.changepoints = np.genfromtxt(f"sequences/{dist_name}/{iteration}/{length}/changepoints.csv")

                    if distribution.changepoints.size == 1:
                        distribution.changepoints = np.array([distribution.changepoints])

                    distribution.count = len(distribution.changepoints)
                    distribution.min_distance = np.genfromtxt(f"sequences/{dist_name}/{iteration}/{length}/min_distance.csv")
                    distribution.process_count = np.genfromtxt(f"sequences/{dist_name}/{iteration}/{length}/process_count.csv")

                    algorithm.estimate(distribution)
                    error = errorComputer.compute_error(distribution.changepoints * int(length), algorithm.estimates)

                    error_log.write(f"{iteration},{dist_name},{algorithm.name},{length},{len(distribution.sequence)},{len(algorithm.estimates)},")
                    error_log.write(f"{'|'.join(map(str, distribution.changepoints))},{'|'.join(map(str, [j * int(length) for j in distribution.changepoints]))},{'|'.join(map(str, algorithm.estimates))},{'|'.join(map(str, error))},{algorithm.time_used}\n")
                    error_log.flush()

                    already_visited = np.append(already_visited, [algorithm.name])
                    algorithms_out = open(f"sequences/{dist_name}/{iteration}/{length}/algorithms.csv", "w")
                    for alg in already_visited:
                        algorithms_out.write(alg + "\n")

    error_log.close()
    shutdown_R()
