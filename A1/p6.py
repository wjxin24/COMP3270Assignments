import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    def count_num_of_attacks(problem):
        attack = 0
        for i in range(8):
            for j in range(i+1, 8):
                if problem[j] == problem[i]:
                    attack += 1
                elif abs(problem[j] - problem[i]) == j - i:
                    attack += 1
        return attack
    solution_list = [[0] * 8 for i in range(8)]
    for i in range(8):
        for j in range(8):
            solution_list[i][j] = count_num_of_attacks(problem[:j] + [i] + problem[j+1:])
    solution = '\n'.join(''.join(['{:2d}'.format(solution_list[i][0])] + 
                        ['{:3d}'.format(solution_list[i][j]) for j in range(1, 8)])for i in range(8))
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)