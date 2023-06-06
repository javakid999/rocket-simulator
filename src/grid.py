import math
import pygame

from part import Capsule, Engine, FuelTank, Separator

class Grid:
    def __init__(self):
        self.size = (10,25)
        self.selected_type = 0
        self.parts = []
    
    def render_blueprint(self, screen, pos, mouse_pos):
        surface = pygame.Surface((1000, 720))
        surface.fill((100,100,100))

        #draw grid
        pygame.draw.rect(surface, (150,200,225), (pos[0], pos[1], self.size[0]*50, self.size[1]*50))

        cursor_pos = (math.floor((mouse_pos[0]-pos[0]-280)/50), math.floor((mouse_pos[1]-pos[1])/50))
        if 0 <= cursor_pos[0] < self.size[0] and 0 <= cursor_pos[1] < self.size[1]:
            pygame.draw.rect(surface, (150,255,255), (cursor_pos[0]*50+pos[0], cursor_pos[1]*50+pos[1], 50, 50))

        for i in range(11):
            pygame.draw.line(surface, (255,255,255), (i*50+pos[0], 0+pos[1]), (i*50+pos[0], self.size[1]*50+pos[1]))
        for i in range(26):
            pygame.draw.line(surface, (255,255,255), (0+pos[0], i*50+pos[1]), (self.size[0]*50+pos[0], i*50+pos[1]))

        for part in self.parts:
            part.render(surface, pos)

        screen.blit(surface, (280,0))

    def convert_to_launch(self):
        min_x = self.parts[0].position[0]
        min_y = self.parts[0].position[1]
        max_x = self.parts[0].position[0]
        max_y = self.parts[0].position[1]
        for i in range(1, len(self.parts)):
            if self.parts[i].position[0] > max_x:
                max_x = self.parts[i].position[0]
            if self.parts[i].position[0] < min_x:
                min_x = self.parts[i].position[0]
            if self.parts[i].position[1] > max_y:
                max_y = self.parts[i].position[1]
            if self.parts[i].position[1] < min_y:
                min_y = self.parts[i].position[1]
        for i in range(len(self.parts)):
            self.parts[i].position[0] -= min_x
            self.parts[i].position[1] -= min_y
        self.size = (max_x-min_x+1, max_y-min_y+1)

    def render_launch(self):
        surface = pygame.Surface((self.size[0]*50, self.size[1]*50), pygame.SRCALPHA)

        for part in self.parts:
            part.render(surface, [0,0])

        return pygame.transform.scale(surface, (15*self.size[0], 15*self.size[1]))
    
    def place(self, offset, pos, type, rotation):
        position = [math.floor((pos[0]-offset[0]-280)/50)*50, math.floor((pos[1]-offset[1])/50)*50]
        position = [position[0]/50,position[1]/50]
        for part in self.parts:
            if part.position[0] == position[0] and part.position[1] == position[1]:
                self.parts.remove(part)
                break
        if 0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]:
            if type == 1:
                self.parts.append(Engine(position, rotation))
            if type == 2:
                self.parts.append(FuelTank(position, rotation))
            if type == 3:
                self.parts.append(Separator(position, rotation))
            if type == 4:
                self.parts.append(Capsule(position, rotation))