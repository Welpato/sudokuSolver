# coding: utf-8
import numpy as np
import copy

import sys

AREA_KEYS = {
    0: [0, 3, 0, 3],
    1: [0, 3, 3, 6],
    2: [0, 3, 6, 9],
    3: [3, 6, 0, 3],
    4: [3, 6, 3, 6],
    5: [3, 6, 6, 9],
    6: [6, 9, 0, 3],
    7: [6, 9, 3, 6],
    8: [6, 9, 6, 9]
}


def total_empty(matrix):
    counter = 0
    for line in matrix:
        for number in line:
            if number == 0:
                counter += 1
    return counter


def return_if_pos_num(pos, number):
    for position in pos:
        if position == number:
            return True
    return False


def return_column(matrix, column):
    return matrix[:, column]


def return_area(matrix, area_number):
    area_keys = AREA_KEYS.get(area_number)

    return matrix[area_keys[0]:area_keys[1], area_keys[2]:area_keys[3]].flatten()


def return_area_number(matrix, number):
    return return_numbers(return_area, matrix, number)


def return_lines_number(matrix, number):
    def get_line(sub_matrix, position):
        return sub_matrix[position]

    return return_numbers(get_line, matrix, number)


def return_numbers_column(matrix, number):
    return return_numbers(return_column, matrix, number)


def return_numbers(get_zone, matrix, number):
    values = np.zeros(9, dtype=object)
    for pos in range(0, 9):
        if not return_if_pos_num(get_zone(matrix, pos), number):
            values[pos] = number

    return values


def cross_number_area_line_column(matrix, number):
    areas = return_area_number(matrix, number)
    lines = return_lines_number(matrix, number)
    columns = return_numbers_column(matrix, number)
    result_matrix = np.zeros((9, 9), dtype=object)
    result_matrix[0:9] = number

    for con in range(0, 9):
        if lines[con] != number:
            result_matrix[con] = 0
        if columns[con] != number:
            result_matrix[:, con] = 0
        if areas[con] != number:
            area_keys = AREA_KEYS.get(con)
            result_matrix[area_keys[0]:area_keys[1], area_keys[2]:area_keys[3]] = 0
    return result_matrix


def all_number_position(matrix):
    matrix_numbers = np.zeros(9, dtype=object)
    for con in range(0, 9):
        matrix_numbers[con] = cross_number_area_line_column(matrix, con + 1)

    return matrix_numbers


def create_probabilities(matrix):
    result_matrix = np.zeros((9, 9), dtype=object)
    matrix_numbers = all_number_position(matrix)

    for line in range(0, 9):
        for column in range(0, 9):
            if matrix[line][column] == 0:
                array_prob = []
                for con in range(0, 9):
                    if matrix_numbers[con][line][column] > 0:
                        array_prob.append(matrix_numbers[con][line][column])
                result_matrix[line][column] = array_prob
            else:
                result_matrix[line][column] = matrix[line][column]

    return result_matrix


def insert_hidden_number(matrix, matrix_prob):
    execute_again = False
    for line in range(0, 9):
        new_line = verify_hidden_number(matrix[line], matrix_prob[line])
        if np.any(new_line != matrix[line]):
            execute_again = True
            matrix[line] = new_line
    if execute_again:
        matrix = execute_probabilities(copy.deepcopy(matrix))
    return matrix


def insert_hidden_number_column(matrix, matrix_prob):
    return insert_hidden_number(matrix.transpose(), matrix_prob.transpose()).transpose()


def insert_hidden_number_area(matrix, matrix_prob):
    # It could also be done using the insert_hidden_number function
    # but the transformation process increase a lot in the processing time
    execute_again = False
    for area in range(0, 9):
        area_matrix = return_area(matrix, area)
        area_prob = return_area(matrix_prob, area)
        new_area = verify_hidden_number(copy.deepcopy(area_matrix), area_prob)
        if np.any(new_area != area_matrix):
            area_keys = AREA_KEYS.get(area)
            matrix[area_keys[0]:area_keys[1], area_keys[2]:area_keys[3]] = new_area.reshape(3, 3)
            execute_again = True

    if execute_again:
        matrix = execute_probabilities(copy.deepcopy(matrix))
    return matrix


