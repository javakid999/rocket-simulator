import pygame, math
from box import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class RocketLaunchScreen:
    def __init__(self):
        pygame.font.init()
        self.ui = []

        self.surface = pygame.Surface((1280,720))
        self.font = pygame.font.Font('./src/Assets/Font/roboto.ttf', 12)
        self.timeActive = 0

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        world.render(self.surface, self.timeActive)

        forces = []
        if inputManager.keys[pygame.K_w]:
            forces.append([(0,0),(30*math.sin(world.rocket.angle*math.pi/180),-30*math.cos(world.rocket.angle*math.pi/180))])
        if inputManager.keys[pygame.K_a]:
            forces.append([(0,30),(-1000,0)])
            forces.append([(0,-30),(1000,0)])
        if inputManager.keys[pygame.K_d]:
            forces.append([(0,30),(1000,0)])
            forces.append([(0,-30),(-1000,0)])
        
        world.update(forces)

        if inputManager.key_press['m']:
            game.mode = 2

        for item in self.ui:
            pass

        self.surface.blit(self.font.render('Altitude: ' + str(math.floor(world.get_altitude())) + 'm', False, (255,255,255)), (0,0))

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass