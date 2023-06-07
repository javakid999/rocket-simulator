import pygame

class RocketPart:
    def __init__(self, position, size, mass, image, rotation):
        self.position = position
        self.size = size
        self.mass = mass
        self.image = image
        self.rotation = rotation

        self.part_surface = pygame.Surface((50,50), pygame.SRCALPHA)
        self.part_surface.blit(image, (0,0))

    def render(self, screen, offset):
        rotated_surface = pygame.transform.rotate(self.part_surface, -self.rotation*90)
        screen.blit(rotated_surface, (self.position[0]*50+offset[0], self.position[1]*50+offset[1]))

class Engine(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (2,2), 220, image, rotation)
        self.activated = False

class FuelTank(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (2,2), 330, image, rotation)
        self.full = 1

class Separator(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (1,2), 50, image, rotation)
        self.activated = False

class Capsule(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (2,2), 120, image, rotation)
        self.activated = False