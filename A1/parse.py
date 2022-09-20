import os, sys

class Problem:
  def __init__(self, start_state : str, goal_states : list, 
                graph : dict, graph_H : dict):
    self.start_state = start_state
    self.goal_states = goal_states
    self.graph = graph
    self.graph_H = graph_H

def read_graph_search_problem(file_path):
    #Your p1 code here
    graph = {}
    graph_H = {}
    with open(file_path, 'r') as file:
        line = file.readline()
        if line.startswith("start_state"):
            start_state = line.split()[1]
        line = file.readline()
        if line.startswith("goal_states"):
            goal_states = line.split()[1:]
        line = file.readline()
        while line and len(line.split()) == 2:
            state, state_H = line.split()
            graph_H[state] = float(state_H)
            graph[state] = []
            line = file.readline()
        while line and len(line.split()) == 3:
            start = line.split()[0]
            graph[start].append((float(line.split()[2]), line.split()[1]))
            line = file.readline()
    problem = Problem(start_state, goal_states, graph, graph_H)
    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    problem = [0, 0, 0, 0, 0, 0, 0, 0]
    with open(file_path, 'r') as file:
        for i in range(8):
            line = file.readline()
            grids = line.split()
            for j in range(8):
                if grids[j] == 'q':
                    problem[j] = i
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')