import pygame, math

from box import Box
from grid import Grid
from planet import Planet

class World:
    def __init__(self):
        self.camera = pygame.Rect(0,0,1280,720)
        self.grid = Grid()
        self.rocket = Box(self.grid, [700,250], [150,375], 1, 0, 0)
        self.platform = pygame.Rect(200,250,1000,50)
        self.planets = []
        self.planet_counter = 0
        self.zoom = 0.1

    def add_planet(self, position, radius, textures, mass, sea_level, map_color, static=True, velocity=[0,0]):
        planet = Planet(position, radius, textures, mass, sea_level, self.planet_counter, map_color, static, velocity)
        self.planet_counter += 1
        self.planets.append(planet)

    def generate_world(self):
        for planet in self.planets:
            planet.get_points(2)

    def add_planet_atmosphere(self, color, size):
        self.planets[self.planet_counter-1].add_atmosphere(color, size)


    def get_altitude(self, planet):
        dist_sq = (self.rocket.position[0]-planet.position[0])**2+(self.rocket.position[1]-planet.position[1])**2
        return math.sqrt(dist_sq)-planet.radius
    
    def in_planet_atmosphere(self, planet):
        if not planet.atmosphere: return False
        if math.hypot(planet.position[0]-self.rocket.position[0], planet.position[1]-self.rocket.position[1])-planet.radius < planet.atmosphere_size: return True
        return False

    def get_gravitational_force(self):
        forces = []
        for planet in self.planets:
            dist = math.hypot(self.rocket.position[0]-planet.position[0], self.rocket.position[1]-planet.position[1])
            vector_planet = [(planet.position[0]-self.rocket.position[0])/dist, (planet.position[1]-self.rocket.position[1])/dist]
            gravitational_force = 6.67*10**-10*planet.mass*self.rocket.mass/(dist*dist)
            forces.append([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])
        sum = [0,0]
        for force in forces:
            sum[0] += force[0]
            sum[1] += force[1]
        return math.hypot(*sum)

    def update(self, forces):
        for planet in self.planets:
            planet.update(self)

            dist = math.hypot(self.rocket.position[0]-planet.position[0], self.rocket.position[1]-planet.position[1])
            vector_planet = [(planet.position[0]-self.rocket.position[0])/dist, (planet.position[1]-self.rocket.position[1])/dist]
            gravitational_force = 6.67*10**-10*planet.mass*self.rocket.mass/(dist*dist)
            forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
        self.rocket.update(self, forces)

    def render(self, screen, time_active):
        atmosphere_color = (0,0,0)
        altitude = self.get_altitude(self.planets[0])
        for planet in self.planets:
            if altitude < planet.atmosphere_size and self.in_planet_atmosphere(planet):
                atmosphere_color = planet.atmosphere_color.lerp(pygame.Color(0,0,0), max(min(altitude/planet.atmosphere_size,1),0))
        screen.fill(atmosphere_color)

        self.camera.x = self.rocket.position[0] - self.camera.width/2
        self.camera.y = self.rocket.position[1] - self.camera.height/2
        
        for planet in self.planets:
            planet.render(screen, self.camera, self.rocket, time_active)
        
        pygame.draw.rect(screen, (128,128,128), (self.platform.left-self.camera.left,self.platform.top-self.camera.top,self.platform.width,self.platform.height))
        self.rocket.render(screen, self.camera, time_active)

    def draw_paths(self, screen, pos, zoom, offset):
        positions = []
        rocket_position = [*self.rocket.position]
        velocities = []
        rocket_velocity = [*self.rocket.linear_velocity]
        points = []
        rocket_points = []
        path_length = 200

        rocket_points.append([640+(self.rocket.position[0]-pos[0])*1.1**zoom+offset[0], 360+(self.rocket.position[1]-pos[1])*1.1**zoom+offset[1]])
        for i in range(len(self.planets)):
            positions.append([*self.planets[i].position])
            velocities.append([*self.planets[i].linear_velocity])
            points.append([])

        #update planets
        for i in range(path_length):
            dt = 150
            
            for j in range(len(self.planets)):
                forces = []
                if self.planets[j].static: continue
                for planet in self.planets:
                    if planet.id == self.planets[j].id: continue
                    dist = math.hypot(planet.position[0]-positions[j][0], planet.position[1]-positions[j][1])
                    vector_planet = [(planet.position[0]-positions[j][0])/dist, (planet.position[1]-positions[j][1])/dist]
                    gravitational_force = 6.67*10**-10*planet.mass*self.planets[j].mass/(dist*dist)
                    forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                
                sum_forces = [0,0]
                for force in forces:
                    sum_forces[0] += force[1][0]
                    sum_forces[1] += force[1][1]
                acceleration = [sum_forces[0]/self.planets[j].mass, sum_forces[1]/self.planets[j].mass]
                velocities[j][0] += acceleration[0]*dt
                velocities[j][1] += acceleration[1]*dt
                positions[j][0] += velocities[j][0]*dt
                positions[j][1] += velocities[j][1]*dt

                points[j].append([640+(positions[j][0]-pos[0])*1.1**zoom+offset[0], 360+(positions[j][1]-pos[1])*1.1**zoom+offset[1]])

        #recalculate positions for different fucking timestep
        positions = []
        velocities = []
        for i in range(len(self.planets)):
            positions.append([*self.planets[i].position])
            velocities.append([*self.planets[i].linear_velocity])

        for i in range(path_length):
            dt = max(self.get_altitude(self.planets[0])/10000,2)
            
            for j in range(len(self.planets)):
                forces = []
                if self.planets[j].static: continue
                for planet in self.planets:
                    if planet.id == self.planets[j].id: continue
                    dist = math.hypot(planet.position[0]-positions[j][0], planet.position[1]-positions[j][1])
                    vector_planet = [(planet.position[0]-positions[j][0])/dist, (planet.position[1]-positions[j][1])/dist]
                    gravitational_force = 6.67*10**-10*planet.mass*self.planets[j].mass/(dist*dist)
                    forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                
                sum_forces = [0,0]
                for force in forces:
                    sum_forces[0] += force[1][0]
                    sum_forces[1] += force[1][1]
                acceleration = [sum_forces[0]/self.planets[j].mass, sum_forces[1]/self.planets[j].mass]
                velocities[j][0] += acceleration[0]*dt
                velocities[j][1] += acceleration[1]*dt
                positions[j][0] += velocities[j][0]*dt
                positions[j][1] += velocities[j][1]*dt

        for i in range(path_length):
            dt = max(self.get_altitude(self.planets[0])/10000,2)

            forces = []
            for i in range(len(positions)):
                planet = positions[i]
                dist = math.hypot(rocket_position[0]-planet[0], rocket_position[1]-planet[1])
                vector_planet = [(planet[0]-rocket_position[0])/dist, (planet[1]-rocket_position[1])/dist]
                gravitational_force = 6.67*10**-10*self.planets[i].mass*self.rocket.mass/(dist*dist)
                forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                
            sum_forces = [0,0]
            for force in forces:
                sum_forces[0] += force[1][0]
                sum_forces[1] += force[1][1]
            acceleration = [sum_forces[0]/self.rocket.mass, sum_forces[1]/self.rocket.mass]
            rocket_velocity[0] += acceleration[0]*dt
            rocket_velocity[1] += acceleration[1]*dt
            rocket_position[0] += rocket_velocity[0]*dt
            rocket_position[1] += rocket_velocity[1]*dt

            rocket_points.append([640+(rocket_position[0]-pos[0])*1.1**zoom+offset[0], 360+(rocket_position[1]-pos[1])*1.1**zoom+offset[1]])
            if pygame.Rect(rocket_position[0]-640,rocket_position[1]-360, 1280, 720).collidepoint(640+(rocket_position[0]-pos[0])*1.1**zoom+offset[0], 360+(rocket_position[1]-pos[1])*1.1**zoom+offset[1]):
                break

        for path in points:
            if len(path) > 1:
                pygame.draw.lines(screen, (255,255,255), False, path)
        pygame.draw.lines(screen, (200,255,200), False, rocket_points)

    def render_map(self, screen, offset, font):
        for planet in self.planets:
            planet.render_map(screen, self, self.rocket.position, self.zoom, offset, font)

        self.draw_paths(screen, self.rocket.position, self.zoom, offset)

        rocket_surface = pygame.Surface((20,20), pygame.SRCALPHA)
        pygame.draw.rect(rocket_surface, (200,200,200), (0,0,20,20))
        rotated_surface = pygame.transform.rotate(rocket_surface, -self.rocket.angle)
        screen.blit(rotated_surface, (640-rotated_surface.get_width()/2+offset[0],360-rotated_surface.get_height()/2+offset[1]))