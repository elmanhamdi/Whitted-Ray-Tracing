# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

class Color:
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '[' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ', ' + str(self.a) + ']'

    #    def __mul__(self, other):
    #       self.r *= other
    #      self.g *= other
    #     self.b *= other
    #    self.a *= other

    def __mul__(self, other):
        r = other * self.r
        g = other * self.g
        b = other * self.b
        a = other * self.a
        return Color(r, g, b, a)

    def __add__(self, other_color):
        r = other_color.r + self.r
        g = other_color.g + self.g
        b = other_color.b + self.b
        a = other_color.a + self.a
        return Color(r, g, b, a)

    def getRGB(self):
        return [self.r, self.g, self.b]
