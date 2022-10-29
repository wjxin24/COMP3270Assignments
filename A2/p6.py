from random import random
import sys, parse
import time, os, copy, random

def expecti_max_mulitple_ghosts(problem, k):
    #Your p6 code here
    solution = parse.Solution(problem.seed, \
        [parse.State(None, None, copy.deepcopy(problem.layout), 0)], None)
    pacTurn = True
    while (problem.pacWin()==False and problem.pacLose()==False):
        if pacTurn == True:
            feasible_direction = problem.feasibleDirection("P")
            if len(feasible_direction) == 1:
                best_direction = feasible_direction[0]
            else:
                _, best_direction = expectimax(problem, k)
            problem.move("P", best_direction)
            state = parse.State("P", best_direction, copy.deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            # print(state.printLayout())
            pacTurn = False
        else:
            for ghost in problem.ghostlocs.keys():
                feasible_direction = problem.feasibleDirection(ghost)
                if feasible_direction==():
                    state = parse.State(ghost, '', copy.deepcopy(problem.layout), problem.score)
                    solution.statelist.append(state)
                else:
                    rand_di = random.choice(feasible_direction)
                    problem.move(ghost, rand_di)
                    state = parse.State(ghost, rand_di, copy.deepcopy(problem.layout), problem.score)
                    solution.statelist.append(state)
                    if problem.pacLose(): break
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output(), solution.winner

def expectimax(problem_state: parse.Problem, depth):
    if problem_state.pacWin() or problem_state.pacLose():
        return problem_state.score, ''
    if depth == 0:
        return eval_func(problem_state), ''
    if depth > 0:
        feasible_direction = problem_state.feasibleDirection("P")
        if len(feasible_direction) == 1:
            next_problem_state = copy.deepcopy(problem_state)
            next_problem_state.move("P", feasible_direction[0])
            score = ghost_agent(next_problem_state, depth, 'W')
            return score, feasible_direction[0]
        else:
            best_average_score = -10000
            for di in feasible_direction:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move('P', di)
                average_score = ghost_agent(next_problem_state, depth, 'W')
                if average_score >  best_average_score:
                    best_average_score = average_score
                    best_direction = di
                if average_score == best_average_score:
                    best_direction = random.choice([best_direction, di])
            return best_average_score, best_direction

def ghost_agent(problem_state: parse.Problem, depth, ghost) -> int:
    if problem_state.pacWin() or problem_state.pacLose():
        return problem_state.score
    feasible_direction = problem_state.feasibleDirection(ghost)
    # if this is the last ghost
    if ghost == list(problem_state.ghostlocs.keys())[-1]:
        if feasible_direction == ():
            score, _ = expectimax(problem_state, depth-1)
            return score
        if len(feasible_direction) == 1:
            next_problem_state = copy.deepcopy(problem_state)
            next_problem_state.move(ghost, feasible_direction[0])
            score, _ = expectimax(next_problem_state, depth-1)
            return score
        else:
            score_sum = 0
            for di in feasible_direction:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, di)
                score, _ = expectimax(next_problem_state, depth-1)
                score_sum += score
            return score_sum / len(feasible_direction)
    else:
        if feasible_direction == ():
            score = ghost_agent(problem_state, depth, chr(ord(ghost)+1))
            return score
        if len(feasible_direction) == 1:
            next_problem_state = copy.deepcopy(problem_state)
            next_problem_state.move(ghost, feasible_direction[0])
            score = ghost_agent(next_problem_state, depth, chr(ord(ghost)+1))
            return score
        else:
            score_sum = 0
            for di in feasible_direction:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, di)
                score = ghost_agent(next_problem_state, depth, chr(ord(ghost)+1))
                score_sum += score
            return score_sum / len(feasible_direction)


def eval_func(problem_state: parse.Problem):
    dist_to_closest_food = 100000
    ghost_score = 0
    food_score = 0
    for ghost in problem_state.ghostlocs.keys():
        dist = abs(problem_state.pacmanloc[0]-problem_state.ghostlocs[ghost][0]) + abs(problem_state.pacmanloc[1]-problem_state.ghostlocs[ghost][1])
        if dist == 0:
            return problem_state.score + parse.PACMAN_EATEN_SCORE
        # penalty for distance to ghost
        # Since the next player is pacman, it is likely to escape when dist>=1, so the penalty is not too high
        ghost_score -= 1/dist

    for food_loc in problem_state.foodlocs:
        dist = abs(problem_state.pacmanloc[0]-food_loc[0]) + abs(problem_state.pacmanloc[1]-food_loc[1])
        if dist < dist_to_closest_food:
            dist_to_closest_food = dist
        # if pacman can win in the next action
        if dist_to_closest_food <= 1 and len(problem_state.foodlocs)==1:
            return problem_state.score + parse.PACMAN_WIN_SCORE
    food_score += 10 - dist_to_closest_food
    return problem_state.score + ghost_score + food_score + parse.PACMAN_MOVING_SCORE

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)