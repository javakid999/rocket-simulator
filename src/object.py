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

    def update(self, other, force):
        dt = 1/60
        forces = [force]

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


        intersect = self.do_polygons_intersect(other)
        if intersect[0]:
            #elasticity coefficient
            e = (self.elasticity + other.elasticity) / 2
            
            #poi and velocity
            poi = [(self.position[0]+other.position[0])/2,(self.position[1]+other.position[1])/2]
            r_a = [poi[0]-self.position[0],poi[1]-self.position[1]]
            r_b = [poi[0]-other.position[0],poi[1]-other.position[1]]
            d_a = math.hypot(poi[0]-self.position[0],poi[1]-self.position[1])
            d_b = math.hypot(poi[0]-other.position[0],poi[1]-other.position[1])
            v_a = [d_a * self.angular_velocity * -math.sin(self.angle) + self.linear_velocity[0], d_a * self.angular_velocity * -math.cos(self.angle) + self.linear_velocity[1]]
            v_b = [d_b * other.angular_velocity * -math.sin(other.angle) + other.linear_velocity[0], d_b * other.angular_velocity * -math.cos(other.angle) + other.linear_velocity[1]]
            r_v = [v_a[0] - v_b[0], v_a[1] - v_b[1]]

            #calculate j
            n = intersect[1]
            j_num = -n[0] * (1+e) * r_v[0]+ -n[1] * (1+e) * r_v[1]
            j_denom = n[0]*n[0]*(1/self.mass+1/other.mass)+n[1]*n[1]*(1/self.mass+1/other.mass)+(n[0]*r_a[0]+n[1]*r_a[1])**2/self.moment_of_inertia+(n[0]*r_b[0]+n[1]*r_b[1])**2/other.moment_of_inertia
            if j_denom == 0: 
                j = 0
            else:
                j = j_num/j_denom
            #move them
            self.linear_velocity[0] += n[0]*j/self.mass
            self.linear_velocity[1] += n[1]*j/self.mass
            self.angular_velocity += (r_a[0]*j*n[0]+r_a[1]*j*n[1])/self.moment_of_inertia

            other.linear_velocity[0] += -n[0]*j/other.mass
            other.linear_velocity[1] += -n[1]*j/other.mass
            other.angular_velocity += (r_b[0]*j*-n[0]+r_b[1]*j*-n[1])/other.moment_of_inertia

        self.position[0] += self.linear_velocity[0]*dt + 1/2*linear_acceleration[0]*dt*dt
        self.position[1] += self.linear_velocity[1]*dt + 1/2*(linear_acceleration[1]+0.0)*dt*dt
        self.linear_velocity[0] += linear_acceleration[0]*dt
        self.linear_velocity[1] += linear_acceleration[1]*dt

        self.angle += self.angular_velocity*dt + 1/2*angular_acceleration*dt*dt
        self.angular_velocity += angular_acceleration*dt

    def render(self, screen):
        surface = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255,0,0), (0, 0, self.size[0], self.size[1]))
        rotated_image = pygame.transform.rotate(surface, -self.angle)
        screen.blit(rotated_image, (self.position[0]-rotated_image.get_width()/2,self.position[1]-rotated_image.get_height()/2))
        for point in self.rotate_points(self.angle):
            pygame.draw.rect(screen, (0,0,255), (point[0]-2,point[1]-2,4,4))

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