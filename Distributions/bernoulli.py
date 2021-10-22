from Distributions.base import Distribution
import numpy as np

class Bernoulli(Distribution):
    def __init__(self, arguments=[], name="Bernoulli"):
        """ 
        arguments should be a list of p values for the bernoulli distribution
        like this [0.2, 0.5, 0.2]
        """
        self.arguments = arguments
        self.name = name

        self.process_count = len(np.unique(self.arguments))
        self.count = len(self.arguments) - 1


    def randomly_create_arguments(self, count, min_distance_between_means=0.1):
        self.count = count

        self.arguments = []
        self.arguments.append(np.random.random())
        while len(self.arguments) < count + 1:

            new_p = np.random.random()
            if abs(self.arguments[len(self.arguments) - 1] - new_p) >= min_distance_between_means:
                self.arguments.append(new_p)

    def get_parameter_string(self):
        return f"p: {' '.join(map(str, self.arguments))}"

    def get_distribution(self, length):
        self.sequence = []

        for i in range(self.count + 1):
            segment_length = self.get_intra_distance(i, length)

            self.sequence.append(np.random.binomial(1, self.arguments[i], segment_length))
        self.sequence = np.concatenate(self.sequence)
