# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from lights import *

MAX_NUM_OF_LIGHTS = 8


class Scene:
    def __init__(self):
        self.nodes = []
        self.lights = []

    def add(self, node):
        if type(node) == Light:
            if len(self.lights) > MAX_NUM_OF_LIGHTS + 1:
                print("Max light size  has been exceed")
                exit(1)

            self.lights.append(node)
        else:
            self.nodes.append(node)
