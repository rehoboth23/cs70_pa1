# generic problem type that can be applied to search problems.I used this for type safe coding
class SearchProblem:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def get_successors(self, state):
        pass

    def valid_state(self, state):
        pass

    def check_goal(self, state):
        pass


class FoxProblem(SearchProblem):
    # I edited the constructor but my additions are optional so it should not affect how the constructor is used
    def __init__(self, start_state=(3, 3, 1), goal_state=(0, 0, 0), boat_capacity=2):
        super().__init__(start_state, goal_state)
        self.boat_capacity = boat_capacity

    # get successor states for the given state
    def get_successors(self, state):
        """
        :param state: state to generate successors for
        :return: if valid successor states for the input state
        """
        boat = state[2]
        # number of foxes on the bank that we are considering
        bf = state[0] if boat == 1 else self.start_state[0] - state[0]

        # number of chickens on the bank that we are considering
        bc = state[1] if boat == 1 else self.start_state[1] - state[1]

        # the successors will be the union of the two actions first with fixes as main target then chickens
        return self.generate_state(bf, bc, boat, 0).union(self.generate_state(bc, bf, boat, 1))

    # generate state is a helper method to generate possible next states within specific parameters
    def generate_state(self, target, other, boat, animal):
        """
        :param target: number of the specific animal on the given bank
        :param other: number of other animal on the given bank
        :param boat: helps to identify which bank the boat will be going to
        :param animal: differentiates between foxes and chickens.fox = 0, chicken = 1
        :return: possible next states limited by the given parameters

        consider all possibilities where an arbitrary number of the animal boards the boat as long as the number
        is less than the boat capacity
        then for all those possibilities consider the possibilities where an arbitrary number of the other animal  is
        used to fill up the boat
        """
        successors = set()  # set of successors
        for i in range(1, min(self.boat_capacity, target) + 1):
            if animal == 0:  # order of tuple will change depending on the animal being considered
                possible_state = (target - i, other, 0) if boat == 1 else \
                    (self.start_state[0] - target + i, self.start_state[1] - other, 1)
            else:
                possible_state = (other, target - i, 0) if boat == 1 else \
                    (self.start_state[0] - other, self.start_state[1] - target + i, 1)
            # if the boat is not full check for all the possible states where the other animal is used to fill the boat
            if i < min(self.boat_capacity, target):
                for x in range(1, min(self.boat_capacity - i, other) + 1):
                    if animal == 0:
                        possible_state2 = (possible_state[0], other - x, 0) if boat == 1 else \
                            (possible_state[0], self.start_state[1] - other + x, 1)
                    else:
                        possible_state2 = (other - x, possible_state[1], 0) if boat == 1 else \
                            (self.start_state[0] - other + x, possible_state[1], 1)
                    if self.valid_state(possible_state2):
                        successors.add(possible_state2)
            if self.valid_state(possible_state):
                successors.add(possible_state)
        return successors

    def valid_state(self, state):
        """
        :param state: check if state is valid for game
        :return: if state is valid for game
        """
        return (state[0] <= state[1] or state[1] == 0) and \
               (self.start_state[0] - state[0] <= self.start_state[1] - state[1] or self.start_state[1] == state[1])

    def check_goal(self, state):
        """
        :param state: state to compare against the goal state
        :return: if state is the same as the goal state
        """
        return state == self.goal_state

    def __str__(self):
        string = "Chickens and foxes problem: " + str(self.start_state)
        return string


# A bit of test code
if __name__ == "__main__":
    test_cp = FoxProblem((5, 5, 1))
    print(test_cp.get_successors((5, 5, 1)))
    print(test_cp)
