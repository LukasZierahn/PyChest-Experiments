from Distributions.base import Distribution
import numpy as np

class Rotary(Distribution):
    name = "Rotary"

    def __init__(self, arguments=[]):
        """
        arguments should be a list of alphas  for the rotary distribution
        like this [0.23890234802934, 0.234723894729384, 0.23890234802934]
        """
        self.arguments = arguments

        self.process_count = len(np.unique(self.arguments))
        self.count = len(arguments) - 1

    def randomly_create_arguments(self, count):
        self.arguments = []
        while len(self.arguments) < count + 1:
            self.arguments.append(np.random.random())

    def get_parameter_string(self):
        return f"alpha {' '.join(map(str, self.arguments))}"

    def get_sample(self, length, alpha):
        output = np.zeros(length)
        output[0] = np.random.random()

        for i in range(1, length):
            output[i] = (output[i - 1] + alpha) % 1

        # np.rint rounds to the closest integer, i. e. 0.5 gets rounded up to 1
        return np.rint(output)

    def get_distribution(self, length):
        self.sequence = []

        for i in range(self.count + 1):
            segment_length = self.get_intra_distance(i, length)

            self.sequence.append(self.get_sample(segment_length, self.arguments[i]))

        self.sequence = np.concatenate(self.sequence)

