from itertools import permutations, combinations
import numpy as np


class ErrorComputer:
    def compute_error(self, changepoints, estimates):
        output = []

        changepoints = np.array(changepoints)
        estimates = np.array(estimates)

        for i in range(1, len(changepoints) + 1):
            if len(estimates) >= i:
                output.append(self.get_smallest_error(changepoints, estimates, i) / i)
            else:
                output.append(-1) 

        return output

    def get_smallest_error(self, changepoints, estimates, subset_size):
        estimate_combinations = list(combinations(estimates, subset_size))

        smallest_error = np.inf
        for combination in estimate_combinations:

            error = self.combination_error(changepoints, combination)
            if smallest_error > error:
                smallest_error = error

        return smallest_error


    def combination_error(self, changepoints, estimates):
        permutations_array = permutations(range(len(changepoints)))

        smallest_error = np.inf
        for permutation in permutations_array:

            error = self.permutation_error(changepoints, estimates, permutation)
            if smallest_error > error:
                smallest_error = error

        return smallest_error

    
    def permutation_error(self, changepoints, estimates, permutation):
        permutation = np.array(permutation)
        error = np.sum(np.abs(changepoints[permutation][:len(estimates)] - estimates))

        return error
