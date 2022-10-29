import sys, parse
import time, os, copy, random

def min_max_mulitple_ghosts(problem, k):
    #Your p5 code here
    solution = parse.Solution(problem.seed, \
        [parse.State(None, None, copy.deepcopy(problem.layout), 0)], None)
    pacman_actions = [] # a list to record all the past actions of the pacman
    pacTurn = True
    while (problem.pacWin()==False and problem.pacLose()==False):
        if pacTurn == True:
            _, best_di = max_agent(problem, (1+len(problem.ghostlocs))*k) # (1+len(problem.ghostlocs))*k actions in total
            pacman_actions.append(best_di)
            problem.move("P", best_di)
            state = parse.State("P", best_di, copy.deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            # print(state.printLayout())
            if problem.pacWin() == True or problem.pacLose() == True: break
            pacTurn = False
        else:
            for ghost in problem.ghostlocs.keys():
                _, best_di = min_agent(problem, (1+len(problem.ghostlocs))*k, ghost)
                if best_di != '':
                    problem.move(ghost, best_di)
                state = parse.State(ghost, best_di, copy.deepcopy(problem.layout), problem.score)
                solution.statelist.append(state)
                if problem.pacLose() == True: break
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output(), solution.winner

# pacman agent
def max_agent(problem_state: parse.Problem, depth):
    if problem_state.pacWin() or problem_state.pacLose():
        return problem_state.score, ''
    if depth == 0:
        return eval_func(problem_state, 'P'), ''
    if depth > 0:
        feasible_direction = problem_state.feasibleDirection("P")
        if len(feasible_direction) == 1:
            next_problem_state = copy.deepcopy(problem_state)
            next_problem_state.move("P", feasible_direction[0])
            score, _ = min_agent(next_problem_state, depth-1, 'W')
            return score, feasible_direction[0]
        v = -1e9
        for di in feasible_direction:
            next_problem_state = copy.deepcopy(problem_state)
            next_problem_state.move("P", di)   
            score, _ = min_agent(next_problem_state, depth-1, 'W')
            if score > v:
                v = score
                best_di = di
            elif score == v:
                best_di = random.choice((di, best_di))
        return v, best_di

# ghost agent
def min_agent(problem_state: parse.Problem, depth, ghost):
    if problem_state.pacWin() or problem_state.pacLose():
        return problem_state.score, ''
    if depth == 0:
        return eval_func(problem_state, ghost), ''
    if depth > 0:
        feasible_direction = problem_state.feasibleDirection(ghost)
        # if this is the last ghost, next player is max_agent
        if ghost == list(problem_state.ghostlocs.keys())[-1]:
            if  feasible_direction == ():
                score, _ = max_agent(problem_state, depth-1)
                return score, ''
            if len(feasible_direction) == 1:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, feasible_direction[0])
                score, _ = max_agent(next_problem_state, depth-1)
                return score, feasible_direction[0]
            v = 1e9
            for di in problem_state.feasibleDirection(ghost):
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, di)
                score, _ = max_agent(next_problem_state, depth-1)
                if score < v:
                    v = score
                    best_di = di
                elif score == v:
                    best_di = random.choice((di, best_di))
        else:
            if feasible_direction == ():
                score, _ = min_agent(problem_state, depth-1, chr(ord(ghost)+1))
                return score, ''
            if len(feasible_direction) == 1:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, feasible_direction[0])
                score, _ = min_agent(next_problem_state, depth-1, chr(ord(ghost)+1))
                return score, feasible_direction[0]
            v = 1e9
            for di in feasible_direction:
                next_problem_state = copy.deepcopy(problem_state)
                next_problem_state.move(ghost, di)
                score, _ = min_agent(next_problem_state, depth-1, chr(ord(ghost)+1))
                if score < v:
                    v = score
                    best_di = di
                elif score == v:
                    best_di = random.choice((di, best_di))
        return v, best_di

def eval_func(problem_state: parse.Problem, next_player):
    dist_to_closest_food = 100000
    ghost_score = 0
    food_score = 0
    for ghost in problem_state.ghostlocs.keys():
        dist = abs(problem_state.pacmanloc[0]-problem_state.ghostlocs[ghost][0]) + abs(problem_state.pacmanloc[1]-problem_state.ghostlocs[ghost][1])
        if dist == 1 and 'P' != next_player:
            return problem_state.score + parse.PACMAN_EATEN_SCORE
        # larger penalty if distance to a ghost is less than 4
        if dist < 4:
            ghost_score -= 5/dist
        else:
            ghost_score -= 1/dist
    for food_loc in problem.foodlocs:
        dist = abs(problem_state.pacmanloc[0]-food_loc[0]) + abs(problem_state.pacmanloc[1]-food_loc[1])
        if dist < dist_to_closest_food:
            dist_to_closest_food = dist
        if dist_to_closest_food <= 1 and len(problem_state.foodlocs)==1 and next_player=="P":
            return problem_state.score + parse.PACMAN_WIN_SCORE
    food_score += 10-dist_to_closest_food
    return problem_state.score + ghost_score + food_score + parse.PACMAN_MOVING_SCORE

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
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
        solution, winner = min_max_mulitple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)