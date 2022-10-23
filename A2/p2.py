import sys, parse
import time, os, copy, random

def better_play_single_ghosts(problem):
    #Your p2 code here
    solution = parse.Solution(problem.seed, \
        [parse.State(None, None, copy.deepcopy(problem.layout), 0)], None)
    pacman_actions = [] # a list to record all the past actions of the pacman
    pacTurn = True
    while (problem.pacWin()==False and problem.pacLose()==False):
        if pacTurn == True:
            feasible_direction = problem.feasibleDirection("P")
            if len(feasible_direction) == 1:
                best_direction = feasible_direction[0]
            else:
                best_eval_score = -1000
                for di in feasible_direction:
                    eval_score = eval_func(problem, di, pacman_actions)
                    if  eval_score > best_eval_score:
                        best_eval_score = eval_score
                        best_direction = di
            problem.move("P", best_direction)
            pacman_actions.append(best_direction)
            state = parse.State("P", best_direction, copy.deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            pacTurn = False
        else:
            rand_di = random.choice(problem.feasibleDirection("W"))
            problem.move("W", rand_di)
            state = parse.State("W", rand_di, copy.deepcopy(problem.layout), problem.score)
            solution.statelist.append(state)
            pacTurn = True
    solution.winner = "Pacman" if problem.pacWin() else "Ghost"
    return solution.output(), solution.winner

def eval_func(problem: parse.Problem, direction, pacman_actions):
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
    if dist_to_closest_ghost<2: return -500
    # if pacman has been moving in loop, avoid repeated direction
    if move_in_loop(pacman_actions, direction):
        return -10
    # if distance to closest ghost is larger than 4, focus on food first
    return min(dist_to_closest_ghost,4) + 3/(dist_to_closest_food+1)

# check if the pacman is move back and forth in loop for more than 2 times
def move_in_loop(pacman_actions, direction):
    if len(pacman_actions) < 4: return False
    if pacman_actions[-1] == pacman_actions[-3] and pacman_actions[-2] == parse.opposite_direction(pacman_actions[-1])\
         and pacman_actions[-2] == pacman_actions[-4] and direction == pacman_actions[-2]:
            return True
        

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
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
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)