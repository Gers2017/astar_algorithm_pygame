from typing import Tuple
import pygame as pg
from astar import Graph

ColorTuple = Tuple[int, int, int]


RED = (217, 25, 25)
GREEN = (25, 217, 25)
BLUE = (90, 25, 217)
BLACK = (0, 0, 0)


class Slot:
    rect: pg.Rect

    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 255, 255)) -> None:
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

    def set_color(self, color):
        self.color = color


class Grid:
    width: int
    height: int
    cell_size: int

    def __init__(self, width, height, cell_count) -> None:
        self.width, self.height, self.cell_count = width, height, cell_count
        cell_size = width // cell_count
        self.cell_size = cell_size

        # make grid of slots
        self.slots = [
            [Slot(x, y, cell_size, cell_size, RED) for x in range(0, width, cell_size)] for y in range(0, height, cell_size)
        ]

        # make grid of nodes (graph)
        self.graph = Graph(width, height, cell_count)

    def world_to_grid_cords(self, wx, wy) -> Tuple[int, int]:
        gx, gy = (wx//self.cell_size, wy//self.cell_size)
        return gx, gy

    def toggle_block(self, gx: int, gy: int):
        node, slot = self.graph.grid[gy][gx], self.slots[gy][gx]
        node.set_is_block(not node.is_block)
        slot.set_color(BLACK if node.is_block else RED)


# functions

def draw_rect(r: pg.Rect, color: pg.Color | ColorTuple, surface: pg.Surface):
    pg.draw.rect(surface, color, r)


def move_rect(r: pg.Rect, new_pos: Tuple[int, int]):
    r.left, r.top = new_pos
