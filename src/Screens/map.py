import pygame, math
from box import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class MapScreen:
    def __init__(self):
        self.ui = []

        self.surface = pygame.Surface((1280,720))
        self.offset = [0,0]
        self.font = pygame.font.Font('./src/Assets/Font/roboto.ttf', 20)

        self.timeActive = 0

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        if (inputManager.click_pos[0] != 0 and inputManager.click_pos[1] != 0):
            self.offset = (inputManager.mouse_pos[0] - inputManager.click_pos[0] + inputManager.global_mouse_offset[0], inputManager.mouse_pos[1] - inputManager.click_pos[1] + inputManager.global_mouse_offset[1])
        else:
            self.offset = (inputManager.global_mouse_offset[0],inputManager.global_mouse_offset[1])

        world.render_map(self.surface, self.offset, self.font)

        if inputManager.keys[pygame.K_q]:
            world.zoom -= 0.1
        if inputManager.keys[pygame.K_e]:
            world.zoom += 0.1
        if inputManager.key_press['m']:
            game.mode = 1

        world.update([])

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass