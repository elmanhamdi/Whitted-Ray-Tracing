# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021


import math
from utils.homogeneus_coordinate import HomogeneusCoor
import numpy


class Vec3d(HomogeneusCoor):

    def __init__(self, x, y, z, w=0):
        HomogeneusCoor.__init__(self, x, y, z, w)

    def dot_product(self, cord):
        x = self.x * cord.x
        y = self.y * cord.y
        z = self.z * cord.z

        return (x + y + z)

    def cross_product(self, cord, dtype=None):
        x = (self.y * cord.z) - (self.z * cord.y)
        y = (self.z * cord.x) - (self.x * cord.z)
        z = (self.x * cord.y) - (self.y * cord.x)

        if dtype == "float32":
            return numpy.array([x, y, z, 0.0], dtype='float32')
        return Vec3d(x, y, z)

    def get_length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** (0.5)

    def find_angle(self, vector):
        dot_pro = self.dot_product(vector)
        length_self = self.get_length()
        length_vec = vector.get_length()

        return math.degrees(math.acos(dot_pro / (length_self * length_vec)))

    def projection(self, vector):
        unit_vec = vector.get_unit_vector()
        len_vec = vector.get_length
        dot_self = self.dot_product(vector)

        return unit_vec.mul(dot_self / len_vec)

    def get_unit_vector(self):
        length = self.get_length()
        if length != 0:
            return Vec3d.hom_to_vec(self.mul(1 / self.get_length()))
        else:
            return self

    def getVectorArray(self):
        return (self.x, self.y, self.z, self.w)

    def toList(self):
        return [self.x, self.y, self.z, self.w]

    # https://codereview.stackexchange.com/questions/43928/algorithm-to-get-an-arbitrary-perpendicular-vector
    def perpendicular_vector(self):
        if self.y == 0 and self.z == 0:
            if self.x == 0:
                raise ValueError('zero vector')
            else:
                return self.cross_product(Vec3d(0, 1, 0))
        return self.cross_product(Vec3d(1, 0, 0))

    @staticmethod
    def list_to_vec(lst):
        return Vec3d(lst[0], lst[1], lst[2])

    @staticmethod
    def positions_to_vec(pos1, pos2):
        return Vec3d(pos1.x - pos2.x, pos1.y - pos2.y, pos1.z - pos2.z)

    @staticmethod
    def hom_to_vec(hom):
        return Vec3d(hom.x, hom.y, hom.z)
