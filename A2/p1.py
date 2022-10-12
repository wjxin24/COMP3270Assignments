import sys, random, grader, parse
from copy import deepcopy

def random_play_single_ghost(problem: parse.Problem):
    #Your p1 code here
    solution = parse.Solution(problem.seed, \
        [parse.State(None, None, deepcopy(problem.layout), 0)], None)
    random.seed(problem.seed, version=1)
    pacTurn = True
    while (problem.pacWin()==False and problem.pacLose()==False):
        if pacTurn == True:
            rand_di = random.choice(problem.feasibleDirection("P"))
            problem.move("P", rand_di)
            state = parse.State("P", rand_di, deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            pacTurn = False
        else:
            rand_di = random.choice(problem.feasibleDirection("W"))
            problem.move("W", rand_di)
            state = parse.State("W", rand_di, deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)