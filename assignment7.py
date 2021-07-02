# CENG 488 Assignment7 by
# Elman Hamdi
# 240201036
# June 2021

from cameras import *
from utils import *
from objects import *
from scenes import *
from views import *
from lights import *
import json

# json_file = open("file.json")

# Okuma isini baska classta yap . data class ile yap. pydantic: bi incele isine yarar belki
# Otomayik olarak file okur loadlar ve kapatir
with open("file.json") as f:
    render_file = json.load(f)

# render_file = json.loads(json_file.read())

render_settings = render_file['renderSettings']
WIDTH = render_settings['xres']
HEIGHT = render_settings['yres']

# init scene
scene = Scene()
window = Window(HEIGHT, WIDTH)
camera = Camera(
    eye=Pos3d.list_to_pos(render_file['camera']['position']),
    center=Pos3d(0, 0, 0),
    window=window,
    window_distance=render_file['camera']['window_distance'],
)

for raw_sphere in render_file['sphere']:
    sphere = Sphere(
        radius=raw_sphere['radius'],
        center=Pos3d.list_to_pos(raw_sphere['position']),
        material=Material(
            color=Color(
                raw_sphere['color'][0],
                raw_sphere['color'][1],
                raw_sphere['color'][2],
            ),
            refractive=raw_sphere['refractive'],
            reflective=raw_sphere['reflective'],
        ),
    )
    scene.add(sphere)

lights = [Light(
        position=Pos3d.list_to_pos(light['position']),
        color=Color(
            light['color'][0],
            light['color'][1],
            light['color'][2],
        ),
        intensity=light['intensity'],
    ) for light in render_file['light']
 ]
 
for raw_light in render_file['light']:
    light = Light(
        position=Pos3d.list_to_pos(raw_light['position']),
        color=Color(
            raw_light['color'][0],
            raw_light['color'][1],
            raw_light['color'][2],
        ),
        intensity=raw_light['intensity'],
    )
    scene.add(light)

view = View(camera=camera, scene=scene)


def main():
    # THREADED VERSION
    view.calculate_whitted_ray_tracing_with_thread(nof_thread=5, nof_divide=100)

    # UNTHREADED VERSION
    # view.draw_whitted_rt()


if __name__ == '__main__':
    main()
