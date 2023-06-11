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

    def render(self, screen, offset, frame):
        rotated_surface = pygame.transform.rotate(self.part_surface, -self.rotation*90)
        screen.blit(rotated_surface, (self.position[0]*50+offset[0], self.position[1]*50+offset[1]))

class Engine(RocketPart):
    def __init__(self, position, rotation, image, consumption, force):
        super().__init__(position, (2,2), 220, image, rotation)
        self.activated = False
        self.force = force
        self.consumption = consumption
        self.firing = False

class FuelTank(RocketPart):
    def __init__(self, position, rotation, image, fuel):
        super().__init__(position, (2,2), 330, image, rotation)
        self.fuel = 1

class Separator(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (2,2), 50, image, rotation)
        self.activated = False

class Capsule(RocketPart):
    def __init__(self, position, rotation, image):
        super().__init__(position, (2,2), 120, image, rotation)
        self.activated = False

class CheeseMachine(RocketPart):
    def __init__(self, position, rotation, images):
        super().__init__(position, (2,2), 120, images[0], rotation)
        
        self.part_surfaces = []
        for image in images:
            surface = pygame.Surface((50,50), pygame.SRCALPHA)
            surface.blit(image, (0,0))
            self.part_surfaces.append(surface)

    def render(self, screen, offset, frame):
        rotated_surface = pygame.transform.rotate(self.part_surfaces[frame], -self.rotation*90)
        screen.blit(rotated_surface, (self.position[0]*50+offset[0], self.position[1]*50+offset[1]))