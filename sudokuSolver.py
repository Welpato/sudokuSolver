# coding: utf-8
import numpy as np
import copy

import sys


def total_empty(matrix):
    counter = 0
    for line in matrix:
        for number in line:
            if number == 0:
                counter += 1
    return counter


def return_if_pos_num(pos, number):
    position = 0
    number_position = False
    while position < len(pos):
        if pos[position] == number:
            number_position = True
            break
        position = position + 1
    return number_position


def return_column(matrix, column):
    return [row[column] for row in matrix]


def return_line_column_area(number_area):
    lines_columns = np.zeros(9, dtype=object)
    lines_columns[0] = 0
    lines_columns[1] = 1
    lines_columns[2] = 2
    lines_columns[3] = 0
    lines_columns[4] = 1
    lines_columns[5] = 2
    if number_area == 1:
        lines_columns[3] = 3
        lines_columns[4] = 4
        lines_columns[5] = 5
    elif number_area == 2:
        lines_columns[3] = 6
        lines_columns[4] = 7
        lines_columns[5] = 8
    elif number_area == 3 or number_area == 4 or number_area == 5:
        lines_columns[0] = 3
        lines_columns[1] = 4
        lines_columns[2] = 5
        if number_area == 4:
            lines_columns[3] = 3
            lines_columns[4] = 4
            lines_columns[5] = 5
        elif number_area == 5:
            lines_columns[3] = 6
            lines_columns[4] = 7
            lines_columns[5] = 8
    elif number_area == 6 or number_area == 7 or number_area == 8:
        lines_columns[0] = 6
        lines_columns[1] = 7
        lines_columns[2] = 8
        if number_area == 7:
            lines_columns[3] = 3
            lines_columns[4] = 4
            lines_columns[5] = 5
        elif number_area == 8:
            lines_columns[3] = 6
            lines_columns[4] = 7
            lines_columns[5] = 8
    return lines_columns


def return_area(matrix, area_number):
    area_new = {
        0: matrix[0:3, 0:3].flatten(),
        1: matrix[0:3, 3:6].flatten(),
        2: matrix[0:3, 6:9].flatten(),
        3: matrix[3:6, 0:3].flatten(),
        4: matrix[3:6, 3:6].flatten(),
        5: matrix[3:6, 6:9].flatten(),
        6: matrix[6:9, 0:3].flatten(),
        7: matrix[6:9, 3:6].flatten(),
        8: matrix[6:9, 6:9].flatten()
    }

    return area_new.get(area_number, 'Invalid area!')


def return_area_number(matrix, number):
    position = 0
    areas = np.zeros(9, dtype=object)
    while position <= 8:
        if not return_if_pos_num(return_area(matrix, position), number):
            areas[position] = number
        position = position + 1
    return areas


def return_lines_number(matrix, number):
    position = 0
    lines = np.zeros(9, dtype=object)
    while position <= 8:
        if not return_if_pos_num(matrix[position], number):
            lines[position] = number
        position = position + 1
    return lines


def return_numbers_column(matrix, number):
    position = 0
    columns = np.zeros(9, dtype=object)
    while position <= 8:
        if not return_if_pos_num(return_column(matrix, position), number):
            columns[position] = number
        position = position + 1
    return columns


# Dont know yet
def cross_number_area_line_column(matrix, number):
    areas = return_area_number(matrix, number)
    lines = return_lines_number(matrix, number)
    columns = return_numbers_column(matrix, number)
    con = 0
    result_matrix = np.zeros((9, 9), dtype=object)
    result_matrix[0:9] = number
    while con <= 8:
        if lines[con] != number:
            result_matrix[con] = 0
        if columns[con] != number:
            c = 0
            while c < 9:
                result_matrix[c][con] = 0
                c = c + 1
        if areas[con] != number:
            lines_columns = return_line_column_area(con)
            result_matrix[lines_columns[0]][lines_columns[3]] = 0
            result_matrix[lines_columns[0]][lines_columns[4]] = 0
            result_matrix[lines_columns[0]][lines_columns[5]] = 0
            result_matrix[lines_columns[1]][lines_columns[3]] = 0
            result_matrix[lines_columns[1]][lines_columns[4]] = 0
            result_matrix[lines_columns[1]][lines_columns[5]] = 0
            result_matrix[lines_columns[2]][lines_columns[3]] = 0
            result_matrix[lines_columns[2]][lines_columns[4]] = 0
            result_matrix[lines_columns[2]][lines_columns[5]] = 0
        con = con + 1
    return result_matrix


# Dont know yet
def all_number_position(matrix):
    con = 0
    matrix_numbers = np.zeros(9, dtype=object)
    while con <= 8:
        matrix_numbers[con] = cross_number_area_line_column(matrix, con + 1)
        con = con + 1
    return matrix_numbers


# Dont know yet
def create_probabilities(matrix):
    result_matrix = np.zeros((9, 9), dtype=object)
    matrix_numbers = all_number_position(matrix)
    line = 0
    while line <= 8:
        column = 0
        while column <= 8:
            if matrix[line][column] == 0:
                con = 0
                array_prob = []
                while con <= 8:
                    if matrix_numbers[con][line][column] > 0:
                        array_prob.append(matrix_numbers[con][line][column])
                    con = con + 1
                result_matrix[line][column] = array_prob
            else:
                result_matrix[line][column] = matrix[line][column]
            column = column + 1
        line = line + 1
    return result_matrix


def verify_hidden_line_number(matrix, matrix_prob):
    line = 0
    execute_again = 0
    while line <= 8:
        new_line = verify_hidden_number(copy.deepcopy(matrix[line]), matrix_prob[line])
        if np.any(new_line != matrix[line]):
            execute_again = 1
            matrix[line] = new_line
        line = line + 1
    if execute_again == 1:
        matrix = execute_probabilities(copy.deepcopy(matrix))
    return matrix


def verify_hidden_column_number(matrix, matrix_prob):
    column = 0
    execute_again = 0
    while column <= 8:
        column_matrix = return_column(matrix, column)
        column_prob = return_column(matrix_prob, column)
        new_column = verify_hidden_number(copy.deepcopy(column_matrix), column_prob)
        if np.any(new_column != column_matrix):
            line = 0
            execute_again = 1
            while line <= 8:
                matrix[line][column] = new_column[line]
                line = line + 1
        column = column + 1
    if execute_again == 1:
        matrix = execute_probabilities(copy.deepcopy(matrix))
    return matrix


def verify_hidden_area_number(matrix, matrix_prob):
    area = 0
    execute_again = 0
    while area <= 8:
        area_matrix = return_area(matrix, area)
        area_prob = return_area(matrix_prob, area)
        new_area = verify_hidden_number(copy.deepcopy(area_matrix), area_prob)
        if np.any(new_area != area_matrix):
            execute_again = 1
            lines_columns = return_line_column_area(area)
            matrix[lines_columns[0]][lines_columns[3]] = new_area[0]
            matrix[lines_columns[0]][lines_columns[4]] = new_area[1]
            matrix[lines_columns[0]][lines_columns[5]] = new_area[2]
            matrix[lines_columns[1]][lines_columns[3]] = new_area[3]
            matrix[lines_columns[1]][lines_columns[4]] = new_area[4]
            matrix[lines_columns[1]][lines_columns[5]] = new_area[5]
            matrix[lines_columns[2]][lines_columns[3]] = new_area[6]
            matrix[lines_columns[2]][lines_columns[4]] = new_area[7]
            matrix[lines_columns[2]][lines_columns[5]] = new_area[8]
        area = area + 1
    if execute_again == 1:
        matrix = execute_probabilities(copy.deepcopy(matrix))
    return matrix


def verify_hidden_number(area, area_prob):
    column = 0
    amount_number = np.zeros(9, dtype=int)
    while column <= 8:
        if area[column] == 0:
            counter = 0
            while counter < len(area_prob[column]):
                amount_number[area_prob[column][counter] - 1] = amount_number[area_prob[column][counter] - 1] + 1
                counter = counter + 1
        column = column + 1
    c = 0
    while c <= 8:
        if amount_number[c] == 1:
            col_add = 0
            while col_add <= 8:
                if area[col_add] == 0:
                    con_add = 0
                    while con_add < len(area_prob[col_add]):
                        if area_prob[col_add][con_add] == c + 1:
                            area[col_add] = c + 1
                        con_add = con_add + 1
                col_add = col_add + 1
        c = c + 1
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
    line = 0
    probabilities = []
    result = np.zeros((9, 9), dtype=int)
    while line <= 8:
        column = 0
        while column <= 8:
            conLen = 0
            if matrix[line][column] == 0:
                while conLen < len(matrix_prob[line][column]):
                    con_resul = copy.deepcopy(matrix)
                    con_resul[line][column] = matrix_prob[line][column][conLen]
                    if is_valid_sudoku(con_resul):
                        con_resul = execute_probabilities(con_resul)
                        if is_valid_sudoku(con_resul):
                            if total_empty(con_resul) == 0:
                                return con_resul
                            else:
                                probabilities.append(con_resul)
                    conLen = conLen + 1
            column = column + 1
        line = line + 1
    c = 0
    con_empty = 81
    while c < len(probabilities):
        if is_valid_sudoku(probabilities[c]):
            if total_empty(probabilities[c]) < con_empty:
                result = probabilities[c]
        c = c + 1
    return result


# Main execute process
def execute_probabilities(matrix):
    matrix_prob = create_probabilities(matrix)
    line = 0
    execute_again = 0
    exist_one = 0
    matrix_result = copy.deepcopy(matrix)
    empty = np.zeros((9, 9), dtype=int)
    while line <= 8:
        column = 0
        while column <= 8:
            if matrix[line][column] == 0 and len(matrix_prob[line][column]) == 1:
                matrix_result[line][column] = matrix_prob[line][column][0]
                execute_again = 1
                exist_one = 1
            column = column + 1
        line = line + 1
    if execute_again == 1 and np.any(empty != matrix_result) and total_empty(matrix_result) > 0:
        control_matrix = execute_probabilities(copy.deepcopy(matrix_result))
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix
    if exist_one == 0 and np.any(empty != matrix_result) and total_empty(matrix_result) > 0:
        matrix_prob = create_probabilities(matrix_result)
        control_matrix = verify_hidden_line_number(matrix_result, matrix_prob)
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix
    if total_empty(matrix_result) > 0 and np.any(empty != matrix_result):
        matrix_prob = create_probabilities(matrix_result)
        control_matrix = verify_hidden_column_number(matrix_result, matrix_prob)
        if is_valid_sudoku(control_matrix):
            matrix_result = control_matrix
    if total_empty(matrix_result) > 0 and np.any(empty != matrix_result):
        matrix_prob = create_probabilities(matrix_result)
        control_matrix = verify_hidden_area_number(matrix_result, matrix_prob)
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
