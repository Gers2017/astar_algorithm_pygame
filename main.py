from typing import Tuple
import pygame as pg
from pygame.locals import *
from astar import PURPLE, GREEN, RED, Graph, Node, a_star

width, height = 1024, 704
size = (width, height)
cell_size = 16
SCREEN = pg.display.set_mode(size)
graph = Graph(width, height, cell_size, SCREEN)
running = True
pg.display.set_caption("pygame baby")
clock = pg.time.Clock()

start_node = graph.get_node(0, 0)
start_node.set_color(GREEN)
goal_node = graph.get_node(graph.cols_count - 1, graph.rows_count - 1)
goal_node.set_color(RED)


def draw_rect(color, rect):
    pg.draw.rect(SCREEN, color, rect)


def world_to_grid(wx, wy) -> Tuple[int, int]:
    return (wx // graph.cell_size, wy // graph.cell_size)


def draw_grid_lines(width: int, height: int, cell_size: int, color=(50, 50, 250)):
    for y in range(0, height, cell_size):
        pg.draw.line(SCREEN, color, (0, y), (width, y), 2)
    for x in range(0, width, cell_size):
        pg.draw.line(SCREEN, color, (x, 0), (x, height), 2)


def draw_grid():
    for rows in graph.grid:
        for node in rows:
            draw_rect(node.color, node.rect)


def clear_grid():
    for row in graph.grid:
        for node in row:
            if node.is_block or node == start_node or node == goal_node:
                continue
            node.reset()
            draw_rect(node.color, node.rect)

    pg.display.update()


def get_mouse_grid_pos():
    x, y = pg.mouse.get_pos()
    return world_to_grid(x, y)


SCREEN.fill((0, 12, 12))
draw_grid()
pg.display.update()

while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        left_ms, middle_ms, right_ms = pg.mouse.get_pressed()
        gx, gy = get_mouse_grid_pos()

        if left_ms:
            graph.get_node(gx, gy).set_is_block(True)

        if right_ms:
            graph.get_node(gx, gy).set_is_block(False)

        if event.type == KEYDOWN:
            if event.key == K_s:
                gx, gy = get_mouse_grid_pos()
                node = graph.get_node(gx, gy)
                if not node.is_block and node != goal_node:
                    start_node = node
                draw_rect(node.color, node.rect)
                pg.display.update()

            if event.key == K_g:
                gx, gy = get_mouse_grid_pos()
                node = graph.get_node(gx, gy)
                if not node.is_block and node != start_node:
                    goal_node = node
                draw_rect(RED, node.rect)
                pg.display.update()

            if event.key == K_SPACE:
                clear_grid()
                path = a_star(start_node, goal_node, graph)

                for node in path:
                    node.tick(PURPLE)

                start_node.tick(GREEN)
                goal_node.tick(RED)

pg.quit()

# draw_grid_lines(width, height, cell_size)
# pg.display.update()
# rat_img = pg.image.load("rat.png")
# rat_img = pg.transform.scale(rat_img, (cell_size, cell_size))
# screen.blit(rat_img, pos)
