from search import *
from time import time
from sys import argv

def nilsson(state):
    order = [0, 1, 2, 5, 8, 7, 6, 3, 4]
    score = 0
    for i in range(1, 8):
        if p8.getTile(state, order[i]) - p8.getTile(state, order[i-1]) != 1:
            score += 2
    if p8.getTile(state, 4) != 0:
        score += 1
    return score

def main():
    if len(argv) == 1:
        puzzle = p8.randomState()
    else:
        for i in range(1, len(argv)):
            argv[i] = int(argv[i])
        puzzle = p8.state(argv[1:10])
    for i in range(3):
        row = ""
        for j in range(3):
            row += (str(p8.getTile(puzzle,3*i+j)) + " ")
        print(row)
    start = time()
    path = astar(puzzle, manhattanDistance)
    timeElapsed = time() - start
    print("Solution path: " + str(path) + ", length = " + str(len(path)))
    print("Time = " + str(timeElapsed))

if __name__ == "__main__":
    main()