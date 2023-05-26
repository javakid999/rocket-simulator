import pygame, math

class Box:
    def __init__(self, position, size, mass, id, static=0):
        self.id = id
        self.size = size

        # 0 = normal, 1 = fixed position, 2 = fixed
        self.static = static

        self.mass = mass
        self.position = position
        self.linear_velocity = [0,0]
        self.linear_acceleration = [0,0]
        self.elasticity = 1
        self.angle = 0
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.moment_of_inertia = 1/12*self.mass*(self.size[0]*self.size[0]+self.size[1]*self.size[1])

    def update(self, scene, forces):
        dt = 1/60

        sum_forces = [0,0]
        for force in forces:
            sum_forces[0] += force[1][0]
            sum_forces[1] += force[1][1]
        linear_acceleration = [sum_forces[0]/self.mass, sum_forces[1]/self.mass]

        #fake cross product axby-bxay
        torque = 0
        for force in forces:
            cm = (force[0][0] - self.position[0], force[0][1] - self.position[1])
            if force[0][0] != 0 or force[0][1] != 0:
                torque += cm[0]*force[1][1]-force[1][0]*cm[1]
        angular_acceleration = torque/self.moment_of_inertia

        # "collide"

        self.linear_accerlation = linear_acceleration
        self.angular_acceleration = angular_acceleration
        if self.static == 0:
            self.linear_velocity[0] += linear_acceleration[0]*dt
            self.linear_velocity[1] += (linear_acceleration[1]+9.8)*dt
            self.position[0] += self.linear_velocity[0]*dt
            self.position[1] += self.linear_velocity[1]*dt

        if self.static != 2:
            self.angular_velocity += angular_acceleration*dt
            self.angle += self.angular_velocity*dt

    def find_contact_points(self, other):
        contact1 = [0,0]
        contact2 = [0,0]
        count = 0
        dist = 100000

        points_self = self.rotate_points(self.angle)
        points_other = other.rotate_points(other.angle)
        for i in range(len(points_self)):
            point = points_self[i]
            for j in range(len(points_other)):
                va = points_other[j]
                vb = points_other[(j+1)%len(points_other)]

                d = self.point_segment_distance(point, va, vb)
                distance_squared = d[0]
                cp = d[1]
                if abs(distance_squared - dist) < 0.01:
                    if not(abs(cp[0]-contact1[0]) < 0.01 and abs(cp[1]-contact1[1]) < 0.01 and abs(cp[0]-contact2[0]) < 0.01 and abs(cp[1]-contact2[1]) < 0.01):
                        contact2 = [*cp]
                        count = 2
                elif (distance_squared < dist):
                    dist = distance_squared
                    count = 1
                    contact1 = cp
        for i in range(len(points_other)):
            point = points_other[i]
            for j in range(len(points_self)):
                va = points_self[j]
                vb = points_self[(j+1)%len(points_self)]

                d = self.point_segment_distance(point, va, vb)
                distance_squared = d[0]
                cp = d[1]
                if abs(distance_squared - dist) < 0.01:
                    if not(abs(cp[0]-contact1[0]) < 0.01 and abs(cp[1]-contact1[1]) < 0.01 and abs(cp[0]-contact2[0]) < 0.01 and abs(cp[1]-contact2[1]) < 0.01):
                        contact2 = [*cp]
                        count = 2
                elif (distance_squared < dist):
                    dist = distance_squared
                    count = 1
                    contact1 = cp

        return [count, contact1, contact2]

    @staticmethod
    def point_segment_distance(point,line_start,line_end):
        ab = [line_end[0] - line_start[0], line_end[1] - line_start[1]];
        ap = [point[0] - line_start[0], point[1] - line_start[1]];

        proj = ap[0] * ab[0] + ap[1] * ab[1]
        abLenSq = ab[0]**2+ab[1]**2
        d = proj / abLenSq

        if d <= 0:
            cp = line_start
        elif d >= 1:
            cp = line_end
        else:
            cp = [line_start[0] + ab[0] * d, line_start[1] + ab[1] * d]

        distance_squared = (point[0]-cp[0])**2+(point[1]-cp[1])**2
        return [distance_squared, cp]

    @staticmethod
    def get_line_intersection(x0,y0,x1,y1,x2,y2,x3,y3):
        s1_x = x1 - x0     
        s1_y = y1 - y0
        s2_x = x3 - x2     
        s2_y = y3 - y2
        d = (-s2_x * s1_y + s1_x * s2_y)
        s = (-s1_y * (x0 - x2) + s1_x * (y0 - y2)) / d
        t = ( s2_x * (y0 - y2) - s2_y * (x0 - x2)) / d

        if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
            x = x0 + (t * s1_x);
            y = y0 + (t * s1_y);
            return True, [x,y]
        return False, [0,0]

    def resolve_collision(self, other, intersect, poi):
        #elasticity coefficient
        e = (self.elasticity + other.elasticity) / 2
        
        #velocity
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