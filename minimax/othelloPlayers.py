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
    '''Determines the quality of a move by how much it increases the player's number of legal moves and decreases
    the opponent's number of legal moves.'''
    return 1/(len(board._legalMoves(1))+1) - 1/(len(board._legalMoves(-1))+1)
    
    

class ComputerPlayerMinimax:
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
        
        self.numHeuristicCalls = 0
        moves = board._legalMoves(self.color)
        curr_best = (minint * self.color, (-1, -1))
        for move in moves:
            curr_minimax = self.minimax(board.makeMove(move[0], move[1], self.color), self.plies, -self.color)
            if curr_minimax*self.color > curr_best[0]*self.color:
                curr_best = (curr_minimax, move)
        if curr_best[0] != minint * self.color:
            return (curr_best[1][0], curr_best[1][1], self.numHeuristicCalls)        
        # None is considered a pass
        return None

    def minimax(self, board, depth_remaining, color):
        if depth_remaining <= 0:
            self.numHeuristicCalls += 1
            return self.heuristic(board)
        moves = board._legalMoves(color)
        if len(moves) == 0:
            self.numHeuristicCalls += 1
            return self.heuristic(board)
        if color == 1:
            best_move = minint
            for move in moves:
                best_move = max(best_move, self.minimax(board.makeMove(move[0], move[1], color), depth_remaining - 1, -1))
        elif color == -1:
            best_move = sys.maxsize
            for move in moves:
                best_move = min(best_move, self.minimax(board.makeMove(move[0], move[1], color), depth_remaining - 1, 1))
        return best_move

    
class ComputerPlayer:
    def __init__(self,name,color,heuristic,plies) -> None:
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies
        self.numHeuristicCalls = 0


    def chooseMove(self,board) -> Optional[Tuple[int,int,int]]:
        self.numHeuristicCalls = 0
        curr_best = (minint * self.color, (-1, -1))
        moves = board._legalMoves(self.color)
        for move in moves:
            curr_option = self.alphabeta(board.makeMove(move[0], move[1], self.color), self.plies-1, minint, sys.maxsize, self.color)
            if curr_option*self.color > curr_best[0]*self.color:
                curr_best = (curr_option, move)
        if curr_best[0] != minint * self.color:
            return (curr_best[1][0], curr_best[1][1], self.numHeuristicCalls)  
        # None is considered a pass
        return None

    def alphabeta(self, board, depth_remaining, alpha, beta, color):
        if depth_remaining == 0:
            self.numHeuristicCalls += 1
            return self.heuristic(board)
        moves = board._legalMoves(color)
        if len(moves) == 0:
            self.numHeuristicCalls += 1
            return self.heuristic(board)
        if color == 1:
            value = minint
            for move in moves:
                value = max(value, self.alphabeta(board.makeMove(move[0], move[1], color), depth_remaining - 1, alpha, beta, -1))
                if value >= beta:
                    break
                alpha = max(alpha, value)
        elif color == -1:
            value = sys.maxsize
            for move in moves:
                value = min(value, self.alphabeta(board.makeMove(move[0], move[1], color), depth_remaining - 1, alpha, beta, 1))
                if value <= alpha:
                    break
                beta = min(beta, value)
        return value

        