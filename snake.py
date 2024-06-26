import random

import pygame


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 255, 255)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0 , 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

        self.walls = []
        self.walls.append(self.head)
   
    def moveAuto(self, key):  # use this move method when directions are generated by successor method
        # todo: feed only actions into moveAuto - successors will have state, action, cost
        # print(key)

        if key == "LEFT":
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "RIGHT":
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "UP":
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif key == "DOWN":
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    #def reset(self, pos):
        #self.head = cube(pos)
        #self.body = []
        #self.body.append(self.head)
        #self.turns = {}
        #self.dirnx = 0
        #self.dirny = 1

        #self.walls = self.body
        

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
            self.walls = self.body
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
            self.walls = self.body
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] -1)))
            self.walls = self.body
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
            self.walls = self.body

        global allWalls
        allWalls = self.body

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def isGoalState(self, current_pos):
        if current_pos == tempFood.pos:
            return True
        else:
            return False

    def getStartState(self):
        return self.head.pos

    def getSuccessors(self, current_pos):  # more like surrounding grid positions
        """returns a tuple of states, actions, costs"""

        '''Theoretically the max # of successors that can be generated at once should be 3: in front of the head,
        and the two sides of the head (if we have not eaten food yet we can have 4 successors). We will also make it so
        that the snake can not wrap around the screen.'''

        cost = 0
        wallPositions = []
        for x, wall in enumerate(self.walls):
            wallPositions.append(wall.pos)
        successors = []  # tuple of states, actions, cost (grid pos, direction to get there, cost to get there)
        x, y = current_pos
        possible_moves = [-1, 1]  # x or y can either stay, increase or decrease position by 1
        # print("Current pos (successor function):", current_pos)

        # look at successors for y axis
        for movesX in possible_moves:
            nextX = x + movesX  # x will move, y will stay the same
            nextY = y
            if nextX < 0 or nextX > 19:  # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            if nextState not in wallPositions:
                if nextState != current_pos:
                    if nextState not in successors:
                        directionX = ""
                        if movesX == 1:
                            directionX = "RIGHT"
                            cost = (euclideanCost(current_pos, tempFood.pos) / 2) # prioritize left and right actions
                        elif movesX == -1:
                            directionX = "LEFT"
                            cost = (euclideanCost(current_pos, tempFood.pos) / 2)
                        successors.append((nextState, directionX, cost))

        # look at successors for y axis
        for moves in possible_moves:
            nextX = x
            nextY = y + moves  # y will move, x will stay the same
            if nextY < 0 or nextY > 19:  # make sure we don't go out of bounds
                continue
            nextState = nextX, nextY
            if nextState not in wallPositions:
                if nextState != current_pos:
                    if nextState not in successors:
                        directionY = ""
                        if moves == 1:
                            directionY = "DOWN"
                            cost = euclideanCost(current_pos, tempFood.pos)
                        elif moves == -1:
                            directionY = "UP"
                            cost = euclideanCost(current_pos, tempFood.pos)
                        successors.append((nextState, directionY, cost))

        return successors


def euclideanCost(position, goal): # use a euclidean measurement to use as a cost
    xy1 = position
    xy2 = goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface, s):
    global rows, width, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)




def main():
    global width, rows, s, snack, startState
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = (10, 10)
    s = snake((255, 0, 0), startState)
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    global food, tempFood
    food = snack
    tempFood = snack
    flag = True
    clock = pygame.time.Clock()

    keyPresses = ["UP", "LEFT", "UP", "LEFT", "UP", "LEFT"]

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.moveAuto(keyPresses)
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))
            tempFood = food  # use this as testing to try to get food value before it changes
            food = snack  # update food to new value

        redrawWindow(win, s)

        # test line
        s.getSuccessors(s.head.pos)  # the head's position works as our current position
        s.isGoalState(s.head.pos)

def feedDirections(s):
    """feedDirections demonstrates how we can input a list of directions to feed into the game"""
    global width, rows, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    clock = pygame.time.Clock()
    flag = True

    directions = ["RIGHT", "UP", "RIGHT", "UP", "RIGHT", "UP", "LEFT", "LEFT"]

    for direction in directions:
        pygame.time.delay(50)
        clock.tick(10)
        s.moveAuto(direction)
        redrawWindow(win, s)

START_POS = (0, 0)
FOOD_POS = []
def foodPos():
    global FOOD_POS
    FOOD_POS= []
    for j in range(0, 399): # max num of food positions can be 400
        foodX = random.randrange(20)
        foodY = random.randrange(20)
        food = foodX, foodY
        FOOD_POS.append(food)

def dfs_search(s, i, slow):
    from util import Stack
    global width, rows, snack, tempFood, startState, food
    def performActions(dirs, slow):
        for action in dirs:
            if slow:
                pygame.time.delay(50)#delay between algorithms
                clock.tick(10)
                s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows =20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(0, 0, 128))
    tempFood = snack
    clock = pygame.time.Clock()
    

    dfs_stack = Stack()  
    visited = set()
    dfs_stack.push((s.getStartState(), []))

    while 1:
        if dfs_stack.isEmpty():
            break
        current, directions = dfs_stack.pop()
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.addCube()
                performActions(directions, slow)
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in dfs_stack.list:
                    if childNode in visited:
                        continue
                    dfs_stack.push((childNode, directions + [direction]))

def bfs_search(s, i, slow):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, slow):
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(255, 219, 164))
    tempFood = snack
    clock = pygame.time.Clock()
    

    bfs_queue = Queue() 
    visited = set()
    bfs_queue.push((s.getStartState(), []))

    while 1:
        if bfs_queue.isEmpty():
            break
        current, directions = bfs_queue.pop()
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.addCube()
                performActions(directions, slow)
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in bfs_queue.list:
                    if childNode in visited:
                        continue
                    bfs_queue.push((childNode, directions + [direction]))

def ucs_search(s, i, slow):
    from util import Queue
    global width, rows, snack, tempFood, startState, food

    def performActions(dirs, slow):
        for action in dirs:
            if slow:
                pygame.time.delay(50)
                clock.tick(10)
            s.moveAuto(action)
            redrawWindow(win, s)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    startState = START_POS
    snack = cube(FOOD_POS[i], color=(255, 153, 153))
    tempFood = snack
    clock = pygame.time.Clock()

    from util import PriorityQueue
    ucs_priorityqueue = PriorityQueue()  
    visited = set()
    ucs_priorityqueue.push((s.getStartState(), [], 0), 0)

    while 1:
        if ucs_priorityqueue.isEmpty():
            break

        current, directions, costs = ucs_priorityqueue.pop()  # add costs for ucs
        if current not in visited:
            visited.add(current)
            if s.isGoalState(current):
                s.addCube()
                performActions(directions, slow)
            for childNode, direction, cost in s.getSuccessors(current):
                if childNode not in ucs_priorityqueue.heap:
                    if childNode in visited:  # make sure child is not in visited so we don't go backwards
                        continue
                    ucs_priorityqueue.push((childNode, directions + [direction], costs + cost), costs + cost)
                    
def showExample():
    foodPos()
    mySnake = snake((255, 0, 0), START_POS)
    slow = True
    for i in range(0,2):
        dfs_search(mySnake, i, slow)
    #mySnake.reset(START_POS) 
    for i in range(2,10):
        ucs_search(mySnake, i, slow)
    #mySnake.reset(START_POS)    
    for i in range(10, 100):
        bfs_search(mySnake, i,slow)
    #mySnake.reset(START_POS)    
showExample()
