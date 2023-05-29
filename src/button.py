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