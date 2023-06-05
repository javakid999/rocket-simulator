import math
import pygame

class Grid:
    def __init__(self):
        self.size = (10,25)
        self.parts = []
        self.selected_type = 0
    
    def render(self, screen, pos, mouse_pos):
        surface = pygame.Surface((1000, 720))
        surface.fill((100,100,100))

        #draw grid
        pygame.draw.rect(surface, (150,200,225), (+pos[0], +pos[1], self.size[0]*50, self.size[1]*50))

        pygame.draw.rect(surface, (150,255,255), (math.floor((mouse_pos[0]-140)/50)*50+pos[0]%50, math.floor((mouse_pos[1])/50)*50+pos[1]%50, 50, 50))

        for i in range(11):
            pygame.draw.line(surface, (255,255,255), (i*50+pos[0], 0+pos[1]), (i*50+pos[0], self.size[1]*50+pos[1]))
        for i in range(26):
            pygame.draw.line(surface, (255,255,255), (0+pos[0], i*50+pos[1]), (self.size[0]*50+pos[0], i*50+pos[1]))

        for part in self.parts:
            part.render()

        screen.blit(surface, (140,0))