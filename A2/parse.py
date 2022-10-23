import os, sys

WALL = '%'
GHOST = ['W', 'X', 'Y', 'Z']
PACMAN = 'P'
FOOD = '.'
EMPTY = ' '

ENSW = {'E': (0,1), 'N': (-1,0), 'S': (1,0), 'W': (0,-1)}

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

class Problem:
    def __init__(self, seed : int, layout : list, pacmanloc : list, ghostlocs : dict, foodlocs : list, score: int):
        self.seed = seed
        self.layout = layout
        self.pacmanloc = pacmanloc
        self.ghostlocs = ghostlocs
        self.foodlocs = foodlocs
        self.score = score
    def pacWin(self) -> bool:
        return self.foodlocs == []
    def pacLose(self) -> bool:
        for gloc in self.ghostlocs.values():
            if self.pacmanloc == gloc:
                return True
        return False

    def feasibleDirection(self, who) -> list:
        feaD = []
        if who == "P":
            for di in ENSW:
                if self.layout[self.pacmanloc[0]+ENSW[di][0]][self.pacmanloc[1]+ENSW[di][1]] != WALL:
                    feaD.append(di)
        else:
            for di in ENSW:
                if self.layout[self.ghostlocs[who][0]+ENSW[di][0]][self.ghostlocs[who][1]+ENSW[di][1]] not in [WALL] + GHOST:
                    feaD.append(di)
        return tuple(feaD)

    def move(self, who, direction):
        if who == "P":
            self.layout[self.pacmanloc[0]][self.pacmanloc[1]] = EMPTY
            newLoc = self.layout[self.pacmanloc[0]+ENSW[direction][0]][self.pacmanloc[1]+ENSW[direction][1]]
            self.layout[self.pacmanloc[0]+ENSW[direction][0]][self.pacmanloc[1]+ENSW[direction][1]] = PACMAN
            self.pacmanloc = [self.pacmanloc[0]+ENSW[direction][0], self.pacmanloc[1]+ENSW[direction][1]]
            if newLoc in GHOST:
                self.layout[self.pacmanloc[0]][self.pacmanloc[1]] = newLoc
                self.score += PACMAN_MOVING_SCORE+PACMAN_EATEN_SCORE
                return
            elif newLoc == FOOD:
                self.foodlocs.remove([self.pacmanloc[0], self.pacmanloc[1]])
                if self.pacWin():
                    self.score += PACMAN_MOVING_SCORE+EAT_FOOD_SCORE+PACMAN_WIN_SCORE
                    return
                self.score += PACMAN_MOVING_SCORE+EAT_FOOD_SCORE
                return
            self.score += PACMAN_MOVING_SCORE
        else:
            if [self.ghostlocs[who][0],self.ghostlocs[who][1]] in self.foodlocs:
                self.layout[self.ghostlocs[who][0]][self.ghostlocs[who][1]] = FOOD
            else:
                self.layout[self.ghostlocs[who][0]][self.ghostlocs[who][1]] = EMPTY
            newLoc = self.layout[self.ghostlocs[who][0]+ENSW[direction][0]][self.ghostlocs[who][1]+ENSW[direction][1]]
            self.layout[self.ghostlocs[who][0]+ENSW[direction][0]][self.ghostlocs[who][1]+ENSW[direction][1]] = who
            self.ghostlocs[who] = [self.ghostlocs[who][0]+ENSW[direction][0], self.ghostlocs[who][1]+ENSW[direction][1]]
            if newLoc == PACMAN:
                self.score += PACMAN_EATEN_SCORE
            return

class State:
    def __init__(self, player, direction, layout, score):
        self.player = player
        self.direction = direction
        self.layout = layout
        self.score = score
    def printLayout(self) -> str:
        out = '\n'.join(''.join(c for c in i) for i in self.layout)
        return out

class Solution:
    def __init__(self, seed, statelist, winner):
        self.seed = seed
        self.statelist = statelist
        self.winner = winner
    def output(self) -> str:
        out = "seed: {seed}\n0\n".format(seed = self.seed)
        out += self.statelist[0].printLayout() + '\n'
        for i in range(1, len(self.statelist)):
            out += "{ind}: {player} moving {direction}\n"\
                .format(ind=i, player=self.statelist[i].player,\
                    direction=self.statelist[i].direction)
            out += self.statelist[i].printLayout()\
                + "\nscore: {score}\n"\
                    .format(score=self.statelist[i].score)
        out += "WIN: {winner}".format(winner=self.winner)
        return out

def opposite_direction(direction):
    if direction == 'W': return 'E'
    if direction == 'E': return 'W'
    if direction == 'N': return 'S'
    if direction == 'S': return 'N'

def read_layout_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        line = file.readline()
        if line.startswith("seed:"):
            seed = int(line.split()[1])
        layout = []
        ghostlocs = {}
        ghostnum = 0
        foodlocs = []
        row = 0
        line = file.readline()
        while line:
            cols = len(line)
            row_list = []
            for col in range(cols):
                if line[col] != '\n':
                    row_list.append(line[col])
                if line[col] == PACMAN:
                    pacmanloc = [row, col]
                elif line[col] in GHOST:
                    ghostlocs[line[col]] = [row, col]
                    ghostnum += 1
                elif line[col] == FOOD:
                    foodlocs.append([row, col])
            row += 1
            layout.append(row_list)
            line = file.readline()
    problem = Problem(seed, layout, pacmanloc, dict(sorted(ghostlocs.items())), foodlocs, 0)
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')