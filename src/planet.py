import pygame, math, json, os
from perlin import PerlinNoise

class Planet:
    def __init__(self, position, radius, textures, mass, sea_level, planet_id, map_color, static = True, velocity = [0,0]):
        self.id = planet_id
        self.position = position
        self.linear_velocity = velocity
        self.radius = radius
        self.textures = textures
        self.mass = mass
        self.static = static
        self.map_color = map_color
        self.sea_level = sea_level
        self.points = []
        self.features = []
        self.quality = 10

        self.atmosphere = False
        self.atmosphere_size = 0
        self.atmosphere_color = (0,0,0)

        self.mask_surface = pygame.Surface((1280,720))
        self.mask_water = pygame.Surface((1280,720))

    def add_atmosphere(self, color, size):
        self.atmosphere_size = size
        self.atmosphere_color = color
        self.atmosphere = True

    def add_feature(self, name, start, points):
        end = start + len(points)
        self.features.append([name, start, end, points, 2*math.pi*(((start+end)/2)/int(self.radius * math.pi / self.quality))])

    def save_points(self):
        planet_data = {}
        planet_data['id'] = self.id
        planet_data['quality'] = self.quality
        planet_data['features'] = self.features
        planet_data['points'] = self.points
        
        with open('./src/Saves/planet_'+str(self.id)+'.json', 'w') as outfile:
            json.dump(planet_data, outfile)

    def get_points(self, seed):
        if not os.path.exists('./src/Saves/planet_'+str(self.id)+'.json'):
            num_points = int(self.radius * math.pi / self.quality)
            values = PerlinNoise.generate_values(seed, 5, num_points)
            for i in range(num_points):
                feature_point = False
                for feature in self.features:
                    if feature[1] <= i < feature[2]:
                        self.points.append(feature[3][i-feature[1]])
                        feature_point = True
                        break
                if feature_point == False:
                        self.points.append(values[i])

            self.save_points()
        else:
            planet = json.load(open('./src/Saves/planet_'+str(self.id)+'.json'))
            self.features = planet['features']
            self.quality = planet['quality']
            self.points = planet['points']

    def update(self, world):
        dt = world.time_step

        if self.static:
            return
        else:
            forces = []
            for planet in world.planets:
                if planet.id == self.id: continue
                dist = math.hypot(self.position[0]-planet.position[0], self.position[1]-planet.position[1])
                vector_planet = [(planet.position[0]-self.position[0])/dist, (planet.position[1]-self.position[1])/dist]
                gravitational_force = 6.67*10**-10*planet.mass*self.mass/(dist*dist)
                forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
            
            sum_forces = [0,0]
            for force in forces:
                sum_forces[0] += force[1][0]
                sum_forces[1] += force[1][1]
            linear_acceleration = [sum_forces[0]/self.mass, sum_forces[1]/self.mass]
            self.linear_velocity[0] += linear_acceleration[0]*dt
            self.linear_velocity[1] += (linear_acceleration[1])*dt
            self.position[0] += self.linear_velocity[0]*dt
            self.position[1] += self.linear_velocity[1]*dt

    def intersection(self, rect):
            half_width = rect.width / 2
            half_height = rect.height / 2

            # Calculate the center of the rectangle
            rect_x = rect.center[0]
            rect_y = rect.center[1]

            # Calculate the closest point on the rectangle to the circle
            closest_x = max(rect_x - half_width, min(self.position[0], rect_x + half_width))
            closest_y = max(rect_y - half_height, min(self.position[1], rect_y + half_height))

            # Calculate the distance between the closest point and the circle center
            distance = math.sqrt((closest_x - self.position[0]) ** 2 + (closest_y - self.position[1]) ** 2)

            # Check if the distance is less than or equal to the circle radius
            if distance <= self.radius:
                return True
            else:
                return False

    def render(self, screen, rect, rocket, time_active):
        self.mask_surface.fill((0,0,0))
        self.mask_water.fill((0,0,0))
        if self.intersection(rect):
            expanded_rect = pygame.Rect(rect.left-20, rect.top-20, rect.width+40, rect.height+40)
            points_land = []
            points_water = []
            for i in range(70):
                rocket_angle = math.atan2(rocket.position[1]-self.position[1], rocket.position[0]-self.position[0])
                planet_point_index = int(rocket_angle/(math.pi*2)*len(self.points))%len(self.points)
                index = i-35+planet_point_index
                angle = 2*math.pi*((index)/len(self.points))
                position = [self.position[0]-rect.left+(self.radius+100*self.points[index])*math.cos(angle),self.position[1]-rect.top+(self.radius+100*self.points[index])*math.sin(angle)]
                position_water = [self.position[0]-rect.left+(self.radius+100*self.sea_level)*math.cos(angle),self.position[1]-rect.top+(self.radius+100*self.sea_level)*math.sin(angle)]
                if expanded_rect.collidepoint(self.position[0]+self.radius*math.cos(angle),self.position[1]+self.radius*math.sin(angle)):
                    points_land.append([*position])
                    points_water.append([*position_water])
            if len(points_land) > 2:
                corners = [rect.topright, rect.bottomright, rect.topleft, rect.bottomleft]
                for i in range(len(corners)):
                    dist_to_corner = (corners[i][0] - self.position[0])**2 + (corners[i][1] - self.position[1])**2
                    if dist_to_corner < self.radius**2:
                        points_land.append([corners[i][0]-rect.left, corners[i][1]-rect.top])
                        points_water.append([corners[i][0]-rect.left, corners[i][1]-rect.top])

                pygame.draw.polygon(self.mask_water, (255,255,255), points_water)
                pygame.draw.polygon(self.mask_surface, (255,255,255), points_land)

                masked_texture_surface = self.textures['land'].copy()
                masked_texture_water = self.textures['water'].copy()

                masked_texture_surface.scroll((self.position[0]-rect.left)%32-32, (self.position[1]-rect.top)%32-32)
                masked_texture_water.scroll((self.position[0]-rect.left+int(time_active/5))%32-32, (self.position[1]-rect.top)%32-32)

                masked_texture_water.blit(self.mask_water, (0,0), None, pygame.BLEND_RGBA_MULT)
                masked_texture_water.set_colorkey((0,0,0))

                masked_texture_surface.blit(self.mask_surface, (0,0), None, pygame.BLEND_RGBA_MULT)
                masked_texture_surface.set_colorkey((0,0,0))

                screen.blit(masked_texture_water, (0,0))
                screen.blit(masked_texture_surface, (0,0))
        else:
            return
    
    def draw_path(self, screen, world, pos, zoom, offset):
        if self.static:
            return
        else:
            dt = 150
            points = []
            position = [*self.position]
            velocity = [*self.linear_velocity]
            for i in range(190):
                forces = []
                for planet in world.planets:
                    if planet.id == self.id: continue
                    dist = math.hypot(position[0]-planet.position[0], position[1]-planet.position[1])
                    vector_planet = [(planet.position[0]-position[0])/dist, (planet.position[1]-position[1])/dist]
                    gravitational_force = 6.67*10**-10*planet.mass*self.mass/(dist*dist)
                    forces.append([[0,0], ([vector_planet[0]*gravitational_force, vector_planet[1]*gravitational_force])])
                
                sum_forces = [0,0]
                for force in forces:
                    sum_forces[0] += force[1][0]
                    sum_forces[1] += force[1][1]
                acceleration = [sum_forces[0]/self.mass, sum_forces[1]/self.mass]
                velocity[0] += acceleration[0]*dt
                velocity[1] += (acceleration[1])*dt
                position[0] += velocity[0]*dt
                position[1] += velocity[1]*dt

                points.append([640+(position[0]-pos[0])*1.1**zoom+offset[0], 360+(position[1]-pos[1])*1.1**zoom+offset[1]])
            pygame.draw.lines(screen, (255,255,255), False, points)

    def render_map(self, screen, world, pos, zoom, offset, font):
        if self.atmosphere:
            pygame.draw.circle(screen, (40,40,40), (640+(self.position[0]-pos[0])*1.1**zoom+offset[0],360+(self.position[1]-pos[1])*1.1**zoom+offset[1]), (self.radius+self.atmosphere_size)*1.1**zoom)
        pygame.draw.circle(screen, self.map_color, (640+(self.position[0]-pos[0])*1.1**zoom+offset[0],360+(self.position[1]-pos[1])*1.1**zoom+offset[1]), self.radius*1.1**zoom)
        for feature in self.features:
            position = (self.position[0]+math.cos(feature[4])*self.radius, self.position[1]+math.sin(feature[4])*self.radius)
            position = (640+(position[0]-pos[0])*1.1**zoom+offset[0],360+(position[1]-pos[1])*1.1**zoom+offset[1])
            pygame.draw.circle(screen, (255,128,128), position, 5)
            screen.blit(font.render(feature[0], False, (255,255,255)), position)