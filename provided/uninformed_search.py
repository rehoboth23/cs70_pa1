from collections import deque
from typing import Union

from SearchSolution import SearchSolution
from provided.FoxProblem import SearchProblem


# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes


class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self._parent = parent
        self._state = state

    @property
    def state(self):
        return self._state

    @property
    def parent(self):
        return self._parent


def make_node_add_fringe(fringe: deque, state, parent: SearchNode = None):
    fringe.append(SearchNode(state, parent))


def bfs_search(search_problem: SearchProblem) -> SearchSolution:
    """
    :param search_problem: the search problem
    :return: search solution
    """
    seen = {search_problem.start_state}  # states that have been seen
    fringe = deque()
    make_node_add_fringe(fringe, search_problem.start_state)  # add start state to fringe
    goal_state: Union[None, SearchNode] = None
    sol = SearchSolution(search_problem, "BFS")

    while not len(fringe) == 0:
        sol.nodes_visited += 1
        current_state = fringe.popleft()  # get state at the front of fringe
        if search_problem.check_goal(current_state.state):
            goal_state = current_state  # st goal state when found
            break
        successors = search_problem.get_successors(current_state.state)  # generate successors

        for s in successors:
            if s not in seen:
                make_node_add_fringe(fringe, s, current_state)
                seen.add(s)  # add to seen to ensure that repeating states are not added to fringe

    # generate solution path by backtracking
    while goal_state is not None:
        sol.path.append(goal_state.state)
        goal_state = goal_state.parent

    sol.path = sol.path[::-1]  # reverse solution path to start from start state
    return sol


def dfs_search(search_problem: SearchProblem, depth_limit=100, node: SearchNode = None,
               solution: SearchSolution = None, path: set = None, depth=0):
    """
    :param search_problem: search problem
    :param depth_limit: max depth limit of the search
    :param node: current node to explore from
    :param solution: working solution
    :param path: the current working
    :param depth: current depth of the search
    :return: solution of the search from the current node
    """
    if node is None:  # set up values if node is none i.e. search is from the root
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
        path = set()

    # add node to the solution path
    solution.nodes_visited += 1
    solution.path.append(node.state)
    if search_problem.check_goal(node.state):  # if node is goal node return solution
        return solution

    # add node to current working path
    path.add(node.state)

    # ensure depth limit is not exceeded
    if depth < depth_limit:
        successors = search_problem.get_successors(node.state)  # get successors
        for s in successors:
            if s not in path:  # path checking
                dfs_search(search_problem, depth_limit, SearchNode(s, node), solution, path, depth + 1)
                if search_problem.check_goal(solution.path[len(solution.path) - 1]):
                    return solution

    # if solution path does not end in goal remove node from solution path
    # recursive logic ensures that if solution path does not end in goal then solution path ends in goal state
    if not search_problem.check_goal(solution.path[len(solution.path) - 1]):
        solution.path.pop()
        path.remove(node.state)

    # return solution
    return solution


def ids_search(search_problem, depth_limit=100):
    """
    :param search_problem: search problem
    :param depth_limit: depth limit for search
    :return: search solution
    """
    current_depth_limit = 0  # current depth limit to search with
    solution = SearchSolution(search_problem, "IDS")
    while current_depth_limit <= depth_limit:  # ensure search depth limit is not exceeded
        # leverage dfs solution to search with current depth limit
        solution = dfs_search(search_problem, current_depth_limit)
        if len(solution.path) > 0:  # from the dfs logic if solution path > 0 then the goal was found
            return solution
        current_depth_limit += 1 # increment depth limit
    return solution
