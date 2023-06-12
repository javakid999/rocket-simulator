import math
import pygame
from button import Button, Slider
from particle import Particle, ParticleSystem
from statemachine import StateMachine

class MainMenuScreen:
    def __init__(self, assets, settings):
        self.menuState = StateMachine()
        self.menuState.addState('title', ['options', 'credits'], True)
        self.menuState.addState('options', ['title'])
        self.menuState.addState('credits', ['title'])

        self.ui = [
            Button('start', (490, 300), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_start']}),
            Button('options', (490, 410), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_options']}),
            Button('credits', (490, 520), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_credits']}),
            Button('back', (490, 600), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_back']}),
            Button('fullscreen', (200, 300), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_fullscreen']}),
            Slider('volume', (500, 520), (400,20), {'ball': assets['slider_ball'], 'empty': assets['slider_empty'], 'full': assets['slider_full']}, settings['volume']),
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
            if self.menuState.activeState == 'title':
                if item.id in ['start', 'options', 'credits']:
                    item.render(self.surface, pos)
            if self.menuState.activeState == 'options':
                if item.id in ['volume', 'back', 'fullscreen']:
                    item.render(self.surface, pos)
                    self.surface.blit(pygame.transform.scale(assets['text_volume'], (300,100)), (200, 460))
            if self.menuState.activeState == 'credits':
                self.surface.blit(assets['credits'], (400,300))
                if item.id == 'back':
                    item.render(self.surface, pos)

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(pos):
                if self.menuState.activeState == 'title':
                    if item.id == 'start':
                        game.mode = 4
                        game.soundManager.playMusic('deftone', 2000)
                    if item.id == 'options':
                        self.menuState.to('options')
                    if item.id == 'credits':
                        self.menuState.to('credits')
                if self.menuState.activeState == 'options':
                    if item.id == 'back':
                        self.menuState.to('title')
                    if item.id == 'volume':
                        game.soundManager.setVolume(item.value)
                    if item.id == 'fullscreen':
                        pygame.display.toggle_fullscreen()
                if self.menuState.activeState == 'credits':
                    if item.id == 'back':
                        self.menuState.to('title')