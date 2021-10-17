"""
MCTS starter code. This is the only file you'll need to modify, although
you can take a look at game1.py to get a sense of how the game is structured.

@author Bryce Wiedenbeck
@author Anna Rafferty (adapted from original)
@author Dave Musicant (adapted for Python 3 and other changes)
"""

'''Things implemented so far:
    - select()
    - Node.UCBValue()
    - Node.updateValue()'''

# These imports are used by the starter code.

# You will want to use this import in your code

# Whether to display the UCB rankings at each turn.
import random
import argparse
import game1
import math
DISPLAY_BOARDS = False

# UCB_CONST value - you should experiment with different values
UCB_CONST = .5


class Node(object):
    """Node used in MCTS"""

    def __init__(self, state, parent_node):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.state = state
        self.parent = parent_node
        # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.children = {}
        self.visits = 0
        self.value = 0
        # Note: you may add additional fields if needed

    def addMove(self, move):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move not in self.children:
            state = self.state.nextState(move)
            self.children[move] = Node(state, self)
            return True
        return False

    def getValue(self):
        """
        Gets the value estimate for the current node. Value estimates should correspond
        to the win percentage for the player at this node (accounting for draws as in 
        the project description).
        """
        return self.value

    def updateValue(self, outcome):
        """Updates the value estimate for the node's state.
        outcome: +1 for 1st player win, -1 for 2nd player win, 0 for draw."""
        "*** YOUR CODE HERE ***"
        wins = self.value * self.visits
        if outcome != self.state.getTurn(): # it was playing perfectly backwards before, so this is an 
            wins += 1                       # effective, albeit hacky, way to fix that
        self.visits += 1
        self.value = wins / self.visits

    def UCBValue(self):
        """Value from the UCB formula used by parent to select a child. """
        if self.visits == 0:
            return 1
        return self.value + UCB_CONST * math.sqrt(math.log(self.parent.visits) / self.visits)

def MCTS(root, rollouts):
    """Select a move by Monte Carlo tree search.
    Plays rollouts random games from the root node to a terminal state.
    In each rollout, play proceeds according to UCB while all children have
    been expanded. The first node with unexpanded children has a random child
    expanded. After expansion, play proceeds by selecting uniform random moves.
    Upon reaching a terminal state, values are propagated back along the
    expanded portion of the path. After all rollouts are completed, the move
    generating the highest value child of root is returned.
    Inputs:
        node: the node for which we want to find the optimal move
        rollouts: the number of root-leaf traversals to run
    Return:
        The legal move from node.state with the highest value estimate
    """
    for i in range(rollouts):
        node = root
        node = select(node)
        if not node.state.isTerminal():
            node = expand(node)
            outcome = random_playout(node)
        else:
            outcome = node.state.value()
        backpropagate(outcome, node, root)
    return bestValue(root)


def select(node):
    while not node.state.isTerminal() and len(node.children) == len(node.state.getMoves()):
        node = bestUCB(node)
    return node


def bestUCB(node):
    curr_best = (-1, None)
    for key in node.children.keys():
        child = node.children[key]
        if child.UCBValue() > curr_best[0]:
            curr_best = (child.UCBValue(), child)
    return curr_best[1]


def expand(node):
    moves = node.state.getMoves()
    for move in moves:
        if move not in node.children.keys():
            node.children[move] = Node(node.state.nextState(move), node)
            child = node.children[move]
            break
    return child


def random_playout(node):
    while not node.state.isTerminal():
        node = Node(node.state.nextState(random_move(node)), None) # no parent so that it's not connected to the tree
    return node.state.value()                                      # and gets garbage collected, since it's a temp node


def backpropagate(outcome, node, root):
    while True:
        node.updateValue(outcome)
        if node is root:
            break
        node = node.parent


def bestValue(node):
    curr_best = (-1, None)
    for key in node.children.keys():
        child = node.children[key]
        if child.value > curr_best[0]:
            curr_best = (child.value, key)
    return curr_best[1]


def parse_args():
    """
    Parse command line arguments.
    """
    p = argparse.ArgumentParser()
    p.add_argument("-r", "--rollouts", type=int, default=0, help="Number of root-to-leaf " +
                   "play-throughs that MCTS should run). Default=0 (random moves)")
    p.add_argument("-n", "--numGames", type=int, default=0, help="Number of games " +
                   "to play). Default=1")
    p.add_argument("-s", "--second", action="store_true", help="Set this flag to " +
                   "make your agent move second.")
    p.add_argument("-d", "--displayBoard", action="store_true", help="Set this flag to " +
                   "make display the board at each MCTS turn with MCTS's rankings of moves.")
    p.add_argument("-sa", "--rolloutsSecondMCTSAgent", type=int, default=0, help="If non-0, other player " +
                   "will also be an MCTS agent and will use the number of rollouts set with this " +
                   "argument. Default=0 (other player is random)")
    p.add_argument("-c", "--ucbConst", type=float, default=.5, help="Value for the UCB exploration " +
                   "constant. Default=.5")
    args = p.parse_args()
    if args.displayBoard:
        global DISPLAY_BOARDS
        DISPLAY_BOARDS = True
    global UCB_CONST
    UCB_CONST = args.ucbConst
    return args


def random_move(node):
    """
    Choose a valid move uniformly at random.
    """
    move = random.choice(node.state.getMoves())
    node.addMove(move)
    return move


def run_multiple_games(num_games, args):
    """
    Runs num_games games, with no printing except for a report on which game 
    number is currently being played, and reports final number
    of games won by player 1 and draws. args specifies whether player 1 or
    player 2 is MCTS and how many rollouts to use. For multiple games, you
    probably do not want to include the --displayBoard option in args, as
    this will do lots of printing and make running relatively slow.
    """
    player1GamesWon = 0
    draws = 0
    for i in range(num_games):
        print("Game " + str(i))
        node = play_game(args)
        winner = node.state.value()
        if winner == 1:
            player1GamesWon += 1
        elif winner == 0:
            draws += 1
    print("Player 1 games won: " + str(player1GamesWon) + "/" + str(num_games))
    print("Draws: " + str(draws) + "/" + str(num_games))


def play_game(args):
    """
    Play one game against another player.
    args specifies whether player 1 or player 2 is MCTS (
    or both if rolloutsSecondMCTSAgent is non-zero)
    and how many rollouts to use.
    Returns the final terminal node for the game.
    """
    # Make start state and root of MCTS tree
    start_state = game1.new_game()
    root1 = Node(start_state, None)
    if args.rolloutsSecondMCTSAgent != 0:
        root2 = Node(start_state, None)

    # Run MCTS
    node = root1
    if args.rolloutsSecondMCTSAgent != 0:
        node2 = root2
    while not node.state.isTerminal():
        if (not args.second and node.state.turn == 1) or \
                (args.second and node.state.turn == -1):
            move = MCTS(node, args.rollouts)
            if DISPLAY_BOARDS:
                print(game1.show_values(node))
        else:
            if args.rolloutsSecondMCTSAgent == 0:
                move = random_move(node)
            else:
                move = MCTS(node2, args.rolloutsSecondMCTSAgent)
                if DISPLAY_BOARDS:
                    print(game1.show_values(node2))
        node.addMove(move)
        node = node.children[move]
        if args.rolloutsSecondMCTSAgent != 0:
            node2.addMove(move)
            node2 = node2.children[move]
    return node


def main():
    """
    Play a game of connect 4, using MCTS to choose the moves for one of the players.
    args on command line set properties; see parse_args() for details.
    """
    # Get commandline arguments
    args = parse_args()

    if args.numGames > 1:
        run_multiple_games(args.numGames, args)
    else:
        # Play the game
        node = play_game(args)

        # Print result
        winner = node.state.value()
        print(game1.print_board(node.state))
        if winner == 1:
            print("Player 1 wins")
        elif winner == -1:
            print("Player 2 wins")
        else:
            print("It's a draw")


if __name__ == "__main__":
    main()
