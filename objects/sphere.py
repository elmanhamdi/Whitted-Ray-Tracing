# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from utils import *
from utils import HomogeneusCoor as hc
from objects import *
from objects.material import Material
import random

class Sphere:
    def __init__(self, x=1, y=1, z=1, scale=1, radius=1, center=Pos3d(0, 0, 0, 1), material=Material()):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.scale = scale
        self.center = center
        self.material = material

    def normal_of_a_point(self, point):
        return hc.normalize(Vec3d.positions_to_vec(point, self.center))
        # return hc.normalize(hc.sub(point, self.center))

    # Idea from https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection
    def intersect(self, ray):
        # ray.start_pos = Pos3d.sub(ray.start_pos, self.center)
        q = hc.sub(self.center, ray.start_pos)

        vDotQ = Vec3d.dot_product(ray.direction, q)
        squareDiffs = Vec3d.dot_product(q, q) - (self.radius * self.radius)
        discrim = vDotQ * vDotQ - squareDiffs

        if discrim >= 0:
            root = discrim ** (1 / 2)
            t0 = (vDotQ - root)
            t1 = (vDotQ + root)
            return Intersect(t1, t0, ray) if t0 > t1 else Intersect(t0, t1, ray)

        return -1

    # @staticmethod
    def generate_random_hemisphere_ray(self, normal_start):

        normal_dir = self.normal_of_a_point(normal_start)

        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = random.uniform(-1, 1)

        n = normal_dir.normalize()
        vec = Vec3d(x, y, z).normalize()

        vec = vec.add(n).normalize()
        return Ray(normal_start , vec)

        '''
        normal_dir = self.normal_of_a_point(normal_start)
        x_angle = random.randint(-90, 90)
        y_angle = random.randint(-90, 90)
        z_angle = random.randint(-90, 90)
        ray_end_point = Transformations.rotate_point(x_angle, y_angle, z_angle, hc.add(normal_dir, normal_start), normal_start)
        #print(normal_dir)
        ray_dir = Vec3d.positions_to_vec( ray_end_point , normal_start)
        #print(ray_dir)
        #print('\n')
        return Ray(Pos3d.sub(self.center, normal_start), ray_dir)
        #return Ray(normal_start, ray_dir)
        '''



class Intersect:
    def __init__(self, t0, t1, ray):
        self.t0 = t0
        self.t1 = t1
        self.p0 = -1
        self.p1 = -1
        self.calculatePoints(ray)

    def __str__(self):
        return 't0:' + str(self.t0) + '  p0:' + str(self.p0) + ' |  t1:' + str(self.t1) + '  t2:' + str(self.p1)

    def calculatePoints(self, ray):
        normalized_dir = hc.normalize(ray.direction)
        point0 = hc.add(ray.start_pos, hc.mul(normalized_dir, self.t0))
        point1 = hc.add(ray.start_pos, hc.mul(normalized_dir, self.t1))

        self.p0 = point0
        self.p1 = point1
