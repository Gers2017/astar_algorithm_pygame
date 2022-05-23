from math import sqrt
from queue import PriorityQueue
from typing import List, Tuple
import pygame as pg

ColorTuple = Tuple[int, int, int]

RED = (240, 30, 116)
GREEN = (43, 240, 120)
BLUE = (30, 70, 240)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
ORANGE = (253, 200, 125)
PURPLE = (140, 25, 230)


class Node:
    def __init__(self, x: int, y: int, width: int, height: int, SCREEN: pg.Surface) -> None:
        self.x, self.y = x, y
        self.G = self.H = float("inf")
        self.parent = None
        self.is_block = False
        # pygame
        self.SCREEN = SCREEN
        self.rect = pg.Rect(x - 1, y - 1, width - 1, height - 1)
        self.color = WHITE

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
        self.tick(BLACK if is_block else WHITE)

    def tick(self, color: ColorTuple):
        self.set_color(color)
        pg.draw.rect(self.SCREEN, self.color, self.rect)
        pg.display.update()

    def set_color(self, color):
        self.color = color

    def reset(self):
        self.G = self.H = float("inf")
        self.parent = None
        self.set_color(WHITE)

    def __str__(self) -> str:
        return "{X, X}" if self.is_block else f"({self.x}, {self.y})"

    def __lt__(self, other) -> bool:
        return self.F() < other.F() or (self.F() == other.F() and self.H < other.H)


# Manhattan distance on a square grid
def get_man_distance(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_distance(a: Node, b: Node) -> int:
    A = abs(a.x - b.x)
    B = abs(a.y - b.y)
    C = sqrt(pow(A, 2) + pow(B, 2))
    return int(C * 10)


class Graph:
    def __init__(self, width: int, height: int, cell_size: int, SCREEN: pg.Surface) -> None:
        self.width, self.height, self.cell_size = width, height, cell_size
        self.cell_size = cell_size
        self.rows_count = height // cell_size
        self.cols_count = width // cell_size

        grid = [[Node(x, y, cell_size, cell_size, SCREEN) for x in range(0, width, cell_size)]
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

            if neighbor.is_block:
                continue

            neighbor_list.append(neighbor)

        return neighbor_list

    def print_graph(self):
        for rows in self.grid:
            row = [str(n) for n in rows]
            print(f"{''.join(row)}")


def a_star(start_node: Node, goal_node: Node, graph: Graph) -> List[Node]:
    closed_nodes: List[Node] = []
    visited_nodes: List[Node] = []

    start_node.G = 0
    start_node.H = 0

    pq = PriorityQueue()
    pq.put((0, start_node))

    while not pq.empty():
        current: Node = pq.get()[1]
        closed_nodes.append(current)

        if current == goal_node:
            p_node = current
            path = []
            while p_node != start_node:
                path.append(p_node)
                p_node = p_node.parent

            path.append(start_node)
            path.reverse()
            return path

        for neighbor in graph.get_neighbors(current):
            if neighbor in closed_nodes:
                continue

            neighbor.tick(ORANGE)

            # possible use of node weights
            new_cost = current.G + get_distance(current, neighbor)
            unvisited = neighbor not in visited_nodes

            if new_cost < neighbor.G or unvisited:
                neighbor.set_G(new_cost)
                neighbor.set_parent(current)
                # print(f"{current} -> {neighbor} G cost={neighbor.G}")

                if unvisited:
                    neighbor.set_H(get_distance(neighbor, goal_node))
                    pq.put((neighbor.F(), neighbor))
                    visited_nodes.append(neighbor)
    return []


def main():
    if __name__ != "__main__":
        return
    graph = Graph(8, 8, 1)
    start = graph.get_node(7, 7)
    goal = graph.get_node(0, 0)
    graph.grid[1][2].set_is_block(True)
    graph.grid[2][1].set_is_block(True)
    graph.grid[2][2].set_is_block(True)
    graph.print_graph()

    path = a_star(start, goal, graph)
    if len(path) > 0:
        for p in path:
            print(f"{p}")


main()
