import pygame, random

class ParticleSystem:
    def __init__(self, size, base_particle, velocity_range, angular_velocity_range, acceleration, rate):
        self.surface = pygame.Surface(size)
        self.lifetime = 0
        self.base_particle = base_particle
        self.velocity_range = velocity_range
        self.angular_velocity_range = angular_velocity_range
        self.acceleration = acceleration
        self.rate = rate
        self.particles = []
    
    def update(self):
        if self.lifetime % self.rate == 0:
            p = Particle.copy(self.base_particle)
            p.angular_velocity = random.randint(self.angular_velocity_range[0], self.angular_velocity_range[1])
            p.velocity = [random.randint(self.velocity_range[0], self.velocity_range[1]), random.randint(self.velocity_range[2], self.velocity_range[3])]
            self.particles.append(p)
        removal = []
        for i in range(len(self.particles)):
            particle = self.particles[i]
            particle.velocity[0] += self.acceleration[0]
            particle.velocity[1] += self.acceleration[1]
            particle.position[0] += particle.velocity[0]
            particle.position[1] += particle.velocity[1]
            particle.rotation += particle.angular_velocity
            if not self.surface.get_rect().collidepoint(*particle.position):
                removal.append(i)
        d = 0
        for index in removal:
            self.particles.pop(index-d)
            d += 1

        self.lifetime += 1

    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)

class Particle:
    def __init__(self, surface):
        self.surface = surface
        self.position = [0,0]
        self.velocity = [0,0]
        self.angular_velocity = 0
        self.rotation = 0
    
    @staticmethod
    def copy(particle):
        p = Particle(particle.surface)
        p.position = [*particle.position]
        p.velocity = [*particle.velocity]
        p.rotation = particle.rotation
        p.angular_velocity = particle.angular_velocity
        return p
    
    def render(self, screen):
        screen.blit(pygame.transform.rotate(self.surface, self.rotation), self.position)