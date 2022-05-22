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

    def set_parent(self, node: "Node"):
        self.parent = node

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def set_is_block(self, b: bool):
        self.is_block = b

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
    def __init__(self, width: int, height: int, cell_count: int) -> None:
        self.width, self.height, self.cell_count = width, height, cell_count
        cell_size = width // cell_count
        self.cell_size = cell_size

        grid = [[Node(x, y) for x in range(0, width, cell_size)]
                for y in range(0, height, cell_size)]
        self.grid = grid

    def get_node(self, x: int, y: int) -> Node:
        if not self.in_col_range(x) or not self.in_row_range(y):
            print(
                f"Index out of range: ({x}, {y}) not in ([0..{self.width - 1}], [0..{self.height - 1}])")

        return self.grid[y][x]

    def in_col_range(self, value: int) -> bool:
        return 0 <= value <= self.width - 1

    def in_row_range(self, value: int) -> bool:
        return 0 <= value <= self.height - 1

    def get_neighbors(self, node: Node) -> List[Node]:
        x, y = node.to_tuple()
        dirs: List[Tuple[int, int]] = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1),  (0, 1), (1, 1),
        ]

        neighbor_list = []

        for dir in dirs:
            dx, dy = dir[0] * self.cell_size, dir[1] * self.cell_size
            next_x, next_y = x + dx, y + dy

            if not self.in_col_range(next_x) or not self.in_row_range(next_y):
                continue

            neighbor = self.grid[next_y][next_x]
            neighbor_list.append(neighbor)

        return neighbor_list

    def print_graph(self):
        for rows in self.grid:
            row = [str(n) for n in rows]
            print(f"{''.join(row)}")


def a_star(start_node: Node, goal_node: Node, graph: Graph) -> List[Node]:
    closed_nodes: List[Node] = []
    open_nodes: List[Node] = []

    start_node.G = 0
    start_node.H = 0

    pq = PriorityQueue()
    pq.put((0, start_node))

    while not pq.empty():
        current: Node = pq.get()[1]
        open_nodes.remove(current)
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
            if neighbor in closed_nodes or neighbor.is_block:
                continue

            # could use weights here
            new_cost = current.G + get_distance(current, neighbor)

            if new_cost < neighbor.G:
                neighbor.set_G(new_cost)
                neighbor.set_parent(current)
                # print(f"{current} -> {neighbor}")

            neighbor.set_H(get_distance(neighbor, goal_node))
            pq.put((neighbor.F(), neighbor))
            open_nodes.append(neighbor)
            # print(f"adding {neighbor.F()} {neighbor} to pq\n")

    return []


def main():
    if __name__ != "__main__":
        return
    graph = Graph(8, 8, 8)
    print(f"cells: {graph.cell_count}, size: {graph.cell_size}")
    start = graph.get_node(0, 0)
    goal = graph.get_node(6, 7)
    graph.grid[1][1].set_is_block(True)
    graph.grid[2][1].set_is_block(True)
    graph.grid[2][2].set_is_block(True)
    graph.print_graph()

    path = a_star(start, goal, graph)
    if len(path) > 0:
        for p in path:
            print(f"{p}")


main()
