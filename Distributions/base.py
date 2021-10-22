import numpy as np

class Distribution:
    sequence = []
    changepoints = []

    min_distance = 0
    count = 0
    process_count = None

    name = ""

    def prepare_distribution(self, min_distance):
        self.changepoints = []
        self.min_distance = min_distance

        while len(self.changepoints) < self.count:
            self.changepoints = []
            for i in range(100):
                new_changepoint = np.random.random()

                # Check if new changepoint is sufficiently far away from the edges
                if new_changepoint < min_distance or (1 - new_changepoint) < min_distance:
                    continue

                too_close = False
                # Check if new changepoint is sufficiently far away from all other points
                for changepoint in self.changepoints:
                    if abs(changepoint - new_changepoint) < min_distance:
                        too_close = True
                        break

                if not too_close:
                    self.changepoints.append(new_changepoint)
                
                if not len(self.changepoints) < self.count:
                    break

        self.changepoints = sorted(self.changepoints)

    def get_intra_distance(self, i, length):
        if i == 0:
            return int(self.changepoints[0] * length)
        elif i == self.count:
            return int((1 - self.changepoints[self.count - 1]) * length)
        else:
            return int((self.changepoints[i] - self.changepoints[i - 1]) * length)

    def get_distribution(self, length):
        raise NotImplementedError

    def get_parameter_string(self):
        raise NotImplementedError

    def prepare_and_get_distribution(self, length, min_distance):
        self.prepare_distribution(min_distance)
        self.get_distribution(length)

