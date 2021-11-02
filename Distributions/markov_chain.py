from Distributions.base import Distribution
import numpy as np


class MarkovChain(Distribution):
    name = "MarkovChain"

    def __init__(self, nodes, order, arguments=[]):
        """
        Each argument should be an array of vectors. Each vector holds the probability to go to the ith node in the ith positions
        and which vector is choosen to find the next nodes depends on the history. Each vector should sum to 1.
        The exact way to determine which vector is choosen can be found by examining the get_position_from_history function.
        N different arguments in an array make up the arguments
        
        This is an example for a single element of the argument array with order 2 and 3 nodes,
        [[0.2, 0, 0.8], [0.3, 0.3, 0.4], [0.2, 0.1, 0.7], [0.1, 0.1, 0.8], [0.1, 0.1, 0.8],
        [0.1, 0.1, 0.8], [0, 0, 1], [1, 0, 0], [0.2, 0, 0.8]]
        """


        self.nodes = nodes
        self.order = order
        self.name = f"MarkovChain_order_{self.order}_with_{self.nodes}_nodes"
        self.arguments = arguments

        self.count = len(arguments) - 1
        self.process_count = len(np.unique(self.arguments, axis=0))

    def randomly_create_arguments(self, count):
        self.arguments = []
        while len(self.arguments) < count + 1:

            buffer = []
            for i in range(self.nodes ** self.order):
                chances = np.zeros(self.nodes)

                total = 0
                for j in range(self.nodes):
                    random_number = np.random.random()
                    total += random_number
                    chances[j] = random_number

                chances = chances / total
                buffer.append(chances)

            self.arguments.append(buffer)
        
        self.count = count
        self.process_count = len(np.unique(self.arguments, axis=0))


    def create_argument_string(self):
        output = str(self.arguments)

        output = output.replace("array", "")
        output = output.replace("(", "")
        output = output.replace(")", "")

        return f"MarkovChain_order_{self.order}_with_{self.nodes}_nodes = {output}"


    def get_kronecker(self, x, degree):
        output = x
        for i in range(degree - 1):
            output = np.outer(output, x).flatten()

        return output

    def get_initial_probabilities(self, markov_matrix):
        transition_probabilities = np.array(markov_matrix)
        initial = np.ones(self.nodes) / self.nodes
        last = np.zeros(self.nodes)

        while np.linalg.norm(initial - last) > 1e-8:
            last = initial
            initial = transition_probabilities.T @ self.get_kronecker(initial, self.order)
        
        return initial

    def get_parameter_string(self):
        return self.name

    def get_position_from_history(self, history):
        position = 0
        for i in range(len(history)):
            position += history[len(history) - i - 1] * (self.nodes ** i)

        return position

    def get_sample(self, length, markov_matrix):
        output = np.zeros(length, dtype=np.int32)

        probabilities = self.get_initial_probabilities(markov_matrix)
        output[0:self.order] = np.random.choice(self.nodes, p=probabilities)

        for i in range(self.order, length):
            random_number = np.random.random()

            total = 0
            chances = markov_matrix[self.get_position_from_history(output[i - self.order:i])]
            for j in range(self.nodes):
                total += chances[j]

                if random_number < total:
                    output[i] = j
                    break

        return output

    def get_distribution(self, length):
        self.sequence = []

        for i in range(self.count + 1):
            segment_length = self.get_intra_distance(i, length)

            self.sequence.append(self.get_sample(segment_length, self.arguments[i]))

        self.sequence = np.concatenate(self.sequence)
