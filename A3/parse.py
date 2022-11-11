import random, p1

ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}
NOISE_DI = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}


            

def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        line = file.readline()
        assert line.startswith("seed:")
        seed = int(line.split()[1])
        line = file.readline()
        assert line.startswith("noise:")
        noise = float(line.split()[1])
        line = file.readline()
        assert line.startswith("livingReward:")
        livingReward = float(line.split()[1])
        line = file.readline()
        
        assert line.startswith("grid:")
        layout = []
        row = 0
        line = file.readline()
        player = []
        while line.startswith("policy:") == False:
            row_list = line.split()
            for col in range(len(row_list)):
                if row_list[col] == 'S':
                    player = [row, col]
            row += 1
            layout.append(row_list)
            line = file.readline()
        
        assert line.startswith("policy:")
        policy = []
        row = 0
        line = file.readline()
        while line:
            row_list = line.split()
            row += 1
            policy.append(row_list)
            line = file.readline()
    state = p1.State(layout, player, policy)
    problem = p1.Problem(seed, noise, livingReward, state, policy)
    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = ''
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = ''
    return problem