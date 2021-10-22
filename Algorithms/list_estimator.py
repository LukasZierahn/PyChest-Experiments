from Algorithms.base import Algorithm
import PyChest

class ListEstimator(Algorithm):
    name = "ListEstimator"

    def estimate(self, dist):
        self.start_timer()
        estimates = PyChest.list_estimator(dist.sequence, dist.min_distance * 0.75)[:dist.count]
        self.guess(dist.changepoints, estimates)
