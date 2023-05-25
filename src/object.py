import pygame, math

class Square:
    def __init__(self, position, size, mass, static=False):
        self.size = size
        self.static = static

        self.mass = mass
        self.position = position
        self.linear_velocity = [0,0]
        self.elasticity = 0.2
        self.angle = 0
        self.angular_velocity = 0

        self.moment_of_inertia = 1/12*self.mass*(self.size[0]*self.size[0]+self.size[1]*self.size[1])

    def update(self, other):
        dt = 1/60
        forces = [[(0,0),(0,0)]]

        sum_forces = [0,0]
        for force in forces:
            sum_forces[0] += force[1][0]
            sum_forces[1] += force[1][1]
        linear_acceleration = [sum_forces[0]/self.mass, sum_forces[1]/self.mass]

        #fake cross product axby-bxay
        torque = 0
        for force in forces:
            cm = (force[0][0] - self.position[0], force[0][1] - self.position[1])
            torque += cm[0]*force[1][1]-force[1][0]*cm[1]
        angular_acceleration = torque/self.moment_of_inertia

        if self.do_polygons_intersect(other):
            #elasticity coefficient
            e = (self.elasticity + other.elasticity) / 2
            
            #poi and velocity
            poi = [(self.position[0]+other.position[0])/2,(self.position[1]+other.position[1])/2]
            v_a = [math.hypot(poi[0]-self.position[0],poi[1]-self.position[1]) * self.angular_velocity * -math.sin(self.angle) + self.linear_velocity[0], math.hypot(poi[0]-self.position[0],poi[1]-self.position[1]) * self.angular_velocity * -math.cos(self.angle) + self.linear_velocity[1]]
            v_b = [math.hypot(poi[0]-other.position[0],poi[1]-other.position[1]) * other.angular_velocity * -math.sin(other.angle) + other.linear_velocity[0], math.hypot(poi[0]-other.position[0],poi[1]-other.position[1]) * other.angular_velocity * -math.cos(other.angle) + other.linear_velocity[1]]
            r_v = [v_a[0] - v_b[0], v_a[1] - v_b[1]]

            #calculate j
            n = [0,0]
            j = ([-n[0] * (1+e) * r_v[0], -n[1] * (1+e) * r_v[1]])/([n[0]*n[0]*(1/self.mass+1/other.mass),n[1]*n[1]*(1/self.mass+1/other.mass)])

            #move them

        self.position[0] += self.linear_velocity[0]*dt + 1/2*linear_acceleration[0]*dt*dt
        self.position[1] += self.linear_velocity[1]*dt + 1/2*(linear_acceleration[1]+9.8)*dt*dt
        self.linear_velocity[0] += linear_acceleration[0]*dt
        self.linear_velocity[1] += linear_acceleration[1]*dt

        self.angle += self.angular_velocity*dt + 1/2*angular_acceleration*dt*dt
        self.angular_velocity += angular_acceleration*dt

    def render(self, screen):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255,0,0), (0, 0, self.size[0], self.size[1]))
        rotated_image = pygame.transform.rotate(surface, -self.angle)
        screen.blit(rotated_image, (self.position[0]-rotated_image.get_width()/2,self.position[1]-rotated_image.get_height()/2))

    def rotate_points(self, angle):
        points = [[self.position[0]-self.size[0],self.position[1]-self.size[1]], [self.position[0]+self.size[0],self.position[1]-self.size[1]], [self.position[0]+self.size[0],self.position[1]+self.size[1]], [self.position[0]-self.size[0],self.position[1]+self.size[1]]]
        rotated_points = []
        for point in points:
            x = point[0]
            y = point[1]
            rotated_points.append([x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle)])
        return rotated_points

    def do_polygons_intersect(self, other_square):
        a = self.get_points(self.angle)
        b = other_square.get_points(other_square.angle)

        polygons = [a, b];
        minA, maxA, projected, i, i1, j, minB, maxB = None, None, None, None, None, None, None, None

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
                    return False;

        return True