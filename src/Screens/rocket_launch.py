import pygame
from object import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine

class RocketLaunchScreen:
    def __init__(self):
        self.ui = []

        self.rocket = Box([700,400],[40,50],1,0,0)

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, pos, globalMouseOffset, keys):
        self.surface.fill((0,0,0))
        
        self.rocket.render(self.surface)
        forces = []
        if keys[pygame.K_w]:
            forces.append([(0,0),(0,-15)])
        if keys[pygame.K_a]:
            forces.append([(0,1),(-15,0)])
        if keys[pygame.K_d]:
            forces.append([(0,1),(15,0)])
        self.rocket.update([],forces)

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def updateUI(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass