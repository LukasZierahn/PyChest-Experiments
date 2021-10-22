from Distributions.base import Distribution
import numpy as np

class Normal(Distribution):
    name = "Normal"

    def __init__(self, arguments=[]):
        """
        arguments should be a list of averages and std deviation for the normal distribution
        like this [[0, 1], [2, 0.1], [0, 1]]
        """

        self.arguments = arguments
        self.count = len(arguments) - 1
        self.process_count = len(np.unique(self.arguments, axis=0))

    def randomly_create_arguments(self, count):
        self.count = count

        self.arguments = []
        while len(self.arguments) < count + 1:
            self.arguments.append([np.random.random(), np.random.random()])

    def get_parameter_string(self):
        output = ""

        for i in range(self.count + 1):
            output += f"Segment: {i} average: {self.arguments[i][0]} scale: {self.arguments[i][1]}, "

        return output

    def get_distribution(self, length):
        self.sequence = []

        for i in range(self.count + 1):
            segment_length = self.get_intra_distance(i, length)

            self.sequence.append(np.random.normal(self.arguments[i][0], self.arguments[i][1], segment_length))
        self.sequence = np.concatenate(self.sequence)
