import sys, parse
import time, os, copy, random

def better_play_mulitple_ghosts(problem):
    #Your p4 code here
    solution = parse.Solution(problem.seed, \
        [parse.State(None, None, copy.deepcopy(problem.layout), 0)], None)
    score = 0
    pacTurn = True
    while (problem.pacWin()==False and problem.pacLose()==False):
        if pacTurn == True:
            feasible_direction = problem.feasibleDirection("P")
            if len(feasible_direction) == 1:
                best_direction = feasible_direction[0]
            else:
                best_eval_score = 0
                for di in feasible_direction:
                    eval_score = eval_func(problem, di)
                    if  eval_score >= best_eval_score:
                        best_eval_score = eval_score
                        best_direction = di
            score += problem.move("P", best_direction)
            state = parse.State("P", best_direction, copy.deepcopy(problem.layout), score)
            solution.statelist.append(state)
            pacTurn = False
        else:
            for ghost in problem.ghostlocs.keys():
                feasible_direction = problem.feasibleDirection(ghost)
                if feasible_direction==():
                    state = parse.State(ghost, '', copy.deepcopy(problem.layout), score)
                    solution.statelist.append(state)
                else:
                    rand_di = random.choice(feasible_direction)
                    score += problem.move(ghost, rand_di)
                    state = parse.State(ghost, rand_di, copy.deepcopy(problem.layout), score)
                    solution.statelist.append(state)
                    if problem.pacLose(): break
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output(), solution.winner

def eval_func(problem: parse.Problem, direction):
    new_pacman_loc = [problem.pacmanloc[0]+parse.ENSW[direction][0],\
                        problem.pacmanloc[1]+parse.ENSW[direction][1]]
    dist_to_closest_ghost = 100000
    dist_to_closest_food = 100000
    for ghost_loc in problem.ghostlocs.values():
        dist = abs(new_pacman_loc[0]-ghost_loc[0]) + abs(new_pacman_loc[1]-ghost_loc[1])
        if dist < dist_to_closest_ghost:
            dist_to_closest_ghost = dist
    for food_loc in problem.foodlocs:
        dist = abs(new_pacman_loc[0]-food_loc[0]) + abs(new_pacman_loc[1]-food_loc[1])
        if dist < dist_to_closest_food:
            dist_to_closest_food = dist
    # if distance to closest ghost is less than 2, run away from ghost
    if dist_to_closest_ghost<2: return 0
    # if distance to closest ghost is larger than 4, focus on food first
    return min(dist_to_closest_ghost,4) + 3/(dist_to_closest_food+1)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_mulitple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)