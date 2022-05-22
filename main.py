import pygame as pg
from pygame.locals import *
from game_structs import Grid, move_rect, draw_rect


width, height = 512, 512
size = (width, height)
cell_count = 8
cell_size = width // cell_count

running = True
screen = pg.display.set_mode(size)
pg.display.set_caption("pygame baby")
clock = pg.time.Clock()

GRID = Grid(width, height, cell_count)


def draw_grid_lines(width: int, height: int, cell_size: int, color=(50, 50, 250)):
    for y in range(0, height, cell_size):
        pg.draw.line(screen, color, (0, y), (width, y), 2)
    for x in range(0, width, cell_size):
        pg.draw.line(screen, color, (x, 0), (x, height), 2)


def draw_grid():
    for rows in GRID.slots:
        for c in rows:
            draw_rect(c.rect, c.color, screen)


def draw():
    screen.fill((12, 0, 12))
    draw_grid()
    draw_grid_lines(width, height, cell_size)
    pg.display.update()


def get_mouse_pos_on_grid(_global_pos):
    x, y = _global_pos
    mx, my = x//cell_size, y//cell_size
    return mx, my


while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:

            w_mouse_pos = pg.mouse.get_pos()
            gx, gy = get_mouse_pos_on_grid(w_mouse_pos)
            print(f"mouse world: {w_mouse_pos}, mouse grid: {gx, gy}")
            GRID.toggle_block(gx, gy)
            # move_rect(my_cell.rect, mpos)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                GRID.graph.print_graph()

        draw()


pg.quit()

# rat_img = pg.image.load("rat.png")
# rat_img = pg.transform.scale(rat_img, (cell_size, cell_size))
# screen.blit(rat_img, pos)
