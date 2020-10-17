import math
import os
from tkinter import *
from tkinter import messagebox

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
startNode = None
endNode = None
columns = SCREEN_WIDTH // 20
rows = SCREEN_HEIGHT // 20
block_size = 20
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

    def get_x(self):

        return self._x

    def get_y(self):

        return self._y

    def is_obstacle(self):

        return self._obstacle

    def draw(self, color, border):

        if self.closed is False:
            node = pygame.Rect(self._x * block_size, self._y * block_size, block_size, block_size)
            pygame.draw.rect(SCREEN, color, node, border)
            pygame.display.update()

    def find_children(self, node_grid):

        column = self._x
        row = self._y
        if (node_grid[row + 1][column].is_obstacle() is False) and (row < rows):
            self.children.append(node_grid[row + 1][column])
        if (node_grid[row - 1][column].is_obstacle() is False) and (row > 0):
            self.children.append(node_grid[row - 1][column])
        if (node_grid[row][column + 1].is_obstacle() is False) and (column < columns):
            self.children.append(node_grid[row][column + 1])
        if (node_grid[row][column - 1].is_obstacle() is False) and (column > 0):
            self.children.append(node_grid[row][column - 1])


root = Tk()
root.withdraw()


def setup():

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    global SCREEN
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface(SCREEN.get_size())
    surface = surface.convert()
    pygame.display.set_caption('Path finder')
    surface.fill((0, 0, 0))


def draw_grid():

    for i in range(rows):
        for j in range(columns):
            rect = Node(j * block_size, i * block_size, False)
            gridNodes.append(rect)
            rect.draw((0, 0, 0), 1)
    pygame.display.update()


for x in range(rows + 1):
    for y in range(columns + 1):
        gridNodes[x][y] = Node(y, x, False)


def distance(start, end):

    x_distance = start.get_x() - end.get_x()
    y_distance = start.get_y() - end.get_y()
    return math.sqrt(x_distance ** 2 + y_distance ** 2)


def mouse_pressed(position):

    y1 = position[0] // 20
    x1 = position[1] // 20
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
        gridNodes[n][m].find_children(gridNodes)


def restart():
    pygame.quit()
    root.deiconify()
    root.destroy()
    root.quit()
    os.system(
        'python "C:\\Users\\PC\\PycharmProjects\\A_star_search\\venv\\project.py"')  # If you want the restart to work for you, instead of this path, insert the path to where you've placed this project
    sys.exit()


def exit_the_program():
    root.deiconify()
    root.destroy()
    root.quit()
    pygame.quit()
    sys.exit()


def a_star(grid, start, goal):

    closed = []
    opened = [start]

    while len(opened) > 0:
        lowest_index = 0
        for i in range(len(opened)):
            if opened[i].f < opened[lowest_index].f:
                lowest_index = i

        current = opened.pop(lowest_index)
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
            if child.is_obstacle() is False:
                if child not in closed:
                    temp_g_cost = current.g + 1
                    if child in opened:
                        if child.g > temp_g_cost:
                            child.g = temp_g_cost
                    else:
                        child.g = temp_g_cost
                        opened.append(child)

                child.h = distance(child, goal)
                child.f = child.g + child.h

                if child.predecessor is None:
                    child.predecessor = current
            else:
                pass

        for i in range(len(opened)):
            opened[i].draw((218, 41, 28), 1)

        for i in range(len(closed)):
            if closed[i] != start:
                closed[i].draw((42, 43, 45), 1)
        current.closed = True


if __name__ == "__main__":

    try:
        messagebox.showinfo('Instructions',
                            '1. The first mouse click places the starting node\n2. The second click places the goal node\n'
                            '3. All other clicks place the obstacles\n4. When you\'re done with setting obstacles, press SPACE key to start the search')
        setup()
        draw_grid()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_the_program()
                elif pygame.mouse.get_pressed()[0]:
                    mousePos = pygame.mouse.get_pos()
                    mouse_pressed(mousePos)
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE) and (startNode is not None and endNode is not None):
                        a_star(gridNodes, startNode, endNode)
                        result = messagebox.askyesno('Question',
                                                     f'The visualizer has finished the search. Found: {found}\nDo you wish to start again?')
                        if result is True:
                            restart()
                        else:
                            exit_the_program()
                pygame.display.update()
    except Exception:
        exit_the_program()
