import json
import pygame, math

from box import Box
from grid import Grid
from planet import Planet
from part import Engine

class World:
    def __init__(self, assets):
        self.camera = pygame.Rect(0,0,1280,720)
        flames = []
        for i in range(20):
            flames.append(assets['00'+str(i+10)])
        self.grid = Grid(flames)
        self.rockets = []
        self.selected_rocket = 0
        self.platform = pygame.Rect(200,250,1000,50)
        self.planets = []
        self.planet_counter = 0
        self.save_state_counter = 0
        self.time_step = 1/60
        self.zoom = 0.1

    def add_planet(self, position, radius, textures, mass, sea_level, map_color, static=True, velocity=[0,0]):
        planet = Planet(position, radius, textures, mass, sea_level, self.planet_counter, map_color, static, velocity)
        self.planet_counter += 1
        self.planets.append(planet)

    def generate_world(self):
        for planet in self.planets:
            planet.get_points(2)
        self.save_state('Launch')

    def time_step_increase(self):
        if self.time_step == 1/60:
            self.time_step = 1/30
        elif self.time_step == 1/30:
            self.time_step = 1/10
        elif self.time_step == 1/10:
            self.time_step = 1/5
        elif self.time_step == 1/5:
            self.time_step = 1
    
    def save_state(self, name=-1):
        state = {}
        if name != -1:
            state['name'] = name
        else:
            state['name'] = 'Quicksave ' + str(self.save_state_counter)
        state['rocket'] = []
        for rocket in self.rockets:
            state['rocket'].append({'position': rocket.position, 'linear_velocity': rocket.linear_velocity, 'angle': rocket.angle, 'angular_velocity': rocket.angular_velocity})

        state['planets'] = {}
        for planet in self.planets:
            state['planets'][str(planet.id)] = {
                'position': planet.position,
                'linear_velocity': planet.linear_velocity
            }

        filename = 'Quicksave '+str(self.save_state_counter)
        if name != -1:
            filename = name
        with open('./src/Saves/save_states/'+filename+'.json', 'w') as outfile:
            json.dump(state, outfile)
        self.save_state_counter += 1
        

    def load_state(self, name):
        state = json.load(open('./src/Saves/save_states/'+name+'.json'))
        for i in range(len(self.rockets)):
            self.rockets[i].position = state['rocket'][i]['position']
            self.rockets[i].angle = state['rocket'][i]['angle']

        for i in range(len(self.planets)):
            self.planets[i].position = state['planets'][str(self.planets[i].id)]['position']
            self.planets[i].linear_velocity = state['planets'][str(self.planets[i].id)]['linear_velocity']

        for planet in self.planets:
            planet.update(self)
        for rocket in self.rockets:
            rocket.update(self, [])

        for i in range(len(self.rockets)):
            self.rockets[i].linear_velocity = state['rocket'][i]['linear_velocity']
            self.rockets[i].linear_acceleration = [0,0]
            self.rockets[i].angular_velocity = state['rocket'][i]['angular_velocity']
            self.rockets[i].angular_acceleration = 0

    def time_step_decrease(self):
        if self.time_step == 1:
            self.time_step = 1/5
        elif self.time_step == 1/5:
            self.time_step = 1/10
        elif self.time_step == 1/10:
            self.time_step = 1/30
        elif self.time_step == 1/30:
            self.time_step = 1/60

    def update(self, forces):
        for planet in self.planets:
            planet.update(self)

        for i in range(len(self.rockets)):
            for planet in self.planets:
                dist = math.hypot(self.rockets[i].position[0]-planet.position[0], self.rockets[i].position[1]-planet.position[1])
                vector_planet = [(planet.position[0]-self.rockets[i].position[0])/dist, (planet.position[1]-self.rockets[i].position[1])/dist]
                gravitational_force = 6.67*10**-10*planet.mass*self.rockets[i].mass/(dist*dist)
                forces[i].append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
            self.rockets[i].update(self, forces[i])

    def render(self, screen, time_active):
        atmosphere_color = (0,0,0)
        altitude = self.rockets[self.selected_rocket].get_altitude(self.planets[0])
        for planet in self.planets:
            if altitude < planet.atmosphere_size and self.rockets[self.selected_rocket].in_planet_atmosphere(planet):
                atmosphere_color = planet.atmosphere_color.lerp(pygame.Color(0,0,0), max(min(altitude/planet.atmosphere_size,1),0))
        screen.fill(atmosphere_color)

        self.camera.x = self.rockets[self.selected_rocket].position[0] - self.camera.width/2
        self.camera.y = self.rockets[self.selected_rocket].position[1] - self.camera.height/2
        
        for planet in self.planets:
            planet.render_experimental(screen, self.camera, self.rockets[self.selected_rocket], time_active)
        
        pygame.draw.rect(screen, (128,128,128), (self.platform.left-self.camera.left,self.platform.top-self.camera.top,self.platform.width,self.platform.height))
        for rocket in self.rockets:
            rocket.render(screen, self.camera, time_active)

    def draw_paths(self, screen, pos, zoom, offset):
        planet_positions = []
        rocket_positions = []
        planet_velocities = []
        rocket_velocities = []
        planet_points = []
        rocket_points = []
        path_length = 200

        
            
        for rocket in self.rockets:
            rocket_positions.append([*rocket.position])
            rocket_velocities.append([*rocket.linear_velocity])
            rocket_points.append([])
        
        for i in range(len(self.rockets)):
            rocket_points[i].append([640+(rocket.position[0]-pos[0])*1.1**zoom+offset[0], 360+(rocket.position[1]-pos[1])*1.1**zoom+offset[1]])

        for i in range(len(self.planets)):
            planet_positions.append([*self.planets[i].position])
            planet_velocities.append([*self.planets[i].linear_velocity])
            planet_points.append([])

        #update planets
        for i in range(path_length):
            dt = 150
            
            for j in range(len(self.planets)):
                forces = []
                if self.planets[j].static: continue
                for planet in self.planets:
                    if planet.id == self.planets[j].id: continue
                    dist = math.hypot(planet.position[0]-planet_positions[j][0], planet.position[1]-planet_positions[j][1])
                    vector_planet = [(planet.position[0]-planet_positions[j][0])/dist, (planet.position[1]-planet_positions[j][1])/dist]
                    gravitational_force = 6.67*10**-10*planet.mass*self.planets[j].mass/(dist*dist)
                    forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                
                sum_forces = [0,0]
                for force in forces:
                    sum_forces[0] += force[1][0]
                    sum_forces[1] += force[1][1]
                acceleration = [sum_forces[0]/self.planets[j].mass, sum_forces[1]/self.planets[j].mass]
                planet_velocities[j][0] += acceleration[0]*dt
                planet_velocities[j][1] += acceleration[1]*dt
                planet_positions[j][0] += planet_velocities[j][0]*dt
                planet_positions[j][1] += planet_velocities[j][1]*dt

                planet_points[j].append([640+(planet_positions[j][0]-pos[0])*1.1**zoom+offset[0], 360+(planet_positions[j][1]-pos[1])*1.1**zoom+offset[1]])

        #recalculate positions for different fucking timestep
        for k in range(len(rocket_positions)):
            planet_positions = []
            planet_velocities = []
            for i in range(len(self.planets)):
                planet_positions.append([*self.planets[i].position])
                planet_velocities.append([*self.planets[i].linear_velocity])

            for i in range(path_length):
                dt = max(self.rockets[self.selected_rocket].get_altitude(self.planets[0])/10000,2)
                
                for j in range(len(self.planets)):
                    forces = []
                    if self.planets[j].static: continue
                    for planet in self.planets:
                        if planet.id == self.planets[j].id: continue
                        dist = math.hypot(planet.position[0]-planet_positions[j][0], planet.position[1]-planet_positions[j][1])
                        vector_planet = [(planet.position[0]-planet_positions[j][0])/dist, (planet.position[1]-planet_positions[j][1])/dist]
                        gravitational_force = 6.67*10**-10*planet.mass*self.planets[j].mass/(dist*dist)
                        forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                    
                    sum_forces = [0,0]
                    for force in forces:
                        sum_forces[0] += force[1][0]
                        sum_forces[1] += force[1][1]
                    acceleration = [sum_forces[0]/self.planets[j].mass, sum_forces[1]/self.planets[j].mass]
                    planet_velocities[j][0] += acceleration[0]*dt
                    planet_velocities[j][1] += acceleration[1]*dt
                    planet_positions[j][0] += planet_velocities[j][0]*dt
                    planet_positions[j][1] += planet_velocities[j][1]*dt

            #get points for rocket
            for i in range(path_length):
                dt = max(self.rockets[self.selected_rocket].get_altitude(self.planets[0])/10000,2)

                forces = []
                for j in range(len(planet_positions)):
                    planet = planet_positions[j]
                    dist = math.hypot(rocket_positions[k][0]-planet[0], rocket_positions[k][1]-planet[1])
                    vector_planet = [(planet[0]-rocket_positions[k][0])/dist, (planet[1]-rocket_positions[k][1])/dist]
                    gravitational_force = 6.67*10**-10*self.planets[j].mass*self.rockets[k].mass/(dist*dist)
                    forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                    
                sum_forces = [0,0]
                for force in forces:
                    sum_forces[0] += force[1][0]
                    sum_forces[1] += force[1][1]
                acceleration = [sum_forces[0]/self.rockets[k].mass, sum_forces[1]/self.rockets[k].mass]
                rocket_velocities[k][0] += acceleration[0]*dt
                rocket_velocities[k][1] += acceleration[1]*dt
                rocket_positions[k][0] += rocket_velocities[k][0]*dt
                rocket_positions[k][1] += rocket_velocities[k][1]*dt

                rocket_points[k].append([640+(rocket_positions[k][0]-pos[0])*1.1**zoom+offset[0], 360+(rocket_positions[k][1]-pos[1])*1.1**zoom+offset[1]])
                if pygame.Rect(rocket_positions[k][0]-640,rocket_positions[k][1]-360, 1280, 720).collidepoint(640+(rocket_positions[k][0]-pos[0])*1.1**zoom+offset[0], 360+(rocket_positions[k][1]-pos[1])*1.1**zoom+offset[1]):
                    break
                for planet in self.planets:
                    if math.hypot(rocket_positions[k][0]-planet.position[0], rocket_positions[k][1]-planet.position[1]) < planet.radius:
                        for path in planet_points:
                            if len(path) > 1:
                                pygame.draw.lines(screen, (255,255,255), False, path)
                        for path in rocket_points:
                            if len(path) > 1:
                                pygame.draw.lines(screen, (200,255,200), False, path)
                        return

        for path in planet_points:
            if len(path) > 1:
                pygame.draw.lines(screen, (255,255,255), False, path)
        for path in rocket_points:
            if len(path) > 1:
                pygame.draw.lines(screen, (200,255,200), False, path)

    def render_map(self, screen, offset, font):
        for planet in self.planets:
            planet.render_map(screen, self, self.rockets[self.selected_rocket].position, self.zoom, offset, font)

        self.draw_paths(screen, self.rockets[self.selected_rocket].position, self.zoom, offset)

        for rocket in self.rockets:
            rocket_surface = pygame.Surface((20,20), pygame.SRCALPHA)
            pygame.draw.rect(rocket_surface, (200,200,200), (0,0,20,20))
            rotated_surface = pygame.transform.rotate(rocket_surface, -rocket.angle)
            screen.blit(rotated_surface, (640-rotated_surface.get_width()/2+offset[0],360-rotated_surface.get_height()/2+offset[1]))