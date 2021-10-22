from Distributions.base import Distribution
import numpy as np

class MovingAverages(Distribution):
    name = "Hidden"

    def __init__(self, base_distribution, length_average=25):
        self.base_distribution = base_distribution
        self.count = base_distribution.count
        self.process_count = base_distribution.process_count

        self.name = f"Moving_Averages_{base_distribution.name}_over_{length_average}_elemts"
        self.length_average = length_average

    def prepare_distribution(self, min_distance):
        self.base_distribution.prepare_distribution(min_distance)
        super().prepare_distribution(min_distance)

    def get_parameter_string(self):
        return f"Hidden: {self.overlap} Base: {self.base_distribution.get_parameter_string()}"

    def get_distribution(self, length):
        self.base_distribution.get_distribution(length + self.length_average * len(self.changepoints))
        base_sequence = self.base_distribution.sequence

        self.sequence = []

        current_position = 0
        for i in range(self.count + 1):
            segment_length = self.get_intra_distance(i, len(base_sequence))
            
            self.sequence.append(np.convolve(base_sequence[current_position:current_position + segment_length], np.ones(self.length_average)/self.length_average, mode='valid'))

            current_position += segment_length

        self.sequence = np.concatenate(self.sequence)
