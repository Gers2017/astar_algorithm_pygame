import random
from typing import List, Tuple
import pygame as pg
ColorTuple = Tuple[int, int, int]

BORDER = (30, 30, 30)
BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
RED = (250, 30, 100)
GREEN = (30, 250, 90)
BLUE = (30, 30, 250)
ORANGE = (230, 180, 30)

EMPTY = 1
START = 2
GOAL = 3
BLOCK = 4
NEIGHBOR = 5
PATH = 6


class Node:
    def __init__(self, x: int, y: int, cell_size: int) -> None:
        self.x, self.y = x, y
        self.G = self.H = float("inf")
        self.parent = None
        # pygame
        self.rect = pg.Rect(x, y, cell_size, cell_size)
        self.set_state(EMPTY)

    # distance cost from start_node
    def set_G(self, g: int):
        self.G = g

    # heuristic, optimistic distance from node the end node
    def set_H(self, h: int):
        self.H = h

    def F(self):
        return self.H + self.G

    def set_parent(self, node: "Node"):
        self.parent = node

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def set_is_block(self, is_block: bool):
        self.is_block = is_block

    def draw(self, SCREEN):
        pg.draw.rect(SCREEN, self.color, self.rect)
        pg.draw.rect(SCREEN, BORDER, self.rect, 1)

    def set_color(self, color):
        self.color = color

    def reset(self):
        self.G = self.H = float("inf")
        self.parent = None
        self.set_state(EMPTY)

    def set_state(self, state: int):
        if state is EMPTY:
            self.set_color(BLACK)
            self.set_is_block(False)
        if state is BLOCK:
            self.set_color(WHITE)
            self.set_is_block(True)
        if state is NEIGHBOR:
            self.set_color(BLUE)
        if state is START:
            self.set_color(GREEN)
        if state is GOAL:
            self.set_color(RED)
        if state is PATH:
            self.set_color(ORANGE)

    def __str__(self) -> str:
        return "{X, X}" if self.is_block else f"({self.x}, {self.y})"

    def __lt__(self, other) -> bool:
        return self.F() < other.F() or (self.F() == other.F() and self.H < other.H)


class Graph:
    start: Node
    goal: Node

    def __init__(self, width: int, height: int, cell_size: int, SCREEN: pg.Surface) -> None:
        self.width, self.height, self.cell_size = width, height, cell_size
        self.cell_size = cell_size
        self.rows_count = height // cell_size
        self.cols_count = width // cell_size
        self.SCREEN = SCREEN
        self.start = self.goal = None

        grid = [[Node(x, y, cell_size) for x in range(0, width, cell_size)]
                for y in range(0, height, cell_size)]
        self.grid = grid

    def get_node(self, x: int, y: int) -> Node:
        if not self.in_cols_range(x) or not self.in_rows_range(y):
            print(
                f"Index out of range: ({x}, {y}) not in ([0..{self.width - 1}], [0..{self.height - 1}])")
        return self.grid[y][x]

    def in_cols_range(self, x: int) -> bool:
        return 0 <= x <= self.cols_count - 1

    def in_rows_range(self, y: int) -> bool:
        return 0 <= y <= self.rows_count - 1

    def get_neighbors(self, node: Node) -> List[Node]:
        x, y = node.to_tuple()
        x, y = x // self.cell_size, y // self.cell_size
        dirs: List[Tuple[int, int]] = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1),  (0, 1), (1, 1),
        ]

        neighbor_list = []

        for dir in dirs:
            dx, dy = dir
            next_x, next_y = x + dx, y + dy
            if not self.in_cols_range(next_x) or not self.in_rows_range(next_y):
                continue

            neighbor = self.grid[next_y][next_x]
            neighbor_list.append(neighbor)

        return neighbor_list

    def draw_grid(self):
        for row in self.grid:
            for node in row:
                node.draw(self.SCREEN)
        pg.display.update()

    def update_node(self, node: Node):
        node.draw(self.SCREEN)
        pg.display.update()

    def set_block(self, node: Node, b: bool):
        if node != self.start and node != self.goal:
            node.set_state(BLOCK if b else EMPTY)
            self.update_node(node)

    def set_start(self, gx, gy):
        node = self.get_node(gx, gy)
        if node.is_block or node == self.goal:
            return

        if self.start == None:
            self.start = node
            self.start.set_state(START)
        else:
            self.start, node = node, self.start
            node.set_state(EMPTY)
            self.start.set_state(START)

        self.start.draw(self.SCREEN)
        node.draw(self.SCREEN)
        pg.display.update()

    def set_goal(self, gx, gy):
        node = self.get_node(gx, gy)
        if node.is_block or node == self.start:
            return

        if self.goal == None:
            self.goal = node
            self.goal.set_state(GOAL)
        else:
            self.goal, node = node, self.goal
            node.set_state(EMPTY)
            self.goal.set_state(GOAL)

        self.goal.draw(self.SCREEN)
        node.draw(self.SCREEN)
        pg.display.update()

    def reset_grid(self):
        for row in self.grid:
            for node in row:
                if node.is_block or node == self.start or node == self.goal:
                    continue
                node.reset()
                node.draw(self.SCREEN)
        pg.display.update()

    def clear_grid(self):
        for row in self.grid:
            for node in row:
                if node == self.start or node == self.goal:
                    continue
                node.set_state(EMPTY)
                node.draw(self.SCREEN)
        pg.display.update()

    def gen_map(self):
        self.start, self.goal = None, None

        for row in self.grid:
            for node in row:
                state = BLOCK if random.random() <= 0.23 else EMPTY
                node.set_state(state)

        self.erosion()

    def erosion(self, times=4):
        for _ in range(times):
            for row in self.grid:
                for node in row:
                    neighbors = [n for n in self.get_neighbors(
                        node) if n.is_block]
                    n = len(neighbors)
                    dn = 8 - n

                    if n < 2 or n > 4:  # dies
                        node.set_state(EMPTY)
                    if n == 3 or dn == 5:  # revives
                        node.set_state(BLOCK)

                    node.draw(self.SCREEN)
                pg.display.update()

    def print_graph(self):
        for rows in self.grid:
            row = [str(n) for n in rows]
            print(f"{''.join(row)}")
