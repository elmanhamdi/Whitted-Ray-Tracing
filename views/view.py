# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021


from utils import *
from objects import *
import numpy as np
import sys
from PIL import Image
from multiprocessing import Pool
from functools import partial

NOF_REFRACTION = 5
NOF_REFLECTION = 5


class View:
    def __init__(self, camera, scene=None, bgColor=Color(0, 0, 0, 1)):
        self.camera = camera
        self.scene = scene
        self.bgColor = bgColor

    def draw_a_list(self, pixel_list, open_after_draw=1, file_name='img'):
        img = Image.fromarray(pixel_list, 'RGB')
        img.save(file_name + '.png')
        if open_after_draw:
            img.close()
            Image.open(file_name + '.png').show()

    def draw_whitted_rt(self, open_after_draw=1, file_name='img'):
        pixel_list = self.calculate_whitted_ray_tracing()

        img = Image.fromarray(pixel_list, 'RGB')
        img.save(file_name + '.png')
        if open_after_draw:
            img.close()
            Image.open(file_name + '.png').show()

    def draw_ambient_occlusion(self, sample, open_after_draw=1, file_name='img'):
        pixel_list = self.calculate_ambient_occlusion(sample)

        img = Image.fromarray(pixel_list, 'RGB')
        img.save(file_name + '.png')
        if open_after_draw:
            img.close()
            Image.open(file_name + '.png').show()

    def calculate_ambient_occlusion(self, sample):
        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)

        for y in range(cam_h):
            View.__print_persantage(self, y, cam_h)

            for x in range(cam_w):

                pos_on_window = Pos3d.add(self.camera.eye,
                                          Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance))

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pos_on_window, self.camera.eye))

                ray = Ray(start_pos=pos_on_window, direction=ray_direction)

                closest_node = None
                shortest = -1

                for node in self.scene.nodes:
                    intersect_tmp = node.intersect(ray)
                    if (intersect_tmp != -1):
                        if (intersect_tmp.t0 >= 0):
                            d = Pos3d.cal_distance_value(intersect_tmp.p0, pos_on_window)
                            if (shortest == -1) or (shortest > d):
                                shortest = d
                                closest_node = node
                                intersect = intersect_tmp

                if closest_node != None:
                    nof_intersect = 0
                    point = intersect.p0
                    for r in range(sample):

                        sample_ray = closest_node.generate_random_hemisphere_ray(point)

                        for n in self.scene.nodes:
                            if n != closest_node:
                                int_sample = n.intersect(sample_ray)
                                if (int_sample != -1):
                                    if (int_sample.t0 > 0):
                                        nof_intersect += 1
                                        break

                        new_color = [x * ((sample - nof_intersect) / sample) for x in
                                     closest_node.material.color.getRGB()]
                        pixel_list[y][x] = new_color

        return pixel_list

    def __print_persantage(self, y, cam_h):
        persentage = ((y + 1) / cam_h) * 100

        a = ("%.2f" % persentage)
        # loading = ['/', '-', '\\','|', '/', '-','\\','|',]
        ENDC = '\033[0m'
        WARNING = '\033[93m'
        # sys.stdout.write('\r' +'  %' + a + ' ' + f'{WARNING}loading {ENDC}' + '.'*(y%5))
        sys.stdout.write('\r' + '  %' + a + ' ' + WARNING + 'loading' + ENDC + '.' * (y % 5))

    def __print_persantage_thread(self, thread_order, nof_thread, y, cam_h):
        persentage = (((y + 1) * thread_order) / (cam_h * nof_thread)) * 100

        a = ("%.2f" % persentage)
        # loading = ['/', '-', '\\','|', '/', '-','\\','|',]
        ENDC = '\033[0m'
        WARNING = '\033[93m'
        # sys.stdout.write('\r' +'  %' + a + ' ' + f'{WARNING}loading {ENDC}' + '.'*(y%5))
        sys.stdout.write(
            '\r' + '  %' + a + ' ' + 'Thread :' + str(thread_order) + ' ' + WARNING + 'loading' + ENDC + '.' * (y % 5))

    def __print_thread(self, thread_order, nof_thread, cam_h):

        # loading = ['/', '-', '\\','|', '/', '-','\\','|',]
        ENDC = '\033[0m'
        WARNING = '\033[93m'
        # sys.stdout.write('\r' +'  %' + a + ' ' + f'{WARNING}loading {ENDC}' + '.'*(y%5))
        sys.stdout.write(
            '\r' "Total num of bucket: " + str(nof_thread) + ' -    ' + WARNING + 'Bucket ' + str(
                thread_order) + ' ' + 'started to be processed by a thread' + ENDC)

    def ac_thread(self, num_thread=5, sample=5, thread_order=1):

        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)

        for y in range(int(thread_order * cam_h / (num_thread + 1)),
                       int((thread_order + 1) * cam_h / (num_thread + 1))):
            View.__print_persantage_thread(self, thread_order, num_thread, y, cam_h)
            # View.__print_persantage(self, y, cam_h)
            for x in range(cam_w):

                pos_on_window = Pos3d.add(self.camera.eye,
                                          Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance))

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pos_on_window, self.camera.eye))

                ray = Ray(start_pos=pos_on_window, direction=ray_direction)

                closest_node, intersect = self.__find_closest_obj(ray)

                if closest_node != -1:
                    nof_intersect = 0
                    point = intersect.p0
                    for r in range(sample):
                        sample_ray = closest_node.generate_random_hemisphere_ray(point)

                        for n in self.scene.nodes:
                            if n != closest_node:
                                int_sample = n.intersect(sample_ray)
                                if (int_sample != -1):
                                    if (int_sample.t0 > 0):
                                        nof_intersect += 1
                                        break

                    new_color = [x * ((sample - nof_intersect) / sample) for x in closest_node.material.color.getRGB()]
                    pixel_list[y][x] = new_color

        return pixel_list

    def calculate_ambient_occusion_with_thread(self, nof_thread=5, nof_divide=2, sample=10):

        parameters = []
        for i in range(nof_divide):
            parameters.append(i + 1)
            parameters.append(nof_divide)
            parameters.append(sample)

        func = partial(self.ac_thread, nof_divide, sample)

        with Pool(processes=nof_thread) as pool:
            results = pool.map(func, list(range(1, nof_divide + 1)))

        lst = results[0]
        for i in range(1, len(results)):
            lst = lst + results[i]

        self.draw_a_list(lst)

    def calculate_whitted_ray_tracing_with_thread(self, nof_thread=5, nof_divide=2):

        parameters = []
        for i in range(nof_divide):
            parameters.append(i + 1)
            parameters.append(nof_divide)

        func = partial(self.w_rt_thread, nof_divide)

        with Pool(processes=nof_thread) as pool:
            results = pool.map(func, list(range(1, nof_divide + 1)))

        lst = results[0]
        for i in range(1, len(results)):
            lst = lst + results[i]

        self.draw_a_list(lst)

    def w_rt_thread(self, num_thread=5, thread_order=1):
        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)

        cam_front = Vec3d.positions_to_vec(self.camera.center, self.camera.eye, ).normalize()
        window_right_vec = Vec3d.cross_product(self.camera.up, cam_front).normalize()
        window_up_vec = Vec3d.cross_product(cam_front, window_right_vec, ).normalize()

        for y in range(int(thread_order * cam_h / (num_thread + 1)),
                       int((thread_order + 1) * cam_h / (num_thread + 1))):
            View.__print_thread(self, thread_order, num_thread, cam_h)
            for x in range(cam_w):
                r = window_right_vec
                u = window_up_vec
                # pos_on_window = Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance)
                # print(1, pos_on_window)
                pos_on_window = ((r * (-cam_w / 2 + x)).add(u * (cam_h / 2 - y))).add(
                    cam_front * self.camera.window_distance)  # Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance)
                # print(2, pos_on_window)
                pixel_pos_in_space = Pos3d.add(self.camera.eye, pos_on_window)

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pixel_pos_in_space, self.camera.eye))
                ray = Ray(start_pos=pixel_pos_in_space, direction=ray_direction)

                color = self.calculate_color_whitted(200, ray)

                pixel_list[y][x] = color.getRGB()

        return pixel_list

    def calculate_whitted_ray_tracing(self):
        cam_h = self.camera.window.height
        cam_w = self.camera.window.width
        pixel_list = np.full((cam_h, cam_w, 3), fill_value=self.bgColor.getRGB(), dtype=np.uint8)

        for y in range(cam_h):
            View.__print_persantage(self, y, cam_h)
            for x in range(cam_w):
                pos_on_window = Pos3d(-cam_w / 2 + x, cam_h / 2 - y, self.camera.window_distance)
                pixel_pos_in_space = Pos3d.add(self.camera.eye, pos_on_window)

                ray_direction = HomogeneusCoor.normalize(Vec3d.positions_to_vec(pixel_pos_in_space, self.camera.eye))
                ray = Ray(start_pos=pixel_pos_in_space, direction=ray_direction)

                color = self.calculate_color_whitted(200, ray)

                pixel_list[y][x] = color.getRGB()

        return pixel_list

    def calculate_color_whitted(self, nof_bounce, coming_ray, max_bounce=10, inside_ray=False, ):
        color = Color(0, 0, 0, 0)
        nDotL = 1
        if nof_bounce == 0 or max_bounce == 0:
            return color
        else:

            closest_node, intersect, c2, i2 = self.__find_closest_obj(coming_ray)

            if closest_node != -1:
                point = intersect.p0
                surface_normal = closest_node.normal_of_a_point(point)
                ray_dir = coming_ray.direction
                nDotL = max(surface_normal.normalize().dot_product(
                    Vec3d.positions_to_vec(self.scene.lights[0].position.normalize(), point.normalize())), 0.0)

                if self.__is_that_closest_to_light(closest_node, point, self.scene.lights[0]):

                    frasnel_value = 1 if closest_node.material.refractive == 0 else Ray.calculate_frasnel(
                        ray_dir, surface_normal, object_ior=closest_node.material.ior)
                    reflective_rate = closest_node.material.reflective

                    # REFRACTIVE CALCULATION
                    bias = 1e-4
                    if closest_node.material.refractive != 0:
                        ray = Ray.calculated_bounced_ray(ray_dir, surface_normal, point)
                        reflective_color_value1 = self.calculate_color_whitted(nof_bounce - 1, ray, max_bounce - 1)

                        refract_ray_tmp = Ray.calculate_refract_ray(ray_dir, surface_normal, closest_node.material.ior,
                                                                    point)

                        p1 = closest_node.intersect(refract_ray_tmp).p1
                        tmp_normal = closest_node.normal_of_a_point(p1)

                        refract_ray = Ray.calculate_refract_ray(refract_ray_tmp.direction, tmp_normal * (-1),
                                                                1 / closest_node.material.ior, p1)
                        reflect_ray = Ray.calculated_bounced_ray(refract_ray_tmp.direction, tmp_normal * (-1), p1)

                        # Ray.calculate_refract_ray(refract_ray.direction, tmp_normal, 0.8, p1)

                        refractive_color_value = Color(0, 0, 0, 0)
                        reflective_color_value = Color(0, 0, 0, 0)
                        if inside_ray == True:
                            print()#return Color(0, 0, 0)
                        elif refract_ray.direction != 0:
                            refractive_color_value = self.calculate_color_whitted(nof_bounce - 1, refract_ray,
                                                                                  max_bounce - 1, inside_ray= True)
                            reflective_color_value = self.calculate_color_whitted(nof_bounce - 1, reflect_ray,
                                                                                  max_bounce=max_bounce - 1)

                        else:
                            reflective_color_value = self.calculate_color_whitted(nof_bounce - 1, refract_ray_tmp,
                                                        max_bounce - 1, )

                        color += ((((refractive_color_value) * (1 - frasnel_value) + reflective_color_value * (
                         frasnel_value)) * (1 - reflective_rate) + reflective_color_value1 * (reflective_rate)
                         )) * (1 - frasnel_value)

                    # REFRACTIVE CALCULATION
                    elif reflective_rate != 0:
                        ray = Ray.calculated_bounced_ray(ray_dir, surface_normal, point)
                        reflective_color_value = self.calculate_color_whitted(nof_bounce - 1, ray, max_bounce - 1)

                        color += closest_node.material.color * (reflective_rate) + reflective_color_value * (
                                1 - reflective_rate)

                    else:
                        return closest_node.material.color * (1 - reflective_rate) * nDotL

            return color#*nDotL

    def reflective_bounce(self, nof_refra_bounce, nof_refle_bounce, nof_bounce, coming_ray, surface_normal,
                          intersect_pos):
        return 0

    def __find_closest_obj(self, ray):
        shortest = -1
        intersect = -1
        closest_node = -1

        closest_node_2 = -1
        intersect_2 = -1
        for node in self.scene.nodes:

            intersect_tmp = node.intersect(ray)
            if (intersect_tmp != -1):
                if (intersect_tmp.t0 >= 0):
                    d = Pos3d.cal_distance_value(intersect_tmp.p0, ray.start_pos)
                    if (shortest == -1) or (shortest > d):
                        closest_node_2 = closest_node
                        intersect_2 = intersect
                        shortest = d
                        closest_node = node
                        intersect = intersect_tmp

        return closest_node, intersect, closest_node_2, intersect_2

    def __is_that_closest_to_light(self, object, intersect_point, light):
        ray_from_light = Ray(start_pos=light.position,
                             direction=HomogeneusCoor.normalize(
                                 Vec3d.positions_to_vec(intersect_point, light.position)))
        closest_node_to_light, tmp_i, c2, i2 = self.__find_closest_obj(ray_from_light)
        if object == closest_node_to_light:
            if tmp_i.p0.compare(intersect_point):
                return True
            if closest_node_to_light.material.refractive > 0:
                return True

        elif closest_node_to_light.material.refractive > 0:
            if object == c2:
                if i2.p0.compare(intersect_point):
                    return True
        return False

    def __is_that_closest_to_light_with_check_light(self, object, intersect_point, light):
        ray_from_light = Ray(start_pos=light.position,
                             direction=HomogeneusCoor.normalize(
                                 Vec3d.positions_to_vec(intersect_point, light.position)))
        closest_node_to_light, tmp_i, c2, i2 = self.__find_closest_obj(ray_from_light)
        if object == closest_node_to_light:
            if tmp_i.p0.compare(intersect_point):
                return True, False
            if closest_node_to_light.material.refractive > 0:
                return True, True

        elif closest_node_to_light.material.refractive > 0:
            if object == c2:
                if i2.p0.compare(intersect_point):
                    return True, True
        return False, False
