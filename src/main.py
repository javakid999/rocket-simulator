import pygame, math, sys
from object import Square

pygame.init()
display = pygame.display.set_mode((1280,720))

s_1 = Square([300,200], [40,40], 2)
s_2 = Square([100,200], [30,40], 2)

while True:
    pygame.display.update()
    display.fill((0,0,0))

    s_1.update(s_2, [(0,0),(0,0)])
    s_2.update(s_1, [(0,0),(1,0)])
    s_1.render(display)
    s_2.render(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()