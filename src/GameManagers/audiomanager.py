import os
import pygame

class AudioManager:
    def __init__(self):
        self.music = {}
        self.sounds = {}
        self.volume = 1
        pygame.mixer.init()

    def loadSounds(self, settings):
        paths = os.listdir('./src/Assets/Music/')
        for path in paths:
            self.music[path[0:len(path)-4]] = './src/Assets/Music/'+path
        pygame.mixer.music.set_volume(settings['volume'])
        paths = os.listdir('./src/Assets/Sounds/')
        for path in paths:
            self.sounds[path[0:len(path)-4]] = pygame.mixer.Sound('./src/Assets/Sounds/'+path)
        
    def play_sound(self, name, loops):
        self.sounds[name].set_volume(self.volume*0.1)
        self.sounds[name].play(loops)

    def stop_sound(self, name):
        self.sounds[name].stop()

    def playMusic(self, name, fade):
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.play(-1, 0, fade)

    def stopMusic(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def setVolume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)