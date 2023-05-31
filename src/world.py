import pygame

from object import Box, Planet

class World:
    def __init__(self):
        self.camera = pygame.Rect(0,0,1280,720)
        self.rocket = Box([700,20],[40,50],1,0,0)
        self.platform = pygame.Rect(200,250,1000,50)
        self.planets = []
        self.zoom = 0.1

    def add_planet(self, position, radius, features, textures, mass, sea_level):
        planet = Planet(position, radius, features, textures, mass, sea_level)
        planet.generate_points(2)
        self.planets.append(planet)

    def render(self, screen, time_active):
        self.camera.x = self.rocket.position[0] - self.camera.width/2
        self.camera.y = self.rocket.position[1] - self.camera.height/2
        
        for planet in self.planets:
            planet.render(screen, self.camera, self, time_active)
        
        pygame.draw.rect(screen, (128,128,128), (self.platform.left-self.camera.left,self.platform.top-self.camera.top,self.platform.width,self.platform.height))
        self.rocket.render(screen, self.camera)

    def render_map(self, screen, offset):
        for planet in self.planets:
            planet.render_map(screen, self.rocket.position, self.zoom, offset)

        rocket_surface = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.rect(rocket_surface, (200,200,200), (0,0,20,20))
        rotated_surface = pygame.transform.rotate(rocket_surface, -self.rocket.angle)
        screen.blit(rotated_surface, (640-rotated_surface.get_width()/2+offset[0],360-rotated_surface.get_height()/2+offset[1]))