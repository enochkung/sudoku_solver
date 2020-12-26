# sudoku solver

import pygame


def solve(board1):
    # board = board1.copy()
    # search for the first zero digit
    # run through possible digits from 1-9
    # check if valid, then solve new board
    # if not valid then go to next digit

    X = [
        (i, j)
        for i in range(len(board))
        for j in range(len(board[i]))
        if board[i][j] == 0
    ]

    if not X:
        return True

    x_index, y_index = X[0]

    for test in range(1, 10):
        if check_valid(board, (x_index, y_index), test):
            # board2 = board.copy()
            board[x_index][y_index] = test
            solution = solve(board)

            if solution:
                return True
            board[x_index][y_index] = 0
    return False


def check_valid(board, index, value):
    # for the index, check column, row and group of nine
    if (
        value in [board[index[0]][index[1]] for index in get_row(index)]
        or value in [board[index[0]][index[1]] for index in get_col(index)]
        or value in [board[index[0]][index[1]] for index in get_nine_group(index)]
    ):
        return False
    else:
        return True


def get_row(index):
    return [(index[0], j) for j in range(9) if j != index[1]]


def get_col(index):
    return [(i, index[1]) for i in range(9) if i != index[0]]


def get_nine_group(index):
    X = [
        (int(index[0] / 3) * 3 + i, int(index[1] / 3) * 3 + j)
        for i in range(3)
        for j in range(3)
    ]
    X.remove(index)
    return X


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0:
            print("-------------------------")
        for j in range(9):
            if j % 3 == 0:
                print("| ", end="")
            print(str(board[i][j]) + " ", end="")
            if j == 8:
                print("|")
    print("-------------------------")
    pass


board = [
    [0, 0, 0, 0, 7, 8, 0, 4, 0],
    [2, 0, 1, 0, 6, 0, 0, 7, 0],
    [0, 0, 0, 1, 5, 0, 8, 3, 0],
    [0, 0, 8, 0, 0, 0, 4, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 5, 0, 0, 0, 1, 0, 0],
    [0, 6, 7, 0, 9, 2, 0, 0, 0],
    [0, 5, 0, 0, 1, 0, 7, 0, 9],
    [0, 1, 0, 6, 3, 0, 0, 0, 0],
]

solve(board)
print(print_board(board))
