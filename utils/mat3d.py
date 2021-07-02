# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021


import math

from utils.pos3d import Pos3d
import numpy


class Mat3d:
    def __init__(self, matrix_lst):
        self.matrix_lst = matrix_lst


    def mat_mul(self, matrix):
        new_lst = [[0] * len(matrix.matrix_lst[0]) for i in range(len(self.matrix_lst))]
        for i in range(len(self.matrix_lst)):
            for k in range(len(matrix.matrix_lst[0])):
                sum = 0
                for j in range(len(matrix.matrix_lst)):
                    sum += self.matrix_lst[i][j] * matrix.matrix_lst[j][k]
                new_lst[i][k] = sum
        return Mat3d(new_lst)

    def transpose(self):
        new_lst = [[0] * len(self.matrix_lst) for i in range(len(self.matrix_lst[0]))]
        for i in range(len(new_lst)):
            for j in range(len(new_lst[i])):
                new_lst[i][j] = self.matrix_lst[j][i]
        new_matrix = Mat3d(new_lst)
        return new_matrix

    def vecmul(self, vector):
        x = self._vecmul(self.matrix_lst[0], vector.x)
        y = self._vecmul(self.matrix_lst[1], vector.y)
        z = self._vecmul(self.matrix_lst[2], vector.z)
        w = self._vecmul(self.matrix_lst[3], vector.w)
        a = Pos3d(x[0] + y[0] + z[0] + w[0], x[1] + y[1] + z[1] + w[1], x[2] + y[2] + z[2] + w[2],
                  x[3] + y[3] + z[3] + w[3])
        return a

    def _vecmul(self, lst, vec_p):
        return [lst[0] * vec_p, lst[1] * vec_p, lst[2] * vec_p, lst[3] * vec_p]

    def product(self, other):
        cols = []
        tmp = self.matrix_lst

        for l in other.matrix_lst:
            x = (tmp[0][0] * l[0]) + (tmp[1][0] * l[1]) + (tmp[2][0] * l[2]) + (tmp[3][0] * l[3])
            y = (tmp[0][1] * l[0]) + (tmp[1][1] * l[1]) + (tmp[2][1] * l[2]) + (tmp[3][1] * l[3])
            z = (tmp[0][2] * l[0]) + (tmp[1][2] * l[1]) + (tmp[2][2] * l[2]) + (tmp[3][2] * l[3])
            w = (tmp[0][3] * l[0]) + (tmp[1][3] * l[1]) + (tmp[2][3] * l[2]) + (tmp[3][3] * l[3])
            cols.append([x, y, z, w])
        return Mat3d(cols)

    @staticmethod
    def product3(mat1, mat2, mat3):
        tmp = mat1.product(mat2)
        return tmp.product(mat3)

    @staticmethod
    def create_translation_matrix(trans_x, trans_y, trans_z):
        return Mat3d([[1, 0, 0, trans_x], [0, 1, 0, trans_y], [0, 0, 1, trans_z], [0, 0, 0, 1]])

    @staticmethod
    def create_scale_matrix(value):
        return Mat3d([[value, 0, 0, 0], [0, value, 0, 0], [0, 0, value, 0], [0, 0, 0, value]])

    @staticmethod
    def create_rotation_matrix_for_x_axis(degree, typ='degree'):
        if typ == 'radian':
            cos = math.cos(degree)
            sin = math.sin(degree)
        else:
            cos = math.cos(math.radians(degree))
            sin = math.sin(math.radians(degree))
        return Mat3d([[1, 0, 0, 0], [0, cos, -sin, 0], [0, sin, cos, 0], [0, 0, 0, 1]])

    @staticmethod
    def create_rotation_matrix_for_y_axis(degree, typ='degree'):
        if typ == 'radian':
            cos = math.cos(degree)
            sin = math.sin(degree)
        else:
            cos = math.cos(math.radians(degree))
            sin = math.sin(math.radians(degree))
        return Mat3d([[cos, 0, sin, 0], [0, 1, 0, 0], [-sin, 0, cos, 0], [0, 0, 0, 1]])

    @staticmethod
    def create_rotation_matrix_for_z_axis(degree, typ='degree'):
        if typ == 'radian':
            cos = math.cos(degree)
            sin = math.sin(degree)
        else:
            cos = math.cos(math.radians(degree))
            sin = math.sin(math.radians(degree))
        return Mat3d([[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # This part taken from 06-HelloFaces.py (belongs Erdem Taylan)
    @staticmethod
    def getProjMatrix(near, far, aspect, fov):
        f = numpy.reciprocal(numpy.tan(numpy.divide(numpy.deg2rad(fov), 2.0)))
        base = near - far
        term_0_0 = numpy.divide(f, aspect)
        term_2_2 = numpy.divide(far + near, base)
        term_2_3 = numpy.divide(numpy.multiply(numpy.multiply(2, near), far), base)

        # https://en.wikibooks.org/wiki/GLSL_Programming/Vertex_Transformations
        return numpy.array([term_0_0, 0.0, 0.0, 0.0,
                            0.0, f, 0.0, 0.0,
                            0.0, 0.0, term_2_2, -1,
                            0.0, 0.0, term_2_3, 0.0], dtype='float32')

    @staticmethod
    def getViewMatrix(camZAxis, camYAxis, camXAxis, cam_eye):
        # THIS HAS A LOT OF HARD CODED STUFF
        # we first calculate camera x, y, z axises and from those we assemble a rotation matrix.
        # Once that is done we add in the translation.
        # We assume camera always look at the world space origin.
        # Up vector is always in the direction of global yAxis.

        rotMat = numpy.array([camXAxis[0], camYAxis[0], camZAxis[0], 0.0,
                              camXAxis[1], camYAxis[1], camZAxis[1], 0.0,
                              camXAxis[2], camYAxis[2], camZAxis[2], 0.0,
                              0.0, 0.0, 0.0, 1.0], dtype='float32').reshape(4, 4)

        traMat = numpy.array([1.0, 0.0, 0.0, 0.0,
                              0.0, 1.0, 0.0, 0.0,
                              0.0, 0.0, 1.0, 0.0,
                              -cam_eye.x, -cam_eye.y, -cam_eye.z, 1.0], dtype='float32').reshape(4, 4)

        return traMat.dot(rotMat)

    @staticmethod
    def getModelMatrix(position):
        return numpy.array([1.0, 0.0, 0.0, 0.0,
                            0.0, 1.0, 0.0, 0.0,
                            0.0, 0.0, 1.0, 0.0,
                            position.x, position.y, position.z, 1.0], dtype='float32')
