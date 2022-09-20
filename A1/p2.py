import sys, grader, parse
import collections

def bfs_search(problem):
    #Your p2 code here
    frontier = collections.deque([[problem.start_state]])
    exploredSet = set()
    exploreOrder = []
    while frontier: 
        node = frontier.popleft()
        if (node[-1] in problem.goal_states):
            solutionPath = node
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            exploreOrder.append(node[-1])
            for child in problem.graph[node[-1]]:
                frontier.append(node + [child[1]])
    solution = ' '.join(exploreOrder) + '\n' + ' '.join(solutionPath)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)