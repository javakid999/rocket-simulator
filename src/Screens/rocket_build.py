import pygame, math
from box import Box
from grid import Grid

class BuildScreen:
    def __init__(self):
        self.ui = []
        self.buttons = [pygame.Rect(20, 205, 40, 40), pygame.Rect(80, 205, 40, 40), pygame.Rect(20, 265, 40, 40), pygame.Rect(80, 265, 40, 40)]

        self.grid = Grid()
        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, input_manager, world, game):
        self.surface.fill((0,0,0))

        if (input_manager.click_pos[0] != 0 and input_manager.click_pos[1] != 0):
            self.offset = (input_manager.mouse_pos[0] - input_manager.click_pos[0] + input_manager.global_mouse_offset[0], input_manager.mouse_pos[1] - input_manager.click_pos[1] + input_manager.global_mouse_offset[1])
        else:
            self.offset = (input_manager.global_mouse_offset[0],input_manager.global_mouse_offset[1])

        self.grid.render(self.surface, self.offset, input_manager.mouse_pos)

        for i in range(4):
            for j in range(2):
                pygame.draw.rect(self.surface, (200,200,200), (j*60+15, i*60+200, 50, 50))

        pygame.draw.rect(self.surface, (255,0,0), self.buttons[0])
        pygame.draw.rect(self.surface, (255,255,0), self.buttons[1])
        pygame.draw.rect(self.surface, (0,255,0), self.buttons[2])
        pygame.draw.rect(self.surface, (0,255,255), self.buttons[3])

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        if self.buttons[0].collidepoint(pos):
            self.grid.selected_type = 0
        if self.buttons[1].collidepoint(pos):
            self.grid.selected_type = 1
        if self.buttons[2].collidepoint(pos):
            self.grid.selected_type = 2
        if self.buttons[3].collidepoint(pos):
            self.grid.selected_type = 3

        for item in self.ui:
            if item.update(-1, pos):
                pass