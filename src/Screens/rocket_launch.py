import pygame, math
from object import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class RocketLaunchScreen:
    def __init__(self, asset_manager):
        self.ui = []

        self.world = World()
        self.planet_texture = asset_manager.generateTiledTexture('dirt', (1312,752))
        self.water_texture = asset_manager.generateTiledTexture('water', (1312,752))
        self.world.add_planet([700,637300], 637000, [], {'land': self.planet_texture, 'water': self.water_texture}, 5.97*10**21, 0.08)

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, pos, globalMouseOffset, keys):
        self.surface.fill((0,0,0))

        self.world.render(self.surface, self.timeActive)

        forces = []
        for planet in self.world.planets:
            dist = math.hypot(self.world.rocket.position[0]-planet.position[0], self.world.rocket.position[1]-planet.position[1])
            vector_planet = [(planet.position[0]-self.world.rocket.position[0])/dist, (planet.position[1]-self.world.rocket.position[1])/dist]
            gravitational_force = 6.67*10**-10*planet.mass*self.world.rocket.mass/(dist*dist)
            forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
        if keys[pygame.K_w]:
            forces.append([(0,0),(30*math.sin(self.world.rocket.angle*math.pi/180),-30*math.cos(self.world.rocket.angle*math.pi/180))])
        if keys[pygame.K_a]:
            forces.append([(0,30),(-1000,0)])
            forces.append([(0,-30),(1000,0)])
        if keys[pygame.K_d]:
            forces.append([(0,30),(1000,0)])
            forces.append([(0,-30),(-1000,0)])
        self.world.rocket.update(self.world, forces)

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass