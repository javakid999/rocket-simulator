import json
import pygame

from GameManagers.assetmanager import AssetManager
from GameManagers.audiomanager import AudioManager
from GameManagers.inputmanager import InputManager
from renderer import Renderer
from world import World


class Game:
    def __init__(self):
        self.time = 0
        self.frame = 0
        self.timeOnScreen = 0
        self.world = World()
        self.clock = pygame.time.Clock()
        self.mode = 0
        self.renderer = Renderer()
        self.inputManager = InputManager()
        self.assetManager = AssetManager()
        self.soundManager = AudioManager()
        
    def start(self):
        pygame.init()
        settings = json.load(open('./src/Saves/settings.json'))
        self.inputManager.loadInput()
        self.assetManager.loadAssets()
        self.soundManager.loadSounds(settings)
        self.renderer.initScreens(self)
        
        self.soundManager.playMusic('cipher', 3000)

        self.init_world()

        self.update()
    
    def init_world(self):
        self.world = World()
        self.planet_texture = self.assetManager.generateTiledTexture('dirt', (1312,752))
        self.water_texture = self.assetManager.generateTiledTexture('water', (1312,752))
        self.world.add_planet([700,637300], 637000, [], {'land': self.planet_texture, 'water': self.water_texture}, 5.97*10**21, 0.08)
        
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