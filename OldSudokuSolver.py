# coding: utf-8
import numpy as np
import copy


def totalEmpty(matrix):
    line = 0
    counter = 0
    while (line <= 8):
        column = 0
        while (column <= 8):
            if (matrix[line][column] == 0):
                counter = counter + 1
            column = column + 1
        line = line + 1
    return counter


def returnIfPosNum(pos, number):
    position = 0
    numberPosition = 'false'
    while (position < len(pos)):
        if (pos[position] == number):
            numberPosition = 'true'
            break
        position = position + 1
    return numberPosition


def returnColumn(matrix, column):
    return [row[column] for row in matrix]


def returnLineColumnArea(numArea):
    linescolumns = np.zeros(9, dtype=object)
    linescolumns[0] = 0
    linescolumns[1] = 1
    linescolumns[2] = 2
    linescolumns[3] = 0
    linescolumns[4] = 1
    linescolumns[5] = 2
    if (numArea == 1):
        linescolumns[3] = 3
        linescolumns[4] = 4
        linescolumns[5] = 5
    elif (numArea == 2):
        linescolumns[3] = 6
        linescolumns[4] = 7
        linescolumns[5] = 8
    elif (numArea == 3 or numArea == 4 or numArea == 5):
        linescolumns[0] = 3
        linescolumns[1] = 4
        linescolumns[2] = 5
        if (numArea == 4):
            linescolumns[3] = 3
            linescolumns[4] = 4
            linescolumns[5] = 5
        elif (numArea == 5):
            linescolumns[3] = 6
            linescolumns[4] = 7
            linescolumns[5] = 8
    elif (numArea == 6 or numArea == 7 or numArea == 8):
        linescolumns[0] = 6
        linescolumns[1] = 7
        linescolumns[2] = 8
        if (numArea == 7):
            linescolumns[3] = 3
            linescolumns[4] = 4
            linescolumns[5] = 5
        elif (numArea == 8):
            linescolumns[3] = 6
            linescolumns[4] = 7
            linescolumns[5] = 8
    return linescolumns


def returnArea(matrix, areaNum):
    linescolumns = returnLineColumnArea(areaNum)
    area = np.zeros(9, dtype=object)
    area[0] = matrix[linescolumns[0]][linescolumns[3]]
    area[1] = matrix[linescolumns[0]][linescolumns[4]]
    area[2] = matrix[linescolumns[0]][linescolumns[5]]
    area[3] = matrix[linescolumns[1]][linescolumns[3]]
    area[4] = matrix[linescolumns[1]][linescolumns[4]]
    area[5] = matrix[linescolumns[1]][linescolumns[5]]
    area[6] = matrix[linescolumns[2]][linescolumns[3]]
    area[7] = matrix[linescolumns[2]][linescolumns[4]]
    area[8] = matrix[linescolumns[2]][linescolumns[5]]
    return area


def returnAreaNumber(matrix, number):
    position = 0
    areas = np.zeros(9, dtype=object)
    while (position <= 8):
        if (returnIfPosNum(returnArea(matrix, position), number) == 'false'):
            areas[position] = number
        position = position + 1
    return areas


def returnLinesNumber(matrix, number):
    position = 0
    lines = np.zeros(9, dtype=object)
    while (position <= 8):
        if (returnIfPosNum(matrix[position], number) == 'false'):
            lines[position] = number
        position = position + 1
    return lines


def returnNumbersColumn(matrix, number):
    position = 0
    columns = np.zeros(9, dtype=object)
    while (position <= 8):
        if (returnIfPosNum(returnColumn(matrix, position), number) == 'false'):
            columns[position] = number
        position = position + 1
    return columns


def crossNumberAreaLineColumn(matrix, number):
    areas = returnAreaNumber(matrix, number)
    lines = returnLinesNumber(matrix, number)
    columns = returnNumbersColumn(matrix, number)
    con = 0
    matrixNumber = np.zeros((9, 9), dtype=object)
    matrixNumber[0:9] = number
    while (con <= 8):
        if (lines[con] != number):
            matrixNumber[con] = 0
        if (columns[con] != number):
            c = 0
            while (c < 9):
                matrixNumber[c][con] = 0
                c = c + 1
        if (areas[con] != number):
            linescolumns = returnLineColumnArea(con)
            matrixNumber[linescolumns[0]][linescolumns[3]] = 0
            matrixNumber[linescolumns[0]][linescolumns[4]] = 0
            matrixNumber[linescolumns[0]][linescolumns[5]] = 0
            matrixNumber[linescolumns[1]][linescolumns[3]] = 0
            matrixNumber[linescolumns[1]][linescolumns[4]] = 0
            matrixNumber[linescolumns[1]][linescolumns[5]] = 0
            matrixNumber[linescolumns[2]][linescolumns[3]] = 0
            matrixNumber[linescolumns[2]][linescolumns[4]] = 0
            matrixNumber[linescolumns[2]][linescolumns[5]] = 0
        con = con + 1
    return matrixNumber


def allNumbersPosition(matrix):
    con = 0
    matrixNumbers = np.zeros(9, dtype=object)
    while (con <= 8):
        matrixNumbers[con] = crossNumberAreaLineColumn(matrix, con + 1)
        con = con + 1
    return matrixNumbers


def createProbabilitys(matrix):
    matrixProb = np.zeros((9, 9), dtype=object)
    matrixNumbers = allNumbersPosition(matrix)
    line = 0
    while (line <= 8):
        column = 0
        while (column <= 8):
            if (matrix[line][column] == 0):
                con = 0
                arrayProb = []
                while (con <= 8):
                    if (matrixNumbers[con][line][column] > 0):
                        arrayProb.append(matrixNumbers[con][line][column])
                    con = con + 1
                matrixProb[line][column] = arrayProb
            else:
                matrixProb[line][column] = matrix[line][column]
            column = column + 1
        line = line + 1
    return matrixProb


def verifyHiddenLineNumber(matrix, matrixProb):
    line = 0
    executeAgain = 0
    while (line <= 8):
        newLine = verifyHiddenNumber(copy.deepcopy(matrix[line]), matrixProb[line])
        if (np.any(newLine != matrix[line])):
            executeAgain = 1
            matrix[line] = newLine
        line = line + 1
    if (executeAgain == 1):
        matrix = executeProbabilities(copy.deepcopy(matrix))
    return matrix


def verifyHiddenColumnNumber(matrix, matrixProb):
    column = 0
    executeAgain = 0
    while (column <= 8):
        columnmatrix = returnColumn(matrix, column)
        columnProb = returnColumn(matrixProb, column)
        newColumn = verifyHiddenNumber(copy.deepcopy(columnmatrix), columnProb)
        if (np.any(newColumn != columnmatrix)):
            line = 0
            executeAgain = 1
            while (line <= 8):
                matrix[line][column] = newColumn[line]
                line = line + 1
        column = column + 1
    if (executeAgain == 1):
        matrix = executeProbabilities(copy.deepcopy(matrix))
    return matrix


def verifyHiddenAreaNumber(matrix, matrixProb):
    area = 0
    executeAgain = 0
    while (area <= 8):
        areaMatrix = returnArea(matrix, area)
        areaProb = returnArea(matrixProb, area)
        newArea = verifyHiddenNumber(copy.deepcopy(areaMatrix), areaProb)
        if (np.any(newArea != areaMatrix)):
            executeAgain = 1
            linescolumns = returnLineColumnArea(area)
            matrix[linescolumns[0]][linescolumns[3]] = newArea[0]
            matrix[linescolumns[0]][linescolumns[4]] = newArea[1]
            matrix[linescolumns[0]][linescolumns[5]] = newArea[2]
            matrix[linescolumns[1]][linescolumns[3]] = newArea[3]
            matrix[linescolumns[1]][linescolumns[4]] = newArea[4]
            matrix[linescolumns[1]][linescolumns[5]] = newArea[5]
            matrix[linescolumns[2]][linescolumns[3]] = newArea[6]
            matrix[linescolumns[2]][linescolumns[4]] = newArea[7]
            matrix[linescolumns[2]][linescolumns[5]] = newArea[8]
        area = area + 1
    if (executeAgain == 1):
        matrix = executeProbabilities(copy.deepcopy(matrix))
    return matrix


def verifyHiddenNumber(area, areaProb):
    column = 0
    amountNumber = np.zeros(9, dtype=int)
    while (column <= 8):
        if (area[column] == 0):
            counter = 0
            while (counter < len(areaProb[column])):
                amountNumber[areaProb[column][counter] - 1] = amountNumber[areaProb[column][counter] - 1] + 1
                counter = counter + 1
        column = column + 1
    c = 0
    while (c <= 8):
        if (amountNumber[c] == 1):
            colAdd = 0
            while (colAdd <= 8):
                if (area[colAdd] == 0):
                    conAdd = 0
                    while (conAdd < len(areaProb[colAdd])):
                        if (areaProb[colAdd][conAdd] == c + 1):
                            area[colAdd] = c + 1
                        conAdd = conAdd + 1
                colAdd = colAdd + 1
        c = c + 1
    return area


def isValidSudoku(matrix):
    line = 0
    if (totalEmpty(matrix) == 81):
        return 0
    while (line <= 8):
        totNumLine = np.zeros(9, dtype=int)
        col = 0
        while (col <= 8):
            if (matrix[line][col] > 0):
                totNumLine[matrix[line][col] - 1] = totNumLine[matrix[line][col] - 1] + 1
                if (totNumLine[matrix[line][col] - 1] > 1):
                    return 0
            col = col + 1
        line = line + 1
    col = 0
    while (col <= 8):
        totNumCol = np.zeros(9, dtype=int)
        column = returnColumn(matrix, col)
        conCol = 0
        while (conCol <= 8):
            if (column[conCol] > 0):
                totNumCol[column[conCol] - 1] = totNumCol[column[conCol] - 1] + 1
                if (totNumCol[column[conCol] - 1] > 1):
                    return 0
            conCol = conCol + 1
        col = col + 1
    a = 0
    while (a <= 8):
        totNumArea = np.zeros(9, dtype=int)
        area = returnArea(matrix, a)
        conCol = 0
        while (conCol <= 8):
            if (area[conCol] > 0):
                totNumArea[area[conCol] - 1] = totNumArea[area[conCol] - 1] + 1
                if (totNumArea[area[conCol] - 1] > 1):
                    return 0
            conCol = conCol + 1
        a = a + 1
    return 1


def executeMultipleProbabilities(matrix, matrixProb):
    line = 0
    probabilities = []
    result = np.zeros((9, 9), dtype=int)
    while (line <= 8):
        column = 0
        while (column <= 8):
            conLen = 0
            if (matrix[line][column] == 0):
                while (conLen < len(matrixProb[line][column])):
                    conResul = copy.deepcopy(matrix)
                    conResul[line][column] = matrixProb[line][column][conLen]
                    if (isValidSudoku(conResul) == 1):
                        conResul = executeProbabilities(conResul)
                        if (isValidSudoku(conResul) == 1):
                            if (totalEmpty(conResul) == 0):
                                return conResul
                            else:
                                probabilities.append(conResul)
                    conLen = conLen + 1
            column = column + 1
        line = line + 1
    c = 0
    conEmpty = 81
    while (c < len(probabilities)):
        if (isValidSudoku(probabilities[c]) == 1):
            if (totalEmpty(probabilities[c]) < conEmpty):
                result = probabilities[c]
        c = c + 1
    return result


def executeProbabilities(matrix):
    matrixProb = createProbabilitys(matrix)
    line = 0
    executeAgain = 0
    existOne = 0
    matrixResult = copy.deepcopy(matrix)
    empty = np.zeros((9, 9), dtype=int)
    while (line <= 8):
        column = 0
        while (column <= 8):
            if (matrix[line][column] == 0 and len(matrixProb[line][column]) == 1):
                matrixResult[line][column] = matrixProb[line][column][0]
                executeAgain = 1
                existOne = 1
            column = column + 1
        line = line + 1
    if (executeAgain == 1 and np.any(empty != matrixResult) and totalEmpty(matrixResult) > 0):
        controlMatrix = executeProbabilities(copy.deepcopy(matrixResult))
        if (isValidSudoku(controlMatrix) == 1):
            matrixResult = controlMatrix
    if (existOne == 0 and np.any(empty != matrixResult) and totalEmpty(matrixResult) > 0):
        matrixProb = createProbabilitys(matrixResult)
        controlMatrix = verifyHiddenLineNumber(matrixResult, matrixProb)
        if (isValidSudoku(controlMatrix) == 1):
            matrixResult = controlMatrix
    if (totalEmpty(matrixResult) > 0 and np.any(empty != matrixResult)):
        matrixProb = createProbabilitys(matrixResult)
        controlMatrix = verifyHiddenColumnNumber(matrixResult, matrixProb)
        if (isValidSudoku(controlMatrix) == 1):
            matrixResult = controlMatrix
    if (totalEmpty(matrixResult) > 0 and np.any(empty != matrixResult)):
        matrixProb = createProbabilitys(matrixResult)
        controlMatrix = verifyHiddenAreaNumber(matrixResult, matrixProb)
        if (isValidSudoku(controlMatrix) == 1):
            matrixResult = controlMatrix
    if (totalEmpty(matrixResult) > 0 and np.any(empty != matrixResult)):
        matrixProb = createProbabilitys(matrixResult)
        controlMatrix = executeMultipleProbabilities(copy.deepcopy(matrixResult), matrixProb)
        if (np.any(controlMatrix != matrixResult) and np.any(empty != controlMatrix)):
            matrixResult = controlMatrix
            if (totalEmpty(matrixResult) > 0):
                matrixResult = executeProbabilities(matrixResult)
    return matrixResult
