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
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turncount = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                turncount += 1
    
    if board == initial_state():
        return X
    if turncount % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #create possible move array
    possiblemoves = set()
    for i in range(3):
       for j in range(3):
           if board[i][j] == EMPTY:
               possiblemoves.add((i,j))
    
    return possiblemoves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """    
    
    #check for out-of-bounds move
    (x,y) = action
    if x < 0 or x > 2:
        raise Exception("error")
    elif y < 0 or y > 2:
        raise Exception("error")
    
    #check for taken move
    #for i in range(3):
       #for j in range(3):
           #if board[i][j] != EMPTY:
            #raise Exception("error")
    
    #copy original board
    result = copy.deepcopy(board)
    
    #apply action to board
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check vertically
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
    
    #check horizontally
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
    
    #check diagnals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #check for winner
    if (winner(board) == X):
        return True
    elif (winner(board) == O):
        return True
        
    #check if all squares have been taken
    for i in range(3):
        for j in range(3):
            if  board[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #check for winner
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    #if no winner
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #check terminal board
    if (terminal(board) == True):
        return None

    Max = float("-inf")
    Min = float("inf")

    if player(board) == X:
        return Max_Value(board, Max, Min)[1]
    else:
        return Min_Value(board, Max, Min)[1]

def Max_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None]
    
    v = float('-inf')
    for action in actions(board):
        test = Min_Value(result(board, action), Max, Min)[0]
        Max = max(Max, test)
        if test > v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]

def Min_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None]
    
    v = float('inf')
    for action in actions(board):
        test = Max_Value(result(board, action), Max, Min)[0]
        Min = min(Min, test)
        if test < v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move]