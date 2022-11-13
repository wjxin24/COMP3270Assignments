# Findings: My algorithm finds the optimal policy about 80% of the time.
# After some observation, I found the policies that are different from the optimal one are usually
# | E || E || E || x |
# | N || # || W || x |
# | N || W || N || S |, where the policy for the grid of the 3rd column of the 3rd row is 'N' instead of 'W'.
#
# Analysis: The random chosen directions may affect the outcome of the optimal policy. 
# Since there is a negative living reward at each action, if a direction is chosen for more times, 
# the Q value for this direction will likely to be smaller.
# Especially if a direction is chosen often in the beginning, as the learning rate is larger in the beginning,
# the living reward may lead to bigger decrease in the Q value for this direction.
# Then the algorithm may choose another direction as the best policy for this state 
# if the Q value for the direction of optimal policy is smaller than others.
#
# To run the code: `python p4.py [trail] [verbose]`
# where trail is the number of trails,
# set verbose to 1 to output the policy of each trail, set verbose to 0 for not outputing the policies
# sample run: `python p4.py 10 0`


import sys, random

ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']} 

def q_learning(grid, start, discount, noise, livingReward):
    # initialize Q values
    Q = []
    for i in range(len(grid)):
        Q_row = []
        for j in range(len(grid[i])):
            if grid[i][j] == '#':
                Q_row.append('#')
            elif grid[i][j] == 'S' or grid[i][j] == '_':
                Q_row.append({'E': 0.0, 'N': 0.0, 'S': 0.0, 'W': 0.0})
            else: # exit grid
                Q_row.append(0.0)
        Q.append(Q_row)

    alpha = 0.5
    epsilon = 0.9
    converge = False
    episode = 0

    while (converge != True):
        episode += 1
        # decrease learning rate and epsilon every 10 episodes
        if episode%10 == 0:
            alpha *= 0.9
            epsilon *= 0.9
        player = start
        converge = True
        while (True):
            # exit grid
            if grid[player[0]][player[1]] not in ('#', 'S', '_'):
                new_Q = float(grid[player[0]][player[1]])
                if abs(new_Q - Q[player[0]][player[1]]) > 1e-4: converge = False
                Q[player[0]][player[1]] = (1-alpha)*Q[player[0]][player[1]] + alpha*new_Q
                break
            
            # using epsilon greedy to force exploration
            random_act = random.choices([True, False], weights=[epsilon, 1-epsilon])
            # randomly explore other actions with probability epsilon
            if random_act:   
                intend_dir = random.choice(('N','E','S','W'))
                player_new = move(player, intend_dir, noise, grid)
                # if arrived at exit grid
                if grid[player_new[0]][player_new[1]] not in ('#', 'S', '_'):
                    new_Q = livingReward + discount*Q[player_new[0]][player_new[1]]
                else:
                    new_Q = livingReward + discount*max(Q[player_new[0]][player_new[1]].values())
                if abs((1-alpha)*Q[player[0]][player[1]][intend_dir] + alpha*new_Q - Q[player[0]][player[1]][intend_dir]) > 1e-4: converge = False
                Q[player[0]][player[1]][intend_dir] = (1-alpha)*Q[player[0]][player[1]][intend_dir] + alpha*new_Q
                player = player_new

            # follow the current best policy with probability 1-epsilon
            else:
                best_policy = max(Q[player[0]][player[1]], key=Q[player[0]][player[1]].get)
                player_new = move(player, best_policy, noise, grid)
                # if arrived at exit grid
                if grid[player_new[0]][player_new[1]] not in ('#', 'S', '_'):
                    new_Q = livingReward + discount*Q[player_new[0]][player_new[1]]
                else:
                    new_Q  = livingReward + discount*max(Q[player_new[0]][player_new[1]].values())
                if abs((1-alpha)*Q[player[0]][player[1]][best_policy] + alpha*new_Q - Q[player[0]][player[1]][best_policy]) > 1e-4: converge = False
                Q[player[0]][player[1]][best_policy] = (1-alpha)*Q[player[0]][player[1]][best_policy] + alpha*new_Q
                player = player_new
                  
    optimal_policy = ''
    for i in range(len(Q)):
        for j in range(len(Q[i])):
            if Q[i][j] == '#':
                optimal_policy += '| # |'
            elif isinstance(Q[i][j], float):
                optimal_policy += '| x |'
            else:
                optimal_policy += '| %s |' % max(Q[i][j], key = Q[i][j].get)
        optimal_policy += '\n'
    return optimal_policy[:-1]


def move(player, intend_dir, noise, grid):
    direction = random.choices(NOISE_DI[intend_dir], weights=[1 - noise*2, noise, noise])[0]
    if player[0] + ENSW[direction][0] >= 0 and player[0] + ENSW[direction][0] < len(grid) and \
            player[1] + ENSW[direction][1] >= 0 and \
                player[1] + ENSW[direction][1] < len(grid[player[0] + ENSW[direction][0]]):
        # check wall
        if grid[player[0] + ENSW[direction][0]][player[1] + ENSW[direction][1]] != '#':
            return [player[0]+ENSW[direction][0], player[1]+ENSW[direction][1]]
    return player

if __name__ == "__main__":
    grid =  [['_', '_', '_', '1'], ['_', '#', '_', '-1'], ['S', '_', '_', '_']]
    start = [2, 0]
    discount = 1
    noise = 0.1
    livingReward = -0.01
    trails = int(sys.argv[1])
    verbose =  int(sys.argv[2])
    optimal = 0
    for i in range(trails):
        policy = q_learning(grid, start, discount, noise, livingReward)
        if verbose:
            print("Trail", i+1)
            print(policy)
        optimal_policy = "| E || E || E || x |\n| N || # || W || x |\n| N || W || W || S |"
        if policy == optimal_policy:
            optimal += 1
    print("Chances that optimal policy is found: %d/%d" %(optimal, trails))
