import pygame

class InputManager:
    def __init__(self):
        self.mouse_state = (False,False,False)
        self.mouse_pos = [0,0]
        self.scale = [1,1]
        self.click_pos = [0,0]
        self.global_mouse_offset = [0,0]
        self.keys = []
        self.keys = pygame.key.get_pressed()
        self.key_press = {
            'x': False,
            'z': False,
            'm': False,
            '+': False,
            '-': False,
            'r': False,
            'c': False,
            ' ': False,
            '<': False,
            '>': False
        }

    def loadInput(self):
        pass

    def update_mouse(self, game):
        pos = pygame.mouse.get_pos()
        self.mouse_pos = [pos[0] / self.scale[0], pos[1] / self.scale[1]]
        if pygame.mouse.get_pressed()[0] == False and self.mouse_state[0]:
            self.global_mouse_offset[0] += (self.mouse_pos[0] - self.click_pos[0]) / self.scale[0]
            self.global_mouse_offset[1] += (self.mouse_pos[1] - self.click_pos[1]) / self.scale[1]
        if self.mouse_state[0] == False and pygame.mouse.get_pressed()[0] == True:
            self.click_event(game)
            self.click_pos[0] = self.mouse_pos[0] / self.scale[0]
            self.click_pos[1] = self.mouse_pos[1] / self.scale[1]
        if pygame.mouse.get_pressed()[0] == False:
            self.click_pos = [0,0]
        self.mouse_state = pygame.mouse.get_pressed()

    def update_keys(self):
        keys_prev = {
            'z': self.keys[pygame.K_z], 'm': self.keys[pygame.K_m],
            '+': self.keys[pygame.K_EQUALS], '-': self.keys[pygame.K_MINUS],
            'r': self.keys[pygame.K_r], 'x': self.keys[pygame.K_x], 'c': self.keys[pygame.K_c], 
            ' ': self.keys[pygame.K_SPACE], '<': self.keys[pygame.K_LEFT], '>': self.keys[pygame.K_RIGHT]
        }
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_x] and not keys_prev['x']:
            self.key_press['x'] = True
        else:
            self.key_press['x'] = False

        if self.keys[pygame.K_z] and not keys_prev['z']:
            self.key_press['z'] = True
        else:
            self.key_press['z'] = False

        if self.keys[pygame.K_c] and not keys_prev['c']:
            self.key_press['c'] = True
        else:
            self.key_press['c'] = False

        if self.keys[pygame.K_m] and not keys_prev['m']:
            self.key_press['m'] = True
        else:
            self.key_press['m'] = False

        if self.keys[pygame.K_EQUALS] and not keys_prev['+']:
            self.key_press['+'] = True
        else:
            self.key_press['+'] = False

        if self.keys[pygame.K_MINUS] and not keys_prev['-']:
            self.key_press['-'] = True
        else:
            self.key_press['-'] = False

        if self.keys[pygame.K_r] and not keys_prev['r']:
            self.key_press['r'] = True
        else:
            self.key_press['r'] = False

        if self.keys[pygame.K_SPACE] and not keys_prev[' ']:
            self.key_press[' '] = True
        else:
            self.key_press[' '] = False   

        if self.keys[pygame.K_LEFT] and not keys_prev['<']:
            self.key_press['<'] = True
        else:
            self.key_press['<'] = False

        if self.keys[pygame.K_RIGHT] and not keys_prev['>']:
            self.key_press['>'] = True
        else:
            self.key_press['>'] = False   

    def click_event(self, game):
        game.soundManager.play_sound('click', 0)
        if game.mode == 0:
            game.renderer.screens['mainmenu'].update_ui(self.mouse_pos, game)
        elif game.mode == 1:
            game.renderer.screens['launch'].update_ui(self.mouse_pos, game)
        elif game.mode == 2:
            game.renderer.screens['map'].update_ui(self.mouse_pos, game)
        elif game.mode == 3:
            game.renderer.screens['build'].update_ui(self.mouse_pos, game)
        elif game.mode == 4:
            game.renderer.screens['intro'].update_ui(self.mouse_pos, game)