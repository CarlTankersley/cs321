import othelloBoard
from typing import Tuple, Optional
import sys

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

minint = -sys.maxsize - 1

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print('Illegal entry, try again.')
            except Exception:
                print('Illegal entry, try again.')

        if move==(0,0):
            return None
        else:
            return move

   
def heuristic(board) -> int:
    '''This very silly heuristic just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    # return len(board._legalMoves(1)) - len(board._legalMoves(-1))
    positiveSum = 0
    negativeSum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            if board.array[i][j] == 1:
                positiveSum += 1
                if (i == 0 or i == 7) and (j == 0 or j == 7):
                    positiveSum += 99
                if (i == 1 or i == 6) or (j == 1 or j == 6):
                    positiveSum -= 2
            elif board.array[i][j] == -1:
                negativeSum += 1
                if (i == 0 or i == 7) and (j == 0 or j == 7):
                    negativeSum += 99
                if (i == 1 or i == 6) or (j == 1 or j == 6):
                    negativeSum -= 2
    # return len(board._legalMoves(1)) - len(board._legalMoves(-1)) + positiveSum ** 2 / 128 - negativeSum ** 2 / 128
    return positiveSum / (len(board._legalMoves(-1)) or .001) - negativeSum / (len(board._legalMoves(1)) or .001)
    

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies) -> None:
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies
        self.numHeuristicCalls = 0

    # chooseMove should return a tuple that looks like:
    # (row of move, column of move, number of times heuristic was called)
    # We will be using the third piece of information to assist with grading.
    def chooseMove(self,board) -> Optional[Tuple[int,int,int]]:
        '''This very silly player just returns the first legal move
        that it finds.'''
        # for i in range(1,othelloBoard.size-1):
        #     for j in range(1,othelloBoard.size-1):
        #         bcopy = board.makeMove(i,j,self.color)
        #         if bcopy:
        #             print('Heuristic value = ' + str(self.heuristic(bcopy)))
        #             numHeuristicCalls += 1
        #             return (i,j,numHeuristicCalls)

        moves = board._legalMoves(self.color)
        curr_best = (minint * self.color, (-1, -1))
        for move in moves:
            curr_minimax = self.minimax(board.makeMove(move[0], move[1], self.color), self.plies * 2, -self.color)
            if curr_minimax*self.color > curr_best[0]*self.color:
                curr_best = (curr_minimax, move)
        if curr_best[0] != minint * self.color:
            return (curr_best[1][0], curr_best[1][1], self.numHeuristicCalls)
        # None is considered a pass
        return None

    def minimax(self, board, depth_remaining, color):
        moves = board._legalMoves(color)
        if depth_remaining == 0 or len(moves) == 0:
            self.numHeuristicCalls += 1
            return self.heuristic(board)
        curr_best = minint * color
        for move in moves:
            curr_best = color * max(curr_best * color, self.minimax(board.makeMove(move[0], move[1], color), depth_remaining - 1, -1 * color) * color)
        return curr_best
    