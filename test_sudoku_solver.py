import unittest
import sudoku_solver
import numpy as np


class TestSudokuSolver(unittest.TestCase):

    def test_complex_sudoku(self):
        matrix = np.loadtxt('test_files/test_file_4.csv', delimiter=',', dtype=int)
        result = sudoku_solver.execute_probabilities(matrix)
        control = [[9, 4, 6, 3, 5, 1, 7, 8, 2], [5, 7, 2, 9, 4, 8, 6, 1, 3], [3, 8, 1, 7, 2, 6, 9, 4, 5],
                   [2, 1, 5, 6, 3, 4, 8, 7, 9], [4, 3, 9, 2, 8, 7, 1, 5, 6], [7, 6, 8, 5, 1, 9, 2, 3, 4],
                   [6, 2, 4, 1, 7, 5, 3, 9, 8], [8, 9, 7, 4, 6, 3, 5, 2, 1], [1, 5, 3, 8, 9, 2, 4, 6, 7]]

        self.assertTrue((result == np.asanyarray(control)).all())

    def test_simple_sudo(self):
        matrix = np.loadtxt('test_files/test_file_2.csv', delimiter=',', dtype=int)
        result = sudoku_solver.execute_probabilities(matrix)
        control = [[4, 5, 8, 9, 1, 7, 3, 6, 2], [3, 9, 6, 2, 4, 8, 5, 7, 1], [2, 1, 7, 6, 5, 3, 4, 8, 9],
                   [5, 6, 2, 1, 8, 9, 7, 3, 4], [8, 4, 3, 7, 2, 5, 1, 9, 6], [1, 7, 9, 4, 3, 6, 8, 2, 5],
                   [6, 8, 4, 5, 7, 2, 9, 1, 3], [9, 3, 1, 8, 6, 4, 2, 5, 7], [7, 2, 5, 3, 9, 1, 6, 4, 8]]

        self.assertTrue((result == np.asanyarray(control)).all())


if __name__ == '__main__':
    unittest.main()
