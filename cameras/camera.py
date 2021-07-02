# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from utils.vec3d import Vec3d
from cameras.window import Window


class Camera:

    def __init__(self, eye, center, window =Window(100,200), window_distance = 100):
        self.eye = eye
        self.center = center
        self.up = Vec3d(0,1, 0)
        self.window = window
        self.window_distance = window_distance
