import math
import pygame
from button import Button
from particle import Particle, ParticleSystem
from statemachine import StateMachine

class MainMenuScreen:
    def __init__(self, assets):
        self.menuState = StateMachine()
        self.menuState.addState('title', ['startgame', 'options'], True)
        self.menuState.addState('startgame', ['title'])
        self.menuState.addState('options', ['title'])

        self.ui = [
            Button('start', (490, 300), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_start']}),
            Button('options', (490, 410), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_options']}),
            Button('credits', (490, 520), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_credits']}),
        ]

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

        title_surface = pygame.transform.rotate(pygame.transform.scale_by(assets['title'], 1), 20*math.sin(self.timeActive/10))
        self.surface.blit(title_surface, (320, 150-title_surface.get_height()/2))

        for item in self.ui:
            item.render(self.surface, pos)

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(pos):
                if item.id == 'start':
                    game.mode = 1
                    game.soundManager.playMusic('free_bird', 2000)
                if item.id == 'options':
                    pass
                if item.id == 'credits':
                    pass