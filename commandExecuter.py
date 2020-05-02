import getopt
import sys
import numpy as np
import sudokuSolver


def main(argv):
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg

    matrix = np.loadtxt(input_file, delimiter=',', dtype=int)
    print('-- SUDOKU --')
    print(matrix)
    print('-- RESULT --')
    result = sudokuSolver.execute_probabilities(matrix)
    print(result)
    print('TOTAL EMPTY: ', sudokuSolver.total_empty(result))
    print('IS VALID: ', sudokuSolver.is_valid_sudoku(result))


if __name__ == "__main__":
    main(sys.argv[1:])
