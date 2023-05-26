import pygame
from particle import Particle, ParticleSystem
from statemachine import StateMachine

class MainMenuScreen:
    def __init__(self, assets):
        self.menuState = StateMachine()
        self.menuState.addState('title', ['startgame', 'options'], True)
        self.menuState.addState('startgame', ['title'])
        self.menuState.addState('options', ['title'])

        self.ui = []

        base_particle = Particle(assets['cheese'])
        base_particle.position = [640,720]
        self.particles = ParticleSystem((1280,720), base_particle, [-7,7,-25,-25], [-3,3], [0,0.5], 10)

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, pos, globalMouseOffset):
        self.surface.fill((0,0,0))
        
        self.surface.blit(assets['background'], (-pos[0]/10-64,-pos[1]/10-64))

        self.particles.render(self.surface)
        self.particles.update()

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def updateUI(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass