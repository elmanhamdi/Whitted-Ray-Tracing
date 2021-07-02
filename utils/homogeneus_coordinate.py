# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021


class HomogeneusCoor:
    def __init__(self, x, y, z, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ', ' + str(self.w) + ')'

    def __sub__(self, other):
        self.x -= other
        self.y -= other
        self.z -= other

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        z = self.z * other
        return self.__class__(x, y, z, self.w)

    def add(self, cord):  # It can caused some errors
        if type(cord) == type(0) or type(cord) == type(0.0):
            x = self.x + cord
            y = self.y + cord
            z = self.z + cord
        else:
            x = self.x + cord.x
            y = self.y + cord.y
            z = self.z + cord.z

        return self.__class__(x, y, z)

    def sub(self, cord):
        if type(cord) == type(0) or type(cord) == type(0.0):
            x = self.x - cord
            y = self.y - cord
            z = self.z - cord
        else:
            x = self.x - cord.x
            y = self.y - cord.y
            z = self.z - cord.z

        return self.__class__(x, y, z)

    def mul(self, value):
        if type(value) == type(0) or type(value) == type(0.0):
            x = self.x * value
            y = self.y * value
            z = self.z * value
            w = self.w * value
        else:
            x = self.x * value.x
            y = self.y * value.y
            z = self.z * value.z
            w = self.w * value.w

        tmp = self.__class__(x, y, z)
        tmp.w = w
        return tmp

    def exp(self, value):
        x = self.x ** value
        y = self.y ** value
        z = self.z ** value
        # w = self.w ** value

        tmp = self.__class__(x, y, z)
        # tmp.w = w
        return tmp

    def normalize(self):
        l = ((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** (1 / 2)
        return self.__class__(self.x / l, self.y / l, self.z / l)

    @staticmethod
    def list_to_homo(lst):
        return HomogeneusCoor(lst[0], lst[1], lst[2], lst[3])

    def to_str(self):
        str = '', self.x, self.y, self.z, self.w
        return str

    def to_lst(self):
        return [self.x, self.y, self.z, self.w]

    def compare(self, other):
        if (round(self.x, 3) == round(other.x, 3)):
            if (round(self.y, 3) == round(other.y, 3)):
                if (round(self.z, 3) == round(other.z, 3)):
                    return True
        return False
