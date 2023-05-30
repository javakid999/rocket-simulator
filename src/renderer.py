import pygame

from Screens.main_menu import MainMenuScreen
from Screens.map import MapScreen
from Screens.rocket_launch import RocketLaunchScreen

class Renderer:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.window = pygame.display.set_mode((1280,720))
        pygame.display.set_caption('I Shot for the Moon & Hit Cheese')
        self.screen.fill((0,0,0))
        self.global_ui = []
        self.screens = {}
        self.screenshot_count = 0

    def render(self, game):
        self.screen.fill((0,0,0))
        self.renderUI(game.inputManager, game.mode)
 
        if game.mode == 0:
            self.screens['mainmenu'].render(self.screen, game.assetManager.assets, game.inputManager.mouse_pos, game.inputManager.global_mouse_offset)
        elif game.mode == 1:
            self.screens['launch'].render(self.screen, game.assetManager.assets, game.inputManager, game.world, game)
        elif game.mode == 2:
            self.screens['map'].render(self.screen, game.assetManager.assets, game.inputManager, game.world, game)

        self.window.blit(pygame.transform.scale(self.screen, (self.window.get_width(), self.window.get_height())), (0,0))

        if game.inputManager.key_press['z']:
            self.save_screen()
            self.screenshot_count+= 1

        pygame.display.flip()

    def save_screen(self):
        pygame.image.save(self.screen, './src/Screenshots/screenshot_'+str(self.screenshot_count)+'.png')

    def renderUI(self, inputManager, gamemode):
        for item in self.global_ui:
            item.render(self.screen, gamemode, inputManager.mousePos, inputManager.globalMouseOffset)

    def initUI(self, game):
        #this is where you would put all of the things in the global ui
        pass

    def initScreens(self, game):
        pygame.display.set_icon(game.assetManager.assets['cheese'])
        self.screens['mainmenu'] = MainMenuScreen(game.assetManager.assets)
        self.screens['launch'] = RocketLaunchScreen()
        self.screens['map'] = MapScreen()