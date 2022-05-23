from typing import Tuple
import pygame as pg
from astar import Graph, Node, a_star

ColorTuple = Tuple[int, int, int]


RED = (217, 25, 25)
GREEN = (25, 217, 25)
BLUE = (90, 25, 217)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (190, 20, 237)


class Slot:
    rect: pg.Rect
    color: ColorTuple

    def __init__(self, x: int, y: int, width: int, height: int, color=WHITE) -> None:
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

    def set_color(self, color):
        self.color = color

    def clear(self):
        self.set_color(WHITE)


class Grid:
    width: int
    height: int
    cell_size: int
    rows_count: int
    cols_count: int

    def __init__(self, width, height, cell_size) -> None:
        self.width, self.height, self.cell_count = width, height, cell_size
        self.rows_count = height // cell_size
        self.cols_count = width // cell_size
        self.cell_size = cell_size
        # make grid of slots
        self.slots = [[Slot(x, y, cell_size, cell_size) for x in range(
            0, width, cell_size)] for y in range(0, height, cell_size)]
        # make grid of nodes (graph)
        self.graph = Graph(width, height, cell_size)
        self.start = None
        self.goal = None

    def get_slot(self, x, y) -> Slot:
        return self.slots[y][x]

    def wcords_2_gcords(self, wx: int, wy: int) -> Tuple[int, int]:
        return (wx//self.cell_size, wy//self.cell_size)

    def toggle_block(self, gx: int, gy: int):
        node, slot = self.graph.get_node(gx, gy), self.get_slot(gx, gy)
        node.set_is_block(not node.is_block)
        slot.set_color(BLACK if node.is_block else WHITE)

    def set_block(self, gx: int, gy: int):
        self.graph.get_node(gx, gy).set_is_block(True)
        self.get_slot(gx, gy).set_color(BLACK)

    def set_not_block(self, gx: int, gy: int):
        self.graph.get_node(gx, gy).set_is_block(False)
        self.get_slot(gx, gy).set_color(WHITE)

    def node_to_slot(self, node: Node) -> "Slot":
        gx, gy = self.wcords_2_gcords(node.x, node.y)
        return self.get_slot(gx, gy)

    def set_start(self, gx: int, gy: int):
        node = self.graph.get_node(gx, gy)
        if node.is_block or node == self.goal:
            return

        if self.start != None:
            self.node_to_slot(self.start).clear()

        self.start = node
        self.node_to_slot(node).set_color(GREEN)

    def set_goal(self, gx: int, gy: int):
        node = self.graph.get_node(gx, gy)
        if node.is_block or node == self.start:
            return

        if self.goal != None:
            self.node_to_slot(self.goal).clear()

        self.goal = node
        self.node_to_slot(node).set_color(RED)

    def clear(self):
        for row in self.graph.grid:
            for node in row:
                if node.is_block or node == self.start or node == self.goal:
                    continue
                self.node_to_slot(node).clear()

    def calculate_path(self):
        path = a_star(self.start, self.goal, self.graph)

        for n in path[1:-1]:
            self.node_to_slot(n).set_color(PURPLE)

        return len(path) > 0


# functions

def draw_rect(r: pg.Rect, color: pg.Color | ColorTuple, surface: pg.Surface):
    pg.draw.rect(surface, color, r)


def move_rect(r: pg.Rect, new_pos: Tuple[int, int]):
    r.left, r.top = new_pos
