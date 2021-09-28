from search import *
from time import time
from sys import argv

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