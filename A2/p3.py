from copy import deepcopy
import sys, grader, parse, math, random

def random_play_multiple_ghosts(problem: parse.Problem):
    #Your p3 code here
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
            for ghost in problem.ghostlocs.keys():
                feasible_direction = problem.feasibleDirection(ghost)
                if feasible_direction==():
                    state = parse.State(ghost, '', deepcopy(problem.layout), problem.score)
                    solution.statelist.append(state)
                else:
                    rand_di = random.choice(feasible_direction)
                    problem.move(ghost, rand_di)
                    state = parse.State(ghost, rand_di, deepcopy(problem.layout), problem.score)
                    solution.statelist.append(state)
                    if problem.pacLose(): break
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)