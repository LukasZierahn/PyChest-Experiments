from Distributions.base import Distribution
import numpy as np

class Hidden(Distribution):
    name = "Hidden"

    def __init__(self, base_distribution, overlap=0.1):
        self.base_distribution = base_distribution
        self.count = base_distribution.count
        self.process_count = base_distribution.process_count

        self.name = f"Hidden_{base_distribution.name}_overlap_{overlap}"
        self.overlap = overlap

    def prepare_distribution(self, min_distance):
        self.base_distribution.prepare_distribution(min_distance)
        super().prepare_distribution(min_distance)

    def get_parameter_string(self):
        return f"Hidden: {self.overlap} Base: {self.base_distribution.get_parameter_string()}"

    def get_distribution(self, length):
        self.base_distribution.get_distribution(length)
        base_sequence = self.base_distribution.sequence
        self.sequence = []

        for element in base_sequence:
            noise = np.random.random()
            # The idea here is that we are drawing from a uniform(0,1) distribution and then add that noise to the base
            # If the overlap is 0, then the base will just be the element.
            # If the overlap is 0.1, then the element base relationship is as follows:
            # 0/0, 1/0.9, 2/1.8, 3/2.7, ...
            base = element - (self.overlap * element)

            self.sequence.append(base + noise)