def verify_hidden_number(area, area_prob):
    amount_number = np.zeros(9, dtype=int)
    for column in range(0, 9):
        if area[column] == 0:
            for prob_value in area_prob[column]:
                amount_number[prob_value - 1] += 1

    for value_amount in range(0, 9):
        if amount_number[value_amount] == 1:
            for col_add in range(0, 9):
                if area[col_add] == 0:
                    for prob_value in area_prob[col_add]:
                        if prob_value == value_amount + 1:
                            area[col_add] = value_amount + 1

    return area


def check_unique_numbers(zone):
    total_num_line = np.zeros(10, dtype=int)
    for number in zone:
        if number > 0:
            total_num_line[number] += 1
            if total_num_line[number] > 1:
                return False
    return True


def is_valid_sudoku(matrix):
    # Really need this if?
    if total_empty(matrix) == 81:
        return False

    for line in matrix:
        if not check_unique_numbers(line):
            return False

    for column in matrix.transpose():
        if not check_unique_numbers(column):
            return False

    for a in range(0, 9):
        area = return_area(matrix, a)
        if not check_unique_numbers(area):
            return False

    return True


def execute_multiple_probabilities(matrix, matrix_prob):
    probabilities = []
    result = np.zeros((9, 9), dtype=int)

    for line in range(0, 9):
        for column in range(0, 9):
            if matrix[line][column] == 0:
                for con_len in range(0, len(matrix_prob[line][column])):
                    con_result = copy.deepcopy(matrix)
                    con_result[line][column] = matrix_prob[line][column][con_len]
                    if is_valid_sudoku(con_result):
                        con_result = execute_probabilities(con_result)
                        if is_valid_sudoku(con_result):
                            if total_empty(con_result) == 0:
                                return con_result
                            else:
                                probabilities.append(con_result)

    for prob in probabilities:
        if is_valid_sudoku(prob):
            if total_empty(prob) < 81:
                result = prob

    return result


# Main execute process
def execute_probabilities(matrix):
    matrix_prob = create_probabilities(matrix)
    execute_again = False
    matrix_result = copy.deepcopy(matrix)
    empty = np.zeros((9, 9), dtype=int)
    for line in range(0, 9):
        for column in range(0, 9):
            if matrix[line][column] == 0 and len(matrix_prob[line][column]) == 1:
                matrix_result[line][column] = matrix_prob[line][column][0]
                execute_again = True

    if execute_again is True and np.any(empty != matrix_result) and total_empty(matrix_result) > 0:
        control_matrix = execute_probabilities(copy.deepcopy(matrix_result))
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix
    elif execute_again is False and np.any(empty != matrix_result) and total_empty(matrix_result) > 0:
        matrix_prob = create_probabilities(matrix_result)
        control_matrix = insert_hidden_number(matrix_result, matrix_prob)
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix

    if total_empty(matrix_result) > 0 and np.any(empty != matrix_result):
        matrix_prob = create_probabilities(matrix_result)
        control_matrix = insert_hidden_number_column(matrix_result, matrix_prob)
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix
        if total_empty(matrix_result) > 0 and np.any(empty != matrix_result):
            matrix_prob = create_probabilities(matrix_result)
            control_matrix = insert_hidden_number_area(matrix_result, matrix_prob)
            if is_valid_sudoku(control_matrix):
                matrix_result = control_matrix
                if total_empty(matrix_result) > 0 and np.any(empty != matrix_result):
                    matrix_prob = create_probabilities(matrix_result)
                    control_matrix = execute_multiple_probabilities(copy.deepcopy(matrix_result), matrix_prob)
                    if np.any(control_matrix != matrix_result) and np.any(empty != control_matrix):
                        matrix_result = control_matrix
                        if total_empty(matrix_result) > 0:
                            matrix_result = execute_probabilities(matrix_result)
    return matrix_result
