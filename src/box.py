import pygame, math
from GameManagers.assetmanager import AssetManager

class Box:
    def __init__(self, grid, position, size, mass, id, static=0):
        self.grid = grid
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
        self.size = [world.grid.size[0]*15, world.grid.size[1]*15]
        mass = 0
        for i in range(len(world.grid.parts)):
            mass += world.grid.parts[i].mass
        self.mass = mass
        self.moment_of_inertia = 1/12*self.mass*(self.size[0]*self.size[0]+self.size[1]*self.size[1])

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
        surface.blit(self.grid.render_launch(), (0,0))
        
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

        polygons = [a, b]
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