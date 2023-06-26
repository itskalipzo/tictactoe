"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY] * 3 for _ in range(3)]  # List comprehension to create 3x3 matrix


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)

    # If count of X is greater than O, it means O's turn
    if count_X > count_O:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action.")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Combine all possible winning lines into one list
    win_positions = [
                        [board[i][j] for j in range(3)] for i in range(3)] + \
                    [[board[i][j] for i in range(3)] for j in range(3)] + \
                    [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]
                     ]

    # If any winning line is all X or all O, declare that as winner
    for line in win_positions:
        if line.count(X) == 3:
            return X
        elif line.count(O) == 3:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        move = None
        for action in actions(board):
            min_val_result = min_value(result(board, action), alpha, beta)[0]
            if min_val_result > v:
                v = min_val_result
                move = action
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v = math.inf
        move = None
        for action in actions(board):
            max_val_result = max_value(result(board, action), alpha, beta)[0]
            if max_val_result < v:
                v = max_val_result
                move = action
            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move

    return max_value(board, -math.inf, math.inf)[1] if player(board) == X else min_value(board, -math.inf, math.inf)[1]
