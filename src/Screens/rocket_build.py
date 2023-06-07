import pygame, math
from box import Box
from button import Button
from grid import Grid

class BuildScreen:
    def __init__(self, assets):
        self.ui = [Button('launch', (20, 500), (200,66), {'default': assets['button'], 'hover': assets['button_highlight'], 'text': assets['text_launch']})]
        self.buttons = [pygame.Rect(20, 205, 40, 40), pygame.Rect(80, 205, 40, 40), pygame.Rect(20, 265, 40, 40), pygame.Rect(80, 265, 40, 40), pygame.Rect(20, 325, 40, 40), pygame.Rect(80, 325, 40, 40), pygame.Rect(20, 385, 40, 40), pygame.Rect(80, 385, 40, 40), pygame.Rect(20, 445, 40, 40)]

        self.surface = pygame.Surface((1280,720))
        self.rotation = 0
        self.timeActive = 0

    def render(self, screen, assets, input_manager, world, game):
        self.surface.fill((0,0,0))

        if (input_manager.click_pos[0] != 0 and input_manager.click_pos[1] != 0):
            self.offset = (input_manager.mouse_pos[0] - input_manager.click_pos[0] + input_manager.global_mouse_offset[0], input_manager.mouse_pos[1] - input_manager.click_pos[1] + input_manager.global_mouse_offset[1])
        else:
            self.offset = (input_manager.global_mouse_offset[0],input_manager.global_mouse_offset[1])

        if input_manager.key_press['r']:
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0

        world.grid.render_blueprint(self.surface, self.offset, input_manager.mouse_pos, math.floor((self.timeActive/15)%10))

        for i in range(4):
            for j in range(2):
                color = (200,200,200)
                if world.grid.selected_type == i*2+j:
                    color = (240,240,240)
                pygame.draw.rect(self.surface, color, (j*60+15, i*60+200, 50, 50))

        self.surface.blit(pygame.transform.scale(assets['eraser'], (40,40)), self.buttons[0])
        self.surface.blit(pygame.transform.scale(assets['engine_strong'], (40,40)), self.buttons[1])
        self.surface.blit(pygame.transform.scale(assets['engine_weak'], (40,40)), self.buttons[2])
        self.surface.blit(pygame.transform.scale(assets['fuel_tank'], (40,40)), self.buttons[3])
        self.surface.blit(pygame.transform.scale(assets['separator'], (40,40)), self.buttons[4])
        self.surface.blit(pygame.transform.scale(assets['capsule'], (40,40)), self.buttons[5])
        self.surface.blit(pygame.transform.scale(assets['fuel_cap'], (40,40)), self.buttons[6])
        self.surface.blit(pygame.transform.scale(assets['cheese_machine_'+str(math.floor(self.timeActive/15)%10)], (40,40)), self.buttons[7])

        for item in self.ui:
            item.render(self.surface, input_manager.mouse_pos)

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        if self.buttons[0].collidepoint(pos):
            game.world.grid.selected_type = 0
        if self.buttons[1].collidepoint(pos):
            game.world.grid.selected_type = 1
        if self.buttons[2].collidepoint(pos):
            game.world.grid.selected_type = 2
        if self.buttons[3].collidepoint(pos):
            game.world.grid.selected_type = 3
        if self.buttons[4].collidepoint(pos):
            game.world.grid.selected_type = 4
        if self.buttons[5].collidepoint(pos):
            game.world.grid.selected_type = 5
        if self.buttons[6].collidepoint(pos):
            game.world.grid.selected_type = 6
        if self.buttons[7].collidepoint(pos):
            game.world.grid.selected_type = 7

        if pygame.Rect(280,0,1000,720).collidepoint(pos):
            game.world.grid.place(self.offset, pos, game.world.grid.selected_type, self.rotation, game.assetManager.assets)

        for item in self.ui:
            if item.update(pos):
                if item.id == 'launch':
                    game.world.grid.convert_to_launch()
                    game.mode = 1
                    game.soundManager.playMusic('free_bird', 2000)