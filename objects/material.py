# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from utils import *

class Material:
    def __init__(self, color=Color(255, 255, 255, 255), refractive=False, reflective=False, ior = 1.5):
        self.color = color
        self.refractive = refractive
        self.reflective = reflective
        self.ior = ior