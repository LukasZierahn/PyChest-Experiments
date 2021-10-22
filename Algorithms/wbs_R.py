from Algorithms.base import Algorithm
import numpy as np

class WbsR(Algorithm):
    name = "WbsR"

    def __init__(self, R_connection):
        self.R_connection = R_connection
        self.R_connection.eval("library(wbs)")

    def estimate(self, dist):
        self.start_timer()

        estimates = self.R_connection.eval(f"changepoints(wbs(c({','.join(map(str, dist.sequence))})), Kmax={2*dist.count}, penalty='ssic.penalty')$cpt.ic$ssic.penalty", atomicArray=True)
        #estimates = self.R_connection.eval(f"changepoints(wbs(c({','.join(map(str, dist.sequence))})), Kmax={dist.count}, penalty='bic.penalty')$cpt.ic$bic.penalty", atomicArray=True)
        if not isinstance(estimates[0], np.float64):
            estimates = []
        self.guess(dist.changepoints, estimates)
