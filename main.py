from puzzles import sudoku_puzzles
from sudoku import create_variables, SudokuCSP, backtracking_search
from constraints.sudoku_constraint9x9 import constraint9x9

def main():
    test_csp = SudokuCSP(create_variables(sudoku_puzzles.puzzle_4))
    variables, intermediate_domains, assignment, failed = backtracking_search(test_csp)
    for i in range(1, 10):
        for j in range(1, 10):
            print(variables[int(f'{i}{j}')], end="")
        print()
    print(variables)
    print(assignment)
    print(failed)

if __name__ == "__main__":
    main()