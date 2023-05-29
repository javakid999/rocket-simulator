import os
import pygame

class AudioManager:
    def __init__(self):
        self.music = {}
        self.sounds = {}
        pygame.mixer.init()

    def loadSounds(self, settings):
        paths = os.listdir('../src/Assets/Music/')
        for path in paths:
            self.music[path[0:len(path)-4]] = '../src/Assets/Music/'+path
        pygame.mixer.music.set_volume(settings['volume'])
        
    def playMusic(self, name, fade):
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.play(-1, 0, fade)

    def stopMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()