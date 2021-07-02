# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

import math
from utils.homogeneus_coordinate import HomogeneusCoor


class Pos3d(HomogeneusCoor):

    def __init__(self, x, y, z, w=1):
        HomogeneusCoor.__init__(self, x, y, z, w)

    @staticmethod
    def list_to_pos(lst):
        return Pos3d(lst[0], lst[1], lst[2])

    def is_equal(self, pos):
        if (self.x == pos.x):
            if (self.y == pos.y):
                if (self.z == pos.z):
                    return True
        return False

    def is_close(self, pos):
        if math.isclose(self.x, pos.x):
            if math.isclose(self.y, pos.y):
                if math.isclose(self.z, pos.z):
                    return True
        return False

    def getPositionArray(self):
        return [self.x, self.y, self.z, self.w]

    @staticmethod
    def calculate_mid_point(poses):

        x, y, z = 0, 0, 0
        for p in poses:
            x += p.x
            y += p.y
            z += p.z

        n_pos = len(poses)

        return Pos3d(x / n_pos, y / n_pos, z / n_pos)

    @staticmethod
    def rotate_point(point, origin, angle, axis="x"):

        pz = point.z
        px = point.x

        oz = origin.z
        ox = origin.x

        pZ = math.cos(angle) * (pz - oz) - math.sin(angle) * (px - ox) + oz

        pX = math.sin(angle) * (pz - oz) + math.cos(angle) * (px - ox) + ox

        pX = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (pz - oz)
        pZ = oz + math.sin(angle) * (px - ox) + math.cos(angle) * (pz - oz)

        return Pos3d(pX, point.y, pZ)

    @staticmethod
    def calculate_distance(p1, p2):
        return math.pow((math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2) + math.pow(p1.z - p2.z, 2)), 1 / 2)

    @staticmethod
    def cal_distance_value(p1, p2):
        return (((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2) + ((p1.z - p2.z) ** 2))
