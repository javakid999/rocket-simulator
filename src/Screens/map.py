import os
import pygame, math
from box import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class MapScreen:
    def __init__(self):
        self.ui = []

        self.surface = pygame.Surface((1280,720))
        self.offset = [0,0]
        self.font = pygame.font.Font('./src/Assets/Font/roboto.ttf', 20)
        self.quicksave_menu = False

        self.timeActive = 0

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        world.render_map(self.surface, self.offset, self.font)

        if self.quicksave_menu:
            self.surface.blit(self.font.render('Load Quicksave:', True, (255,255,255)), (400, 100))
            saves = os.listdir('./src/Saves/save_states')
            for i in range(len(saves)):
                save = saves[i]
                pygame.draw.rect(self.surface, (0,0,0), (500,i*60+160,200,50))
                self.surface.blit(self.font.render(save[0:save.rindex('.')], True, (255,255,255)), (520, 180+i*60))
        else:
            if (inputManager.click_pos[0] != 0 and inputManager.click_pos[1] != 0):
                self.offset = (inputManager.mouse_pos[0] - inputManager.click_pos[0] + inputManager.global_mouse_offset[0], inputManager.mouse_pos[1] - inputManager.click_pos[1] + inputManager.global_mouse_offset[1])
            else:
                self.offset = (inputManager.global_mouse_offset[0],inputManager.global_mouse_offset[1])


            if inputManager.keys[pygame.K_q]:
                world.zoom -= 0.1
            if inputManager.keys[pygame.K_e]:
                world.zoom += 0.1
            if inputManager.key_press['m']:
                game.mode = 1
            if inputManager.key_press['x']:
                world.save_state()
            if not world.in_planet_atmosphere(world.planets[0]):
                if inputManager.key_press['+']:
                    world.time_step_increase()
                if inputManager.key_press['-']:
                    world.time_step_decrease()
            else:
                world.time_step = 1/60

            world.update([])

            for item in self.ui:
                pass

        tw = world.get_thrust() / world.get_gravitational_force()
        self.surface.blit(self.font.render('Altitude: ' + str(math.floor(world.rockets[world.selected_rocket].get_altitude(world.planets[0]))) + 'm      ' + 'Thrust/Weight: ' + str(round(tw, 2)) + '      Time Step: ' + str(round(world.time_step, 2)), False, (255,255,255)), (0,0))

        if inputManager.key_press['c']:
            self.quicksave_menu = not self.quicksave_menu

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        if self.quicksave_menu == True:
                saves = os.listdir('./src/Saves/save_states')
                for i in range(len(saves)):
                    if pygame.Rect(500,i*60+160,200,50).collidepoint(*pos):
                        game.world.load_state(saves[i][0:saves[i].rindex('.')])
                        self.quicksave_menu = False
                        
        for item in self.ui:
            if item.update(-1, pos):
                pass