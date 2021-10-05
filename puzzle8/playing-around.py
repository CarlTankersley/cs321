from search import *
from time import time
import argparse

def nilsson(state):
    order = [0, 1, 2, 5, 8, 7, 6, 3, 4]
    score = 0
    for i in range(1, 8):
        if p8.getTile(state, order[i]) - p8.getTile(state, order[i-1]) != 1:
            score += 2
    if p8.getTile(state, 4) != 0:
        score += 1
    score *= 3
    score += manhattanDistance(state)
    return score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--state", nargs='*', type=int)
    args = parser.parse_args()
    if args.state is None:
        puzzle = p8.randomState()
    elif len(args.state) == 9:
        puzzle = p8.state(args.state)
    else:
        exit(f"Error: Incorrect number of arguments ({len(args.state)})")
    for i in range(3):
        row = ""
        for j in range(3):
            row += (str(p8.getTile(puzzle,3*i+j)) + " ")
        print(row)
    start = time()
    path = astar(puzzle, manhattanDistance)
    timeElapsed = time() - start
    print("Solution path: " + str(path))
    print("Length = " + str(len(path)))
    print("Time = " + str(timeElapsed))

if __name__ == "__main__":
    main()