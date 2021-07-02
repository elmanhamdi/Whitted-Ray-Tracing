# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from utils import *


class Ray:
    def __init__(self, start_pos=Pos3d(0, 0, 0, 1), direction=Vec3d(1, 1, 1, 0)):
        self.start_pos = start_pos
        self.direction = direction

    def __str__(self):

        return  '\nRay Properties+\n' +'start_pos: ' + str(self.start_pos) +'\ndirection: ' +str(self.direction)

    @property
    def start_pos(self):
        return self.__start_pos

    @start_pos.setter
    def start_pos(self, start_pos):
        self.__start_pos = start_pos

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    @staticmethod
    def calculated_bounced_ray(coming_ray_dir, surface_normal, intersect_pos):

        #r=d−2(d⋅n)n

        tmp = surface_normal.mul(2*coming_ray_dir.dot_product(surface_normal))
        r = coming_ray_dir.sub(tmp)


        return Ray(start_pos=intersect_pos, direction=r)


    #Formula reference: https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel
    @staticmethod
    def calculate_refract_ray(coming_ray_dir, surface_normal, object_ior, intersect_pos):
        i = coming_ray_dir
        n = surface_normal

        cosi = max(-1, min(1, i.dot_product(n)))
        ior_rate = 1/ object_ior

        if cosi < 0:
            cosi = -cosi
        else:
            ior_rate = 1/ior_rate
            n = n*(-1)

        k =1 - (ior_rate**2) * (1- (cosi**2))

        t = 0 if k < 0 else (i*ior_rate).add(n*((ior_rate*cosi) - k**(1/2)))

        return Ray(start_pos = intersect_pos, direction=t)

    #Formula reference: https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-shading/reflection-refraction-fresnel
    @staticmethod
    def calculate_frasnel(coming_ray_dir, surface_normal, object_ior):
        i = coming_ray_dir
        n = surface_normal
        etai =1
        etat = object_ior

        cosi = max(-1, min(1, i.dot_product(n)))
        #ior_rate = 1/ object_ior

        if cosi > 0:
            etai = object_ior
            etat = 1


        sint = (etai/etat) * (max(0, 1 - (cosi**2)))**(1/2)

        if sint >= 1:
            k = 1
        else:
            cost = (max(0, 1 - (sint**2)))**(1/2)
            cosi = abs(cosi)
            Rs = ((etat*cosi) -(etai *cost)) / ((etat*cosi) +(etai *cost))
            Rp = ((etai*cosi) -(etat *cost)) / ((etai*cosi) +(etat *cost))
            k = ((Rs*Rp) + (Rp*Rp))/2

        return k








'''


Vec3f refract(const Vec3f &I, const Vec3f &N, const float &ior)
{
    float cosi = clamp(-1, 1, dotProduct(I, N));
    float etai = 1, etat = ior;
    Vec3f n = N;
    if (cosi < 0) { cosi = -cosi; } else { std::swap(etai, etat); n= -N; }
    float eta = etai / etat;
    float k = 1 - eta * eta * (1 - cosi * cosi);
    return k < 0 ? 0 : eta * I + (eta * cosi - sqrtf(k)) * n;
}

'''