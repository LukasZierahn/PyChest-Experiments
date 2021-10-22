from Algorithms.base import Algorithm
import PyChest


class FindChangepoints(Algorithm):
    name = "FindChangepoints"

    def estimate(self, dist):
        self.start_timer()

        print("find_changepoints process count", dist.process_count)
        estimates = PyChest.find_changepoints(dist.sequence, dist.min_distance * 0.75, int(dist.process_count))
        self.guess(dist.changepoints, estimates)

