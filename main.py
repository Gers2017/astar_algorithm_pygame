import pygame as pg
from pygame.locals import *

width, height = 512, 512
size = (width, height)
cell_size = 64
h_cells = width // cell_size
v_cells = height // cell_size


running = True
screen = pg.display.set_mode(size)
pg.display.set_caption("pygame baby")


clock = pg.time.Clock()


positions = []
for x in range(0, width, cell_size):
    for y in range(0, height, cell_size):
        positions.append((x, y))


rat_img = pg.image.load("rat.png")
rat_img = pg.transform.scale(rat_img, (cell_size, cell_size))


while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            mpos = pg.mouse.get_pos()
            upos = (mpos[0] / width,  mpos[1] / height)
            print(mpos, ", ", upos)
            pass

    screen.fill((21, 0, 12))

    for pos in positions:
        screen.blit(rat_img, pos)
    pg.display.update()


pg.quit()
