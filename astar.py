from math import sqrt
from queue import PriorityQueue
from typing import List, Tuple


class Node:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.G = self.H = float("inf")
        self.parent = None
        self.is_block = False

    # distance cost from start_node
    def set_G(self, g: int):
        self.G = g

    # heuristic, optimistic distance from node the end node
    def set_H(self, h: int):
        self.H = h

    def F(self):
        return self.H + self.G

    def set_parent(self, node):
        self.parent = node

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # Manhattan distance on a square grid
# def get_distance(a: Node, b: Node) -> int:
#     return abs(a.x - b.x) + abs(a.y - b.y)


def get_distance(a: Node, b: Node) -> int:
    A = abs(a.x - b.x)
    B = abs(a.y - b.y)
    C = sqrt(pow(A, 2) + pow(B, 2))
    return int(C * 10)


class Graph:
    def __init__(self, width, height) -> None:
        grid = [[Node(x, y) for x in range(width)] for y in range(height)]
        self.grid = grid
        self.rows = width
        self.columns = height

    def get_node(self, x: int, y: int) -> Node:
        if not self.in_row_range(x) or not self.in_col_range(y):
            print(
                f"Index out of range: ({x}, {y}) not in ([0..{self.rows - 1}], [0..{self.columns - 1}])")

        return self.grid[y][x]

    def in_row_range(self, value: int) -> bool:
        return 0 <= value <= self.rows - 1

    def in_col_range(self, value: int) -> bool:
        return 0 <= value <= self.columns - 1

    def neighbors(self, node: Node) -> List[Node]:
        x, y = node.to_tuple()
        dirs = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1),  (0, 1), (1, 1),
        ]

        neighbor_list = []

        for dir in dirs:
            dx, dy = dir
            next_x, next_y = x + dx, y + dy
            if not self.in_row_range(next_x) or not self.in_col_range(next_y):
                continue
            neighbor = self.grid[next_y][next_x]
            neighbor_list.append(neighbor)

        return neighbor_list

    def print_graph(self):
        for y in range(self.columns):
            row = [str(n) for n in self.grid[y]]
            print(f"{' '.join(row)}")


graph = Graph(4, 4)
start = graph.get_node(0, 0)
goal = graph.get_node(3, 3)
graph.print_graph()


open_nodes: List[Node] = []
closed_nodes: List[Node] = []


def a_star(start_node: Node, goal_node: Node) -> List[Node]:
    start_node.G = 0
    start_node.H = 0
    open_nodes.append(start_node)

    while len(open_nodes) > 0:
        # sorted(open_nodes, key=lambda n: n.get_F())

        current = open_nodes[0]
        for t in open_nodes:
            if t.F() < current.F() or (t.F() == current.F() and t.H < current.H):
                current = t

        closed_nodes.append(current)
        open_nodes.remove(current)

        if current == goal_node:
            p_node = current
            path = []
            while p_node != start_node:
                path.append(p_node)
                p_node = p_node.parent

            path.reverse()
            return path

        for neighbor in graph.neighbors(current):
            if neighbor in closed_nodes or neighbor.is_block:
                continue

            in_search = neighbor in open_nodes

            # could use weights here
            new_cost = current.G + get_distance(current, neighbor)

            if new_cost < neighbor.G or not in_search:
                neighbor.set_G(new_cost)
                neighbor.parent = current
                print(f"set parent: {current} > {neighbor}")

            if not in_search:
                neighbor.set_H(get_distance(neighbor, goal_node))
                open_nodes.append(neighbor)

    return []


path = a_star(start, goal)
if len(path) > 0:
    for p in path:
        print(f"{p}")
