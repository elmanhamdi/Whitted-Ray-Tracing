# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from utils import *


class Light:
    def __init__(self, position=Pos3d(0, 0, 0), color=[1, 1, 1, 1], intensity=1):
        self.position = position
        self.color = color
        self.intensity = intensity


class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '[' + self.r + ', ' + self.g + ', ' + self.b + ', ' + self.a + ']'
