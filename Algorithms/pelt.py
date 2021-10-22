
from Algorithms.base import Algorithm
import ruptures as rpt

class Pelt(Algorithm):
    name = "Pelt"

    def estimate(self, dist):
        self.start_timer()

        algo = rpt.Pelt(model="rbf", min_size=int(dist.min_distance * 0.75 * len(dist.sequence))).fit(dist.sequence)
        estimates = algo.predict(pen=3)
        self.guess(dist.changepoints, estimates)
