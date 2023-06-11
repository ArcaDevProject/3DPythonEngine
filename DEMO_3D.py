import pyrr

from ThreeDPythonEngine.Objects.DOP import create_data_ray, create_data_quad2D, impact_quad2D
import numpy as np
from ThreeDPythonEngine import Game
from ThreeDPythonEngine import Scene, Entity, Render
from ThreeDPythonEngine.GameUtils import make_mesh, make_sprite, sprite_frames_by_grid, make_colision_mesh
from ThreeDPythonEngine.GameClasses._EntityComponent import EntityComponent, Renderable, SpriteAnimator, ColiderComponent as Colider
from ThreeDPythonEngine.Objects.utils import Vector3D, normalize
from ThreeDPythonEngine.Objects.DOP import *
from PIL import Image

"""
q1, r1 = create_data_quad2D((-1, -1, 0), (0, -1, 0), (0, 0, 0))
q2, r2 = create_data_quad2D((-0.5, -0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0))

for r in r2:
    print(impact_quad2D(q1, r))
"""
import os, time

import sounddevice as sd
import soundfile as sf

f = r'Discord-Ping-Sound-Effect.wav'
data, fs = None, None
if(os.path.exists(f)):

    # convert mp3 to wav file
    #subprocess.call(['ffmpeg', '-i', f,
    #                 'converted_to_wav_file.wav'])

    data, fs = sf.read(f)
    #print(data, 'A')
# print(v,i)
class My3D(Scene):

    def __init__(self):
        super().__init__()
        self.speed = 10
        self.mouse_pos = None
        self.rot_speed = 0.01

    def input(self, inputs, time):
        movement_vector = Vector3D((0, 0, 0))
        for key, scancode, action, mods in inputs:
            if key == 83:
                v = pyrr.matrix44.multiply(self.camera_entity.rotation_from_eulers,Vector3D((0, 0, 1, 0)))
                self.camera_entity.move_position(Vector3D(v[:3]) * time * self.speed)
            if key == 87:
                v = pyrr.matrix44.multiply(self.camera_entity.rotation_from_eulers,Vector3D((0, 0, -1, 0)))
                self.camera_entity.move_position(Vector3D(v[:3]) * time * self.speed)
            if key == 68:
                v = pyrr.matrix44.multiply(self.camera_entity.rotation_from_eulers,Vector3D((1, 0, 0, 0)))
                self.camera_entity.move_position(Vector3D(v[:3]) * time * self.speed)
            if key == 65:
                v = pyrr.matrix44.multiply(self.camera_entity.rotation_from_eulers,Vector3D((-1, 0, 0, 0)))
                self.camera_entity.move_position(Vector3D(v[:3]) * time * self.speed)

    pass

    def mouse_update(self, inputs, time):
        self.mouse_pos = Vector3D((-inputs[1], 0, -inputs[0]))
        self.mouse_update = self.mouse_update2
        #print(inputs)
        #self.camera_entity.move_position(movement_vector)

    def mouse_update2(self, inputs, time):
        self.camera_entity.add_eulers(Vector3D(((-inputs[1], 0, -inputs[0]))- self.mouse_pos)* self.rot_speed)
        self.mouse_pos = Vector3D((-inputs[1], 0, -inputs[0]))
s = My3D()
g = Game(scene=s)
"""
Create Object 1
"""
im = Image.open(r"./textures/Tumora.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-1.2, -0.72, 0), (1.2, -0.72, 0), (1.2, -0.71, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
from ThreeDPythonEngine.GameUtils import load_mesh
"""v, i = make_sprite(points=((-1.2, -0.72, 0), (1.2, -0.72, 0), (-1.2, 0, 0), (1.2, 0, 0)))
v, i = load_mesh(r'./models/opointonebox.obj')
v, i = make_sprite(points=((0.1, 0.1, 0), (0.1, -0.1, 0), (-0.1, -0.1, 0), (-0.1, 0.1, 0)))"""
v, i = load_mesh(r'./models/opointonebox3.obj')
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (0.3, 0, 0), 'BOTborder')
""""""
"""
Create Object 1
"""
im = Image.open(r"./textures/Tumora.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-1.2, -0.72, 0), (1.2, -0.72, 0), (1.2, -0.71, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
"""v, i = make_sprite(points=((-1.2, -0.72, 0), (1.2, -0.72, 0), (-1.2, 0, 0), (1.2, 0, 0)))
v, i = load_mesh(r'./models/opointonebox.obj')
v, i = make_sprite(points=((0.1, 0.1, 0), (0.1, -0.1, 0), (-0.1, -0.1, 0), (-0.1, 0.1, 0)))"""
v, i = load_mesh(r'./models/square.obj')
"""
"""
v, i = make_sprite(points=((-0.1, -0.1, -0.1), (0.1, -0.1, -0.1), (-0.1, 0.1, -0.1), (0.1, 0.1, -0.1)))
for e in range(len(v[:33])//11):
    print(v[11*e:11*(e+1)])
i= np.array((0, 1, 2))
print(i)
i= np.array((0, 1, 2))
#x = 10*v-10*b
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (-0.3, 0, 0), 'BOTborder2')
""""""
cam = Entity()
s.spawn_entity(cam, (0, 0, 2), 'camera')
s.set_camera(cam)
s.player = obj
g.run()