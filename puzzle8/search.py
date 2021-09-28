import puzzle8 as p8
import heapq as pq # for "Priority Queue"

def numWrongTiles(state):
    numWrong = 0
    for i in range(9):
        if p8.getTile(state, i) != p8.getTile(p8.solution(), i) and p8.getTile(state, i) != 0:
            numWrong += 1
    return numWrong


def manhattanDistance(state):
    distance = 0
    soln = [(),    # Locations of the tiles in the solution state
            (0,0),
            (1,0),
            (2,0),
            (2,1),
            (2,2),
            (1,2),
            (0,2),
            (0,1)]
    for i in range(9):
        tile = p8.getTile(state, i)
        location = p8.xylocation(i)
        if tile != 0:
            distance += abs(location[0] - soln[tile][0]) + abs(location[1] - soln[tile][1])        
    return distance

def itdeep(state):
    path = None
    count = 0
    while path is None:
        path = DFS(state, count)
        count += 1
    return path
    
def DFS(state, maxDepth):
    stack = [(state, 0)]
    path = []
    for i in range(maxDepth):
        path.append(0)
    currentDepth = 0
    while len(stack) > 0:
        currentNode = stack.pop()
        currentDepth = currentNode[1]
        if currentDepth > 0:
            path[currentDepth-1] = currentNode[0]
        if currentDepth < maxDepth:
            children = findChildren(currentNode[0])
            currentDepth += 1
            for child in children:
                if child == p8.solution():
                    path[currentDepth-1] = child
                    return path
                else:
                    stack.append((child, currentDepth))
    return None

def findChildren(state):
    for i in range(9):
        if p8.getTile(state, i) == 0:
            square = i
            break
    neighbors = p8.neighbors(square)
    children = []
    for neighbor in neighbors:
        children.append(p8.moveBlank(state, neighbor))
    return children

def astar(state, heuristic):
    queue = [(heuristic(state), Node(state, heuristic(state), 0, []))]
    while len(queue) > 0:
        currentNode = pq.heappop(queue)[1]
        if currentNode.state == p8.solution():
            break
        children = astarFindChildren(currentNode, heuristic)
        for child in children:
            pq.heappush(queue, (currentNode.depth+1+child.heuristic, child))
    return currentNode.path

def astarFindChildren(parent, heuristic):
    zeroLocation = p8.blankSquare(parent.state)
    neighbors = p8.neighbors(zeroLocation)
    children = []
    for neighbor in neighbors:
        newState = p8.moveBlank(parent.state, neighbor)
        childZero = p8.blankSquare(newState)
        newPath = parent.path.copy()
        newPath.append(childZero)
        child = Node(newState, heuristic(newState), parent.depth+1, newPath)
        children.append(child)
    return children

class Node:
    def __init__(self, state, heuristic, depth, path):
        self.state = state
        self.heuristic = heuristic
        self.depth = depth
        self.path = path
        
    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)

    def __str__(self):
        return f"state = {self.state}, heuristic = {self.heuristic}, depth = {self.depth}, path = {self.path}"
