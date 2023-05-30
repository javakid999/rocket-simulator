import pygame, math
from object import Box
from particle import Particle, ParticleSystem
from statemachine import StateMachine
from world import World

class MapScreen:
    def __init__(self):
        self.ui = []

        self.surface = pygame.Surface((1280,720))
        self.timeActive = 0

    def render(self, screen, assets, inputManager, world, game):
        self.surface.fill((0,0,0))

        world.render_map(self.surface, inputManager.mouse_pos, inputManager.global_mouse_offset, inputManager.click_pos)

        if inputManager.keys[pygame.K_q]:
            world.zoom -= 0.1
        if inputManager.keys[pygame.K_e]:
            world.zoom += 0.1
        if inputManager.key_press['m']:
            game.mode = 1

        forces = []
        for planet in world.planets:
            dist = math.hypot(world.rocket.position[0]-planet.position[0], world.rocket.position[1]-planet.position[1])
            vector_planet = [(planet.position[0]-world.rocket.position[0])/dist, (planet.position[1]-world.rocket.position[1])/dist]
            gravitational_force = 6.67*10**-10*planet.mass*world.rocket.mass/(dist*dist)
            forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
        world.rocket.update(world, forces)

        for item in self.ui:
            pass

        screen.blit(self.surface, (0,0))
        self.timeActive += 1

    def update_ui(self, pos, game):
        for item in self.ui:
            if item.update(-1, pos):
                pass