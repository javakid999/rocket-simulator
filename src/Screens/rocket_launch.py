import os
import pygame, math
from box import Box
from part import Engine
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class RocketLaunchScreen:
    def __init__(self):
        pygame.font.init()
        self.ui = []
        self.text = [
            [['Good luck,', (255,255,255)], ['Agent Arnav.', (255,0,255)], ['We are counting on you to establish these', (255,255,255)], ['cheese mines', (255,255,0)], ['and restore our great nation.', (255,255,255)]],
            [['You can do this', (255,255,255)], ['Agent Arnav!', (255,0,255)], ['All security checks on the', (255,255,255)], ['Galactose I', (0,255,255)], ['have passed!', (255,255,255)]],
            [['Your rocket has taken off! Congratulations!', (255,255,255)]],
            [['We are all very proud of you,', (255,255,255)], ['Agent Arnav.', (255,0,255)], ['We wish you good luck on reaching the moon', (255,255,255)]],
            [['We are now launching our own', (255,255,255)], ['Soymilk Mk. IV', (100,255,0)], ['Hurry up', (255,255,255)], [':)', (255,0,0)]],
            [['Oh no! The Soviets are launching a rocket too! Don\'t waste any time!', (255,255,255)]],
            [['Looks like you\'ve got competition. Stay safe out there soldier.', (255,255,255)]],
            [['Rats! Our rocket combusted in orbit...', (255,255,255)]],
            [['Excelsior! Thanks to you,', (255,255,255)], ['Agent Arnav,', (255,0,255)], ['America can rest easy. The', (255,255,255)], ['cheese mines', (255,255,0)], ['will be installed. Now to get you home...', (255,255,255)]]
        ]

        self.surface = pygame.Surface((1280,720))
        self.font = pygame.font.Font('./src/Assets/Font/roboto.ttf', 20)
        self.quicksave_menu = False
        self.dialogue_state = 0
        self.dialogue_time = -1

        self.timeActive = 0

    def advance_dialogue(self, assets, world, sound_manager, game):
        if self.dialogue_state == 0 and self.timeActive == 200:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive
        
        if self.dialogue_state == 1 and self.timeActive-self.dialogue_time >= 720:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 2 and world.rockets[world.selected_rocket].get_altitude(world.planets[0]) >= 2000:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 3 and world.rockets[world.selected_rocket].get_altitude(world.planets[0]) >= 10000:
            sound_manager.playMusic('everything', 6000)
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 4 and world.rockets[world.selected_rocket].get_altitude(world.planets[0]) >= 25000:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 5 and self.timeActive-self.dialogue_time >= 720:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 6 and self.timeActive-self.dialogue_time >= 720:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 7 and world.rockets[world.selected_rocket].get_altitude(world.planets[1]) <= 3000:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive
        
        if self.dialogue_state == 8 and world.rockets[world.selected_rocket].get_altitude(world.planets[1]) <= 300:
            self.dialogue_state += 1
            self.dialogue_time = self.timeActive

        if self.dialogue_state == 9 and self.timeActive-self.dialogue_time >= 720:
            game.renderer.screens['intro'].menuState.to('4')
            game.soundManager.playMusic('cipher', 3000)
            game.mode = 4

        if self.dialogue_state == 1 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['president_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[0], self.timeActive-self.dialogue_time), (250,600))
        
        if self.dialogue_state == 2 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['engineer_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[1], self.timeActive-self.dialogue_time), (250,600))

        if self.dialogue_state == 3 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['engineer_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[2], self.timeActive-self.dialogue_time), (250,600))
        
        if self.dialogue_state == 4 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['president_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[3], self.timeActive-self.dialogue_time), (250,600))
        
        if self.dialogue_state == 5 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['soviet_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[4], self.timeActive-self.dialogue_time), (250,600))

        if self.dialogue_state == 6 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['engineer_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[5], self.timeActive-self.dialogue_time), (250,600))

        if self.dialogue_state == 7 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['president_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[6], self.timeActive-self.dialogue_time), (250,600))
        
        if self.dialogue_state == 8 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['soviet_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[7], self.timeActive-self.dialogue_time), (250,600))
        
        if self.dialogue_state == 9 and self.timeActive-self.dialogue_time < 600:
            pygame.draw.rect(self.surface, (0,0,0), (140,600,1000,110))
            self.surface.blit(assets['president_dialogue'], (145,605))
            self.surface.blit(self.render_scroll(self.text[8], self.timeActive-self.dialogue_time), (250,600))

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
            if lineSize + word.get_width() > 890 and 890 != -1:
                lineSize = word.get_width()
                height += 20
            else:
                lineSize += word.get_width()
        if 890 == -1:
            width = lineSize
        else:
            width = 890
        surface = pygame.Surface((width, height))
        surface.fill((0,0,0))

        n = scroll
        row = 0
        lineSize = 0
        for i in range(len(words)):
            if n > len(words[i]):
                n -= len(words[i])
                word = self.font.render(words[i] + ' ', True, colors[i])
                if lineSize + word.get_width() <= 890 or 890 == -1:
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                else:
                    lineSize = 0
                    row += 1
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
            else:
                word = self.font.render(words[i][0:n] + ' ', True, colors[i])
                if lineSize + word.get_width() <= 890 or 890 == -1:
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                else:
                    lineSize = 0
                    row += 1
                    surface.blit(word, (lineSize, row * 20))
                    lineSize += word.get_width()
                break
        return surface

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        world.render(self.surface, self.timeActive)

        if world.rockets[world.selected_rocket].grid.engine_active():
            game.soundManager.play_sound('engine', 0)

        if self.quicksave_menu:
            self.surface.blit(self.font.render('Load Quicksave:', True, (255,255,255)), (400, 100))
            saves = os.listdir('./src/Saves/save_states')
            for i in range(len(saves)):
                save = saves[i]
                pygame.draw.rect(self.surface, (0,0,0), (500,i*60+160,200,50))
                self.surface.blit(self.font.render(save[0:save.rindex('.')], True, (255,255,255)), (520, 180+i*60))
        else:
            forces = []
            for rocket in world.rockets:
                forces.append([])

            if world.time_step == 1/60:
                rocket = world.rockets[world.selected_rocket]
                for part in rocket.grid.get_active_parts():
                    if isinstance(part, Engine):
                        part.firing = False
                if inputManager.keys[pygame.K_w]:
                    if rocket.get_fuel() > 0:
                        for part in rocket.grid.get_active_parts():
                            if isinstance(part, Engine):
                                if part.activated:
                                    part.firing = True
                                    forces[world.selected_rocket].append([(0,0),(part.force*math.sin(rocket.angle*math.pi/180+part.rotation*math.pi/2),-part.force*math.cos(rocket.angle*math.pi/180+part.rotation*math.pi/2))])
                        rocket.grid.update_fuel()
                if inputManager.keys[pygame.K_a]:
                    forces[world.selected_rocket].append([(0,1000),(-1000,0)])
                    forces[world.selected_rocket].append([(0,-1000),(1000,0)])
                if inputManager.keys[pygame.K_d]:
                    forces[world.selected_rocket].append([(0,1000),(1000,0)])
                    forces[world.selected_rocket].append([(0,-1000),(-1000,0)])
            
            world.update(forces)

            if inputManager.key_press['m']:
                game.mode = 2
            if inputManager.key_press[' ']:
                position = world.rockets[world.selected_rocket].position
                linear_velocity = world.rockets[world.selected_rocket].linear_velocity
                angle = world.rockets[world.selected_rocket].angle
                angular_velocity = world.rockets[world.selected_rocket].angular_velocity

                grids = world.rockets[world.selected_rocket].grid.stage()
                if grids != None and len(grids) > 1:
                    world.rockets.remove(world.rockets[world.selected_rocket])
                    for grid in grids:
                        box = Box(grid, [position[0]+grid.position[0]*15-15,position[1]+grid.position[1]*15-15], [grid.size[0]*15, grid.size[1]*15], 1, 0, 0)
                        box.linear_velocity = [*linear_velocity]
                        box.angle = angle
                        box.angular_velocity = angular_velocity
                        world.rockets.append(box)
            if inputManager.key_press['x']:
                world.save_state()
            if inputManager.key_press['<']:
                world.rockets[world.selected_rocket].grid.stop_firing()
                if world.selected_rocket == 0:
                    world.selected_rocket = len(world.rockets)-1
                else:
                    world.selected_rocket -= 1
            if inputManager.key_press['>']:
                world.rockets[world.selected_rocket].grid.stop_firing()
                if world.selected_rocket == len(world.rockets)-1:
                    world.selected_rocket = 0
                else:
                    world.selected_rocket += 1
            if not world.rockets[world.selected_rocket].in_planet_atmosphere(world.planets[0]):
                if inputManager.key_press['+']:
                    world.time_step_increase()
                if inputManager.key_press['-']:
                    world.time_step_decrease()
            else:
                world.time_step = 1/60

            for item in self.ui:
                pass

            self.advance_dialogue(assets, world, game.soundManager, game)

        tw = world.rockets[world.selected_rocket].get_thrust() / world.rockets[world.selected_rocket].get_gravitational_force(world.planets)
        self.surface.blit(self.font.render('Earth Altitude: ' + str(math.floor(world.rockets[world.selected_rocket].get_altitude(world.planets[0]))) + 'm      ' + 'Thrust/Weight: ' + str(round(tw, 2)) + '      Speed: ' + str(round(world.time_step*60, 2)) + '      Fuel: ' + str(max(round(world.rockets[world.selected_rocket].get_fuel()*100, 2),0)) + '%', False, (255,255,255)), (0,0))

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