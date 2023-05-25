import pygame, math, sys
from object import Square

pygame.init()
display = pygame.display.set_mode((1280,720))

c = Square([300,20], [40,40], 2)

while True:
    pygame.display.update()
    display.fill((0,0,0))

    c.update()
    c.render(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()