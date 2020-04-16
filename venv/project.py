import pygame
import sys
import math
import os
from tkinter import *
from tkinter import messagebox


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
startNode = None
endNode = None
columns = SCREEN_WIDTH//20
rows = SCREEN_HEIGHT//20
gridNodes = [[0 for i in range(columns + 1)] for j in range(rows + 1)]
found = False


class Node:

    def __init__(self, x, y, obstacle):

        self._x = x
        self._y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.closed = False
        self.predecessor = None
        self._obstacle = obstacle
        self.children = []


    def getX(self):

        return self._x


    def getY(self):

        return self._y


    def draw(self, color, border, blockSize = 20):

        if self.closed is False:
            node = pygame.Rect(self._x * blockSize, self._y * blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, color, node, border)
            pygame.display.update()


    def findChildren(self, nodeGrid):
        
        column = self._x
        row = self._y
        if (nodeGrid[row + 1][column]._obstacle is False) and (row < rows):
             self.children.append(nodeGrid[row + 1][column])
        if (nodeGrid[row - 1][column]._obstacle is False) and (row > 0):
            self.children.append(nodeGrid[row - 1][column])
        if (nodeGrid[row][column + 1]._obstacle is False) and (column < columns):
            self.children.append(nodeGrid[row][column + 1])
        if (nodeGrid[row][column - 1]._obstacle is False) and (column > 0):
            self.children.append(nodeGrid[row][column - 1])


root = Tk()
root.withdraw()


def setup():

    os.environ['SDL_VIDEO_CENTERED'] = '1' #da bi se centrirao ekran
    pygame.init()
    global SCREEN
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=0, depth=32)
    surface = pygame.Surface(SCREEN.get_size())
    surface = surface.convert()
    pygame.display.set_caption('Path finder')
    surface.fill((0, 0, 0))


def draw_grid():

    blockSize = 20
    for x in range(rows):
        for y in range(columns):
            rect = Node(y * blockSize, x * blockSize, False)
            gridNodes.append(rect)
            rect.draw((0, 0, 0), 1)
    pygame.display.update()


for x in range(rows + 1):
    for y in range(columns + 1):
        gridNodes[x][y] = Node(y, x, False)


def distance(start, end):

    x = start.getX() - end.getX()
    y = start.getY() - end.getY()
    return math.sqrt(x**2 + y**2)


def mousePressed(position):

    x = position[0]
    y = position[1]
    y1 = x // 20
    x1 = y // 20
    entry = gridNodes[x1][y1]
    global startNode
    global endNode
    if startNode is None:
        startNode = entry
        startNode.draw((63, 104, 28), 0)
    elif endNode is None:
        endNode = entry
        if distance(startNode, endNode) != 0:
            endNode.draw((244, 47, 8), 0)
        else:
            endNode = None
    elif (startNode is not None) and (endNode is not None):
        if distance(entry, startNode) != 0 and distance(entry, endNode) != 0:
            obstacle_rect = entry
            obstacle_rect._obstacle = True
            obstacle_rect.draw((252, 246, 245), 0)


for m in range(columns):
    for n in range(rows):
        gridNodes[n][m].findChildren(gridNodes)


def restart():

    pygame.quit()
    root.deiconify()
    root.destroy()
    root.quit()
    os.system('python "C:\\Users\\PC\\PycharmProjects\\A_star_search\\venv\\project.py"') # If you want the restart to work for you, instead of this path, insert the path to where you've placed this project
    sys.exit()


def exit():

    root.deiconify()
    root.destroy()
    root.quit()
    pygame.quit()
    sys.exit()


def aStar(grid, start, goal):

    closed = []
    opened = []
    opened.append(start)
    while len(opened) > 0:
        lowestIndex = 0
        for i in range(len(opened)):
            if opened[i].f < opened[lowestIndex].f:
                lowestIndex = i

        current = opened.pop(lowestIndex)
        closed.append(current)

        if distance(current, goal) == 0:
            for i in range(round(current.f)):
                current.closed = False
                current.draw((91, 200, 172), 0)
                current = current.predecessor
            goal.draw((244, 47, 8), 0)
            global found
            found = True
            break

        children = current.children
        for i in range(len(children)):
            child = children[i]
            if child._obstacle is False:
                if child not in closed:
                    tempGCost = current.g + 1
                    if child in opened:
                        if child.g > tempGCost:
                            child.g = tempGCost
                    else:
                        child.g = tempGCost
                        opened.append(child)

                child.h = distance(child, goal)
                child.f = child.g + child.h

                if child.predecessor == None:
                    child.predecessor = current
            else :
                pass

        for i in range(len(opened)):
            opened[i].draw((218, 41, 28), 1)

        for i in range(len(closed)):
            if closed[i] != start:
                closed[i].draw((42, 43, 45), 1)
        current.closed = True


if __name__ == "__main__":

    try:
        messagebox.showinfo('Instructions', '1. The first mouse click places the starting node\n2. The second click places the goal node\n'
                                            '3. All other clicks place the obstacles\n4. When you\'re done with setting obstacles, press SPACE key to start the search')
        setup()
        draw_grid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif pygame.mouse.get_pressed()[0]:
                    mousePos = pygame.mouse.get_pos()
                    mousePressed(mousePos)
                elif event.type == pygame.KEYDOWN:
                   if (event.key == pygame.K_SPACE) and (startNode is not None and endNode is not None):
                       aStar(gridNodes, startNode, endNode)
                       result = messagebox.askyesno('Question', f'The visualizer has finished the search. Found: {found}\nDo you wish to start again?')
                       if result == True:
                           restart()
                       else:
                           exit()
                pygame.display.update()
    except Exception:
        exit()