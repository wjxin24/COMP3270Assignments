import sys, parse, grader
from heapq import heappush, heappop

def greedy_search(problem : parse.Problem):
    #Your p4 code here
    frontier = []
    heappush(frontier, (problem.graph_H[problem.start_state], [problem.start_state]))
    exploredSet = set()
    exploreOrder = []
    while frontier: 
        node = heappop(frontier)
        if (node[1][-1] in problem.goal_states):
            solutionPath = node[1]
            break
        if node[1][-1] not in exploredSet:
            exploredSet.add(node[1][-1])
            exploreOrder.append(node[1][-1])
            for child in problem.graph[node[1][-1]]:
                heappush(frontier, (problem.graph_H[child[1]], node[1] + [child[1]]))
    solution = ' '.join(exploreOrder) + '\n' + ' '.join(solutionPath)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)