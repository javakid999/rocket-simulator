import pygame

class RocketPart:
    def __init__(self, position, size, mass, color, rotation):
        self.position = position
        self.size = size
        self.mass = mass
        self.color = color
        self.rotation = rotation

        self.part_surface = pygame.Surface((50,50), pygame.SRCALPHA)
        pygame.draw.rect(self.part_surface, self.color, (0, 0, 50, 50))
        pygame.draw.rect(self.part_surface, (0,0,0), (20, 40, 10, 10))

    def render(self, screen, offset):
        rotated_surface = pygame.transform.rotate(self.part_surface, self.rotation*90)
        screen.blit(rotated_surface, (self.position[0]*50+offset[0], self.position[1]*50+offset[1]))

class Engine(RocketPart):
    def __init__(self, position, rotation):
        super().__init__(position, (2,2), 450, (255,0,0), rotation)
        self.activated = False

class FuelTank(RocketPart):
    def __init__(self, position, rotation):
        super().__init__(position, (2,2), 670, (255,255,0), rotation)
        self.full = 1

class Separator(RocketPart):
    def __init__(self, position, rotation):
        super().__init__(position, (1,2), 100, (0,255,0), rotation)
        self.activated = False

class Capsule(RocketPart):
    def __init__(self, position, rotation):
        super().__init__(position, (2,2), 250, (0,255,255), rotation)
        self.activated = False