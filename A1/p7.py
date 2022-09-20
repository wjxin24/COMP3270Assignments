import sys, parse, grader
import p6

def better_board(problem):
    #Your p7 code here
    min = 100
    number_of_attacks_row = p6.number_of_attacks(problem).split('\n')
    number_of_attacks = [number_of_attacks_row[i].split() for i in range(8)]
    for row in range(8):
        for col in range(8):
            if int(number_of_attacks[row][col]) < min:
                min = int(number_of_attacks[row][col])
                min_loc = (row, col)
    problem[min_loc[1]] = min_loc[0]
    solution_list = [['.'] * 8 for i in range(8)]
    for col in range(8):
        solution_list[problem[col]][col] = 'q'
    solution = '\n'.join([' '.join(str(solution_list[i][j]) for j in range(8)) for i in range(8)])
    return solution
# file_path = "test_cases/p7/1.prob"
# better_board(parse.read_8queens_search_problem(file_path))
if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)