import pygame, math
from GameManagers.assetmanager import AssetManager

from perlin import PerlinNoise

class Planet:
    def __init__(self, position, radius, features, textures, mass, sea_level):
        self.position = position
        self.radius = radius
        self.features = features
        self.textures = textures
        self.mass = mass
        self.sea_level = sea_level
        self.points = []
        self.quality = 10

        self.mask_surface = pygame.Surface((1280,720))
        self.mask_water = pygame.Surface((1280,720))
    def generate_points(self, seed):
        num_points = int(self.radius * math.pi / self.quality)
        values = PerlinNoise.generate_values(seed, 5, num_points)
        for i in range(num_points):
            if i > 9395 and i < 9454:
                self.points.append(0.1)
            else:
                self.points.append(values[i])

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

    def render(self, screen, rect, world, time_active):
        self.mask_surface.fill((0,0,0))
        self.mask_water.fill((0,0,0))
        if self.intersection(rect):
            
            expanded_rect = pygame.Rect(rect.left-20, rect.top-20, rect.width+40, rect.height+40)
            points_land = []
            points_water = []
            for i in range(70):
                index = i-35+world.rocket.planet_point_index
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

                pygame.draw.polygon(self.mask_water, (0,128,255), points_water)
                pygame.draw.polygon(self.mask_surface, (255,255,255), points_land)

                masked_texture_surface = self.textures['land'].copy()
                masked_texture_water = self.textures['water'].copy()

                masked_texture_surface.scroll(-rect.left%32-32, -rect.top%32-32)
                masked_texture_water.scroll((-rect.left+int(time_active/5))%32-32, -rect.top%32-32)

                masked_texture_water.blit(self.mask_water, (0,0), None, pygame.BLEND_RGBA_MULT)
                masked_texture_water.set_colorkey((0,0,0))

                masked_texture_surface.blit(self.mask_surface, (0,0), None, pygame.BLEND_RGBA_MULT)
                masked_texture_surface.set_colorkey((0,0,0))

                screen.blit(masked_texture_water, (0,0))
                screen.blit(masked_texture_surface, (0,0))
        else:
            return

class Box:
    def __init__(self, position, size, mass, id, static=0):
        self.id = id
        self.size = size

        # 0 = normal, 1 = fixed position, 2 = fixed
        self.static = static

        self.angular_friction = 0.1
        self.kinetic_friction = 0.3

        self.mass = mass
        self.position = position
        self.linear_velocity = [0,0]
        self.linear_acceleration = [0,0]
        self.elasticity = 1
        self.angle = 0
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.moment_of_inertia = 1/12*self.mass*(self.size[0]*self.size[0]+self.size[1]*self.size[1])

        self.planet_point_index = 0

    def update(self, world, forces):
        dt = 1/60

        sum_forces = [0,0]
        for force in forces:
            sum_forces[0] += force[1][0]
            sum_forces[1] += force[1][1]
        linear_acceleration = [sum_forces[0]/self.mass, sum_forces[1]/self.mass]

        #fake cross product axby-bxay
        torque = 0
        for force in forces:
            if force[0][0] != 0 or force[0][1] != 0:
                torque += (force[0][0]*force[1][1]-force[1][0]*force[0][1])
        angular_acceleration = -torque/self.moment_of_inertia

        # "collide"
        for planet in world.planets:
            self.test_points = []
            rocket_angle = math.atan2(self.position[1]-planet.position[1], self.position[0]-planet.position[0])
            self.planet_point_index = int(rocket_angle/(math.pi*2)*len(planet.points))%len(planet.points)
            for i in range(6):
                rocket_angle = math.atan2(self.position[1]-planet.position[1], self.position[0]-planet.position[0])
                planet_point_index = int(rocket_angle/(math.pi*2)*len(planet.points)+i-3)%len(planet.points)
                point_angle = 2*math.pi*planet_point_index/len(planet.points)
                for point in self.rotate_points(self.angle):
                    dist_to_center = math.hypot(point[0]-planet.position[0], point[1]-planet.position[1])
                    surface_radius = planet.points[planet_point_index]*100+planet.radius
                    if dist_to_center < surface_radius:
                        self.position[0] += math.cos(point_angle)*(surface_radius-dist_to_center)
                        self.position[1] += math.sin(point_angle)*(surface_radius-dist_to_center)


        if pygame.Rect(self.position[0]-self.size[0]/2,self.position[1]-self.size[1]/2,*self.size).colliderect(world.platform):
            self.position[1] = world.platform.top-(self.size[1]/2)
            self.linear_velocity[1] = 0
            self.angular_velocity = 0
            self.angular_acceleration = 0
            linear_acceleration[1] = 0

        self.linear_accerlation = linear_acceleration
        self.angular_acceleration = angular_acceleration
        if self.static == 0:
            self.linear_velocity[0] += linear_acceleration[0]*dt
            self.linear_velocity[1] += (linear_acceleration[1])*dt
            self.position[0] += self.linear_velocity[0]*dt
            self.position[1] += self.linear_velocity[1]*dt

        if self.static != 2:
            self.angular_velocity += angular_acceleration*dt
            self.angle += self.angular_velocity*dt

    def render(self, screen, camera):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255,0,0), (0, 0, self.size[0], self.size[1]))  
        rotated_image = pygame.transform.rotate(surface, -self.angle)
        screen.blit(rotated_image, (self.position[0]-camera.left-rotated_image.get_width()/2,self.position[1]-camera.top-rotated_image.get_height()/2))
        for point in self.rotate_points(self.angle):
            pygame.draw.rect(screen, (0,0,255), (point[0]-2-camera.left,point[1]-2-camera.top,4,4))
        pygame.draw.line(screen, (0,255,0), (self.position[0]-camera.left, self.position[1]-camera.top), (self.position[0]-camera.left-50*math.sin(self.angle*math.pi/180), self.position[1]-camera.top+50*math.cos(self.angle*math.pi/180)))

    def rotate_points(self, angle):
        angle_rads = angle*math.pi/180
        points = [[self.position[0]-self.size[0]/2,self.position[1]-self.size[1]/2], [self.position[0]+self.size[0]/2,self.position[1]-self.size[1]/2], [self.position[0]+self.size[0]/2,self.position[1]+self.size[1]/2], [self.position[0]-self.size[0]/2,self.position[1]+self.size[1]/2]]
        rotated_points = []
        for point in points:
            x = point[0]-self.position[0]
            y = point[1]-self.position[1]
            rotated_points.append([x*math.cos(angle_rads)-y*math.sin(angle_rads)+self.position[0], x*math.sin(angle_rads)+y*math.cos(angle_rads)+self.position[1]])
        return rotated_points

    def do_polygons_intersect(self, other_square):
        a = self.rotate_points(self.angle)
        b = other_square.rotate_points(other_square.angle)

        polygons = [a, b];
        minA, maxA, projected, i, i1, j, minB, maxB = None, None, None, None, None, None, None, None

        normal = [0,0]
        depth = 1000000

        for i in range(len(polygons)):

            # for each polygon, look at each edge of the polygon, and determine if it separates
            # the two shapes
            polygon = polygons[i];
            for i1 in range(len(polygon)):

                # grab 2 vertices to create an edge
                i2 = (i1 + 1) % len(polygon);
                p1 = polygon[i1];
                p2 = polygon[i2];

                # find the line perpendicular to this edge
                normal = { 'x': p2[1] - p1[1], 'y': p1[0] - p2[0] };

                minA, maxA = None, None
                # for each vertex in the first shape, project it onto the line perpendicular to the edge
                # and keep track of the min and max of these values
                for j in range(len(a)):
                    projected = normal['x'] * a[j][0] + normal['y'] * a[j][1];
                    if (minA is None) or (projected < minA): 
                        minA = projected

                    if (maxA is None) or (projected > maxA):
                        maxA = projected

                # for each vertex in the second shape, project it onto the line perpendicular to the edge
                # and keep track of the min and max of these values
                minB, maxB = None, None
                for j in range(len(b)): 
                    projected = normal['x'] * b[j][0] + normal['y'] * b[j][1]
                    if (minB is None) or (projected < minB):
                        minB = projected

                    if (maxB is None) or (projected > maxB):
                        maxB = projected

                # if there is no overlap between the projects, the edge we are looking at separates the two
                # polygons, and we know there is no overlap
                if (maxA < minB) or (maxB < minA):
                    return [False, [normal['x'], normal['y']]];

        return [True, [normal['x'], normal['y']]]