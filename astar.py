from math import sqrt
from queue import PriorityQueue
from typing import List, Set
from game_structs import NEIGHBOR, Node, Graph


# Manhattan distance on a square grid
def get_man_distance(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_distance(a: Node, b: Node) -> int:
    A = abs(a.x - b.x)
    B = abs(a.y - b.y)
    C = sqrt(pow(A, 2) + pow(B, 2))
    return int(C * 10)


def a_star(graph: Graph) -> List[Node]:
    closed_nodes: List[Node] = []
    visited_nodes: Set[Node] = set()

    start_node, goal_node = graph.start, graph.goal
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
            if neighbor in closed_nodes or neighbor.is_block:
                continue

            # draw stuff
            if neighbor != graph.goal:
                neighbor.set_state(NEIGHBOR)
                graph.update_node(neighbor)

            # possible use of node weights
            new_cost = current.G + get_distance(current, neighbor)
            unvisited = neighbor not in visited_nodes

            if new_cost < neighbor.G or unvisited:
                neighbor.set_G(new_cost)
                neighbor.set_parent(current)
                pq.put((neighbor.F(), neighbor))
                # print(f"{current} -> {neighbor} G cost={neighbor.G}")

                if unvisited:
                    neighbor.set_H(get_distance(neighbor, goal_node))
                    visited_nodes.add(neighbor)
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
