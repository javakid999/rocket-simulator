import pygame

from Screens.main_menu import MainMenuScreen
from Screens.rocket_launch import RocketLaunchScreen

class Renderer:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.window = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('I Aimed for the Moon & Hit Cheese')
        self.screen.fill((0,0,0))
        self.global_ui = []
        self.screens = {}

    def render(self, game):
        self.screen.fill((0,0,0))
        self.renderUI(game.inputManager, game.mode)
 
        if game.mode == 0:
            self.screens['mainmenu'].render(self.screen, game.assetManager.assets, game.inputManager.mouse_pos, game.inputManager.global_mouse_offset)
        if game.mode == 1:
            self.screens['launch'].render(self.screen, game.assetManager.assets, game.inputManager.mouse_pos, game.inputManager.global_mouse_offset, game.inputManager.keys)
 
        self.window.blit(pygame.transform.scale(self.screen, (self.window.get_width(), self.window.get_height())), (0,0))
        pygame.display.flip()

    def renderUI(self, inputManager, gamemode):
        for item in self.global_ui:
            item.render(self.screen, gamemode, inputManager.mousePos, inputManager.globalMouseOffset)

    def initUI(self, game):
        pass

    def initScreens(self, game):
        pygame.display.set_icon(game.assetManager.assets['cheese'])
        self.screens['mainmenu'] = MainMenuScreen(game.assetManager.assets)
        self.screens['launch'] = RocketLaunchScreen()