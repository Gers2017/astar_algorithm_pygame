from typing import Tuple
import pygame as pg
from pygame.locals import *
from astar import a_star
from game_structs import Graph, PATH

width, height = 1024, 704
size = (width, height)
cell_size = 16
SCREEN = pg.display.set_mode(size)
graph = Graph(width, height, cell_size, SCREEN)

running = True
pg.display.set_caption("pygame baby")
clock = pg.time.Clock()

graph.set_start(0, 0)
graph.set_goal(graph.cols_count - 1, graph.rows_count - 1)


def world_to_grid(wx, wy) -> Tuple[int, int]:
    return (wx // graph.cell_size, wy // graph.cell_size)


def get_mouse_grid_pos():
    x, y = pg.mouse.get_pos()
    return world_to_grid(x, y)


SCREEN.fill((0, 12, 12))
graph.draw_grid()

while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        left_ms, middle_ms, right_ms = pg.mouse.get_pressed()
        gx, gy = get_mouse_grid_pos()

        if left_ms:
            node = graph.get_node(gx, gy)
            graph.set_block(node, True)

        if right_ms:
            node = graph.get_node(gx, gy)
            graph.set_block(node, False)

        if event.type == KEYDOWN:
            if event.key == K_s:
                graph.set_start(gx, gy)

            if event.key == K_g:
                graph.set_goal(gx, gy)

            if event.key == K_SPACE:
                graph.clear_grid()
                path = a_star(graph)

                for p in path[1:-1]:
                    p.set_state(PATH)
                    graph.update_node(p)


pg.quit()

# draw_grid_lines(width, height, cell_size)
# pg.display.update()
# rat_img = pg.image.load("rat.png")
# rat_img = pg.transform.scale(rat_img, (cell_size, cell_size))
# screen.blit(rat_img, pos)
