import json
import pygame

from GameManagers.assetmanager import AssetManager
from GameManagers.audiomanager import AudioManager
from GameManagers.inputmanager import InputManager
from grid import Grid
from renderer import Renderer
from world import World

class Game:
    def __init__(self):
        self.time = 0
        self.frame = 0
        self.timeOnScreen = 0
        self.clock = pygame.time.Clock()
        self.mode = 3
        self.settings = {}
        self.renderer = Renderer()
        self.inputManager = InputManager()
        self.assetManager = AssetManager()
        self.soundManager = AudioManager()
        
    def start(self):
        pygame.init()
        self.settings = json.load(open('./src/Saves/settings.json'))
        self.inputManager.loadInput()
        self.assetManager.loadAssets()
        self.soundManager.loadSounds(self.settings)
        self.renderer.initScreens(self)
        
        self.init_world()

        self.soundManager.playMusic('cipher', 3000)

        self.update()
    
    def init_world(self):
        self.world = World(self.assetManager.assets)
        planet_texture = self.assetManager.generateTiledTexture('dirt', (1312,752))
        water_texture = self.assetManager.generateTiledTexture('water', (1312,752))
        moon_texture = self.assetManager.generateTiledTexture('moon', (1312,752))
        moon_water_texture = self.assetManager.generateTiledTexture('cheese_water', (1312,752))
        self.world.add_planet([700,637300], 637000, {'land': planet_texture, 'water': water_texture, 'frog': self.assetManager.assets['frog'], 'leaf': [self.assetManager.assets['leaf1'], self.assetManager.assets['leaf2']], 'rock': [self.assetManager.assets['rock1'], self.assetManager.assets['rock2'], self.assetManager.assets['rock3'], self.assetManager.assets['rock4']]}, 5.97*10**21, 30, 0.08, (128,128,255), True)
        self.world.planets[0].add_atmosphere(pygame.Color(128,128,255), 10000)
        self.world.planets[0].add_feature('Launchpad', 150063, [0.1]*52)
        self.world.planets[0].add_feature('Ocean of Nav', 130000, [-6]*400)
        self.world.add_planet([700,4636040], 173740, {'land': moon_texture, 'water': moon_water_texture, 'frog': -1, 'leaf': -1, 'rock': [self.assetManager.assets['rock1'], self.assetManager.assets['rock2'], self.assetManager.assets['rock3'], self.assetManager.assets['rock4']]}, 7.348*10**19, -30, 0.08, (200,200,200), False, [1000,0])
        self.world.planets[1].add_feature('Arnavian Crater', 12000, [-6]*40)

        self.world.generate_world()
        
    def save_game(self, file):
        pass

    def load_saved_game(self):
        pass
       
    def update(self):
        while True:
            self.inputManager.update_mouse(self)
            self.inputManager.update_keys()
            self.renderer.render(self)
            for event in pygame.event.get():     
                if event.type == pygame.QUIT:
                    return    
            self.frame += 1
            self.timeOnScreen += 1
            self.clock.tick(60)
            print(self.clock.get_fps())