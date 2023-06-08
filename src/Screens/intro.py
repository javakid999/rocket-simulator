import math
import pygame
from button import Button
from particle import Particle, ParticleSystem
from statemachine import StateMachine

class IntroScreen:
    def __init__(self, assets):
        self.menuState = StateMachine()
        self.menuState.addState('1', ['2'], True)
        self.menuState.addState('2', ['3'])
        self.menuState.addState('3', [])
        self.text = [[['The year is 20XX. Global cheese reserves are at an all time low ever since the last cow jumped over the moon 71 years ago.', (255,255,255)]],
                     [['To prevent the imminent collapse of these Great United States, we have tasked you,', (255,255,255)], ['Agent Arnav', (255,0,255)], ['with the mission of reestablishing the lunar cheese mines.', (255,255,255)]],
                     [['Of course, we will provide you with the necessary resources and supplies, as well as the materials for your', (255,255,255)], ['Galactose I', (0,255,255)], ['. Good luck, Agent. You are our only hope.', (255,255,255)]]]

        self.ui = [
            Button('continue', (490, 300), (300,100), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_continue']}),
        ]
        self.font = pygame.font.Font('./src/Assets/Font/roboto.ttf', 20)

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render_scroll(self, texts, scroll):
        height = 20
        words = []
        length = 0
        colors = []

        for i in range(len(texts)):
            text = texts[i][0].split(' ')
            for word in text:
                words.append(word)
                length += len(word)
                colors.append(texts[i][1])

        lineSize = 0
        for i in range(len(words)):
            word = self.font.render(words[i] + ' ', True, colors[i])
            if lineSize + word.get_width() > 1280 and 1280 != -1:
                lineSize = word.get_width()
                height += 20
            else:
                lineSize += word.get_width()
        if 1280 == -1:
            width = lineSize
        else:
            width = 1280
        surface = pygame.Surface((width, height))
        surface.fill((0,0,0))

        n = scroll
        row = 0
        lineSize = 0
        for i in range(len(words)):
            if n > len(words[i]):
                n -= len(words[i])
                word = self.font.render(words[i] + ' ', True, colors[i])
                if lineSize + word.get_width() <= 1280 or 1280 == -1:
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                else:
                    lineSize = 0
                    row += 1
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
            else:
                word = self.font.render(words[i][0:n] + ' ', True, colors[i])
                if lineSize + word.get_width() <= 1280 or 1280 == -1:
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                else:
                    lineSize = 0
                    row += 1
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                break
        return surface

    def render(self, screen, assets, pos, globalMouseOffset):
        self.surface.fill((0,0,0))
        
        if self.menuState.activeState == '1':
            self.surface.blit(self.render_scroll(self.text[0], self.timeActive), (0,640))
            self.surface.blit(assets['cutscene_1'], (0,0))
            self.surface.blit(assets['cutscene_2'], (640, 0))
        if self.menuState.activeState == '2':
            self.surface.blit(self.render_scroll(self.text[1], self.timeActive), (0,640))
            self.surface.blit(assets['cutscene_3'], (0,0))
            self.surface.blit(assets['cutscene_4'], (640, 0))
        if self.menuState.activeState == '3':
            self.surface.blit(self.render_scroll(self.text[2], self.timeActive), (0,640))
            self.surface.blit(assets['cutscene_5'], (0,0))
            self.surface.blit(assets['cutscene_6'], (640, 0))

        for item in self.ui:
            if self.timeActive > 400:
                item.render(self.surface, pos)

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(pos):
                if item.id == 'continue' and self.timeActive > 400:
                    if self.menuState.activeState == '1':
                        self.menuState.to('2')
                        self.timeActive = 0
                    elif self.menuState.activeState == '2':
                        self.menuState.to('3')
                        self.timeActive = 0
                    elif self.menuState.activeState == '3':
                        game.mode = 3
                        game.soundManager.playMusic('bored_to_bits', 2000)