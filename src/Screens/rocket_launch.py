import pygame, math
from object import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class RocketLaunchScreen:
    def __init__(self):
        self.ui = []

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        world.render(self.surface, self.timeActive)

        forces = []
        for planet in world.planets:
            dist = math.hypot(world.rocket.position[0]-planet.position[0], world.rocket.position[1]-planet.position[1])
            vector_planet = [(planet.position[0]-world.rocket.position[0])/dist, (planet.position[1]-world.rocket.position[1])/dist]
            gravitational_force = 6.67*10**-10*planet.mass*world.rocket.mass/(dist*dist)
            forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
        if inputManager.keys[pygame.K_w]:
            forces.append([(0,0),(30*math.sin(world.rocket.angle*math.pi/180),-30*math.cos(world.rocket.angle*math.pi/180))])
        if inputManager.keys[pygame.K_a]:
            forces.append([(0,30),(-1000,0)])
            forces.append([(0,-30),(1000,0)])
        if inputManager.keys[pygame.K_d]:
            forces.append([(0,30),(1000,0)])
            forces.append([(0,-30),(-1000,0)])
        world.rocket.update(world, forces)

        if inputManager.key_press['m']:
            game.mode = 2

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass