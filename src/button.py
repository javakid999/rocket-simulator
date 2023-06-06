import pygame

class Button:
    def __init__(self, id, position, size, textures):
        self.id = id
        self.rect = pygame.Rect(*position, *size)
        self.textures = textures

    def render(self, screen, mouse_pos):
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        if self.rect.collidepoint(*mouse_pos):
            surface.blit(pygame.transform.scale(self.textures['hover'], self.rect.size), (0,0))
        else:
            surface.blit(pygame.transform.scale(self.textures['default'], self.rect.size), (0,0))
        surface.blit(pygame.transform.scale(self.textures['text'], self.rect.size), (0,0))

        screen.blit(surface, self.rect.topleft)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
class Slider:
    def __init__(self, id, position, size, textures, value):
        self.id = id
        self.rect = pygame.Rect(*position, *size)
        self.textures = textures
        self.value = value

    def render(self, screen, mouse_pos):
        surface = pygame.Surface((self.rect.size[0]+15, self.rect.size[1]), pygame.SRCALPHA)
        surface.blit(pygame.transform.scale(self.textures['empty'], self.rect.size), (10,5), (0, 0, self.rect.width, self.rect.height-10))
        surface.blit(pygame.transform.scale(self.textures['full'], self.rect.size), (10, 5), (0, 0, self.rect.width*self.value, self.rect.height-10))
        surface.blit(pygame.transform.scale(self.textures['ball'], (self.rect.height,self.rect.height)), (self.rect.width*self.value+10, 0))

        screen.blit(surface, self.rect.topleft)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.value = min(max((mouse_pos[0]-self.rect.left-10)/self.rect.width,0),1)
            return True
        return False