from ThreeDPythonEngine import Game, Scene, Entity
from ThreeDPythonEngine.GameUtils import make_sprite, sprite_frames_by_grid, load_texture
from ThreeDPythonEngine.GameClasses._EntityComponent import EntityComponent, Renderable, SpriteAnimator, ColiderComponent as Colider
from ThreeDPythonEngine.Objects.utils import Vector3D, normalize
from ThreeDPythonEngine.Objects.DOP import *
from PIL import Image
import os, sounddevice as sd, soundfile as sf

f = r'Discord-Ping-Sound-Effect.wav'
data, fs = None, None
if(os.path.exists(f)):

    # convert mp3 to wav file
    #subprocess.call(['ffmpeg', '-i', f,
    #                 'converted_to_wav_file.wav'])

    data, fs = sf.read(f)
    #print(data, 'A')
# print(v,i)
class PongGameScene(Scene):

    def __init__(self):
        super().__init__()
        self.a = 0
        self.speed = 20

    def input(self, inputs, time):
        movement_vector = Vector3D((0, 0, 0))
        for key, scancode, action, mods in inputs:
            if key == 87:
                self.p1.move_position(Vector3D((0, 0.1, 0)) * time * self.speed)
            if key == 83:
                self.p1.move_position(Vector3D((0, -0.1, 0)) * time * self.speed)
            if key == 264:
                self.p2.move_position(Vector3D((0, -0.1, 0)) * time * self.speed)
            if key == 265:
                self.p2.move_position(Vector3D((0, 0.1, 0)) * time * self.speed)
        #print(inputs)
        #self.camera_entity.move_position(movement_vector)
s = PongGameScene()
g = Game(scene=s)
"""
Create Object 1
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-1.2, -0.72, 0), (1.2, -0.72, 0), (1.2, -0.71, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((-1.2, -0.72, 0), (1.2, -0.72, 0), (-1.2, -0.71, 0), (1.2, -0.71, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (0, 0, 0), 'BOTborder')
""""""
"""
Create Object 2
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-1.2, 0.71, 0), (1.2, 0.71, 0), (1.2, 0.72, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((-1.2, 0.71, 0), (1.2, 0.71, 0), (-1.2, 0.72, 0), (1.2, 0.72, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
obj.components['MeshComponent'].set_model(make_sprite(points=((-1.2, 0.71, 0), (1.2, 0.71, 0), (-1.2, 0.72, 0), (1.2, 0.72, 0))))
obj.components['TextureComponent'].texture = load_texture(r"./textures/white.png")
s.spawn_entity(obj, (0, 0, 0), 'TOPborder')
""""""
"""
Create Object 3
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((1.19, -0.71, 0), (1.2, -0.71, 0), (1.2, 0.72, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((1.19, -0.71, 0), (1.2, -0.71, 0), (1.19, 0.72, 0), (1.2, 0.72, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (-1.19*2, 0, 0), 'leftborder')
#c.dump_data(create_data_quad2D((-1.19, -0.71, 0), (-1.2, -0.71, 0), (-1.2, 0.72, 0)), impact_quad2D, translocate_quad2D)
""""""
"""
Create Object 4
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((1.19, -0.71, 0), (1.2, -0.71, 0), (1.2, 0.72, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((1.19, -0.71, 0), (1.2, -0.71, 0), (1.19, 0.72, 0), (1.2, 0.72, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (0, 0, 0), 'Rigborder')
""""""
"""
Create Object 9
"""
im = Image.open(r"./textures/zeroanueve.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = SpriteAnimator()
obj.add_component(renderable)
renderable.set_frames(sprite_frames_by_grid((10, 1)))
renderable.set_states(((0, ),(1, ),(2, ),(3, ),(4, ),(5, ),(6, ),(7, ),(8, ),(9, ),))
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((0, 0, 0), (0.4, 0, 0), (0, 0.4, 0), (0.4, 0.4, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
renderable.begin()
s.spawn_entity(obj, (-0.9, 0.5, -2), 'puntos1')
puntos1 = obj
"""
Create Object 10
"""
im = Image.open(r"./textures/zeroanueve.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = SpriteAnimator()
obj.add_component(renderable)
renderable.set_frames(sprite_frames_by_grid((10, 1)))
renderable.set_states(((0, ),(1, ),(2, ),(3, ),(4, ),(5, ),(6, ),(7, ),(8, ),(9, ),))
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((0, 0, 0), (0.4, 0, 0), (0, 0.4, 0), (0.4, 0.4, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
renderable.begin()
s.spawn_entity(obj, (0.5, 0.5, -2), 'puntos2')
puntos2 = obj
""""""
"""
Create Object 5
"""
sc = Entity()
class SCComponent(EntityComponent):

    def __init__(self):
        self.p1 = 0
        self.p2 = 0

    def score(self, position):
        sd.play(data, fs)
        if 0 < position[0]:
            self.p1 += 1
            self.pv1.set_active_state(self.p1%10)
        else:
            self.p2 += 1
            self.pv2.set_active_state(self.p2%10)
        print(f"Player 1: {self.p1}, Player 2: {self.p2}")
sc.add_component(SCComponent())
sc.components['SCComponent'].pv1 = puntos1.components['SpriteAnimator']
sc.components['SCComponent'].pv2 = puntos2.components['SpriteAnimator']
s.spawn_entity(sc, (0, 0, 0), 'ScoreCounter')
""""""
"""
Create Object 6
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((-0.05, -0.05, 0), (0.05, -0.05, 0), (-0.05, 0.05, 0), (0.05, 0.05, 0)))
class ballComponent(EntityComponent):

    def __init__(self):
        self.movement = np.array((0.01, 0, 0), dtype = np.float32)

    def update(self, entity):
        if entity.impacts:
            si, distance, point, normal, other = entity.impacts[0]
            if other.name in ('Rigborder', 'leftborder'):
                entity.score(entity.position)
                entity.set_position(Vector3D((0, 0, 0)))
                self.movement = -self.movement
            else:
                vp = Vector3D((0, 0, 0))
                for s, t, p, n, o in entity.impacts:
                    vp += p
                s = -normalize(vp/len(entity.impacts)-entity.position)*0.01
                if abs(s[1]) > 0.009:
                    s[0] = self.movement[0]
                self.movement = s
        entity.move_position(self.movement)
        pass
obj.add_component(ballComponent())
c = Colider()
c.dump_data(create_data_quad2D((-0.05, -0.05, 0), (0.05, -0.05, 0), (0.05, 0.05, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
obj.score = sc.components['SCComponent'].score
s.spawn_entity(obj, (0, 0, 0), 'ball')
""""""
"""
Create Object 7
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-0.02, -0.07, 0), (0.02, -0.07, 0), (0.02, 0.07, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((-0.02, -0.07, 0), (0.02, -0.07, 0), (-0.02, 0.07, 0), (0.02, 0.07, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (1.1, 0, 0), 'RPlayer')
s.p2 = obj
""""""
"""
Create Object 8
"""
im = Image.open(r"./textures/white.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
renderable = Renderable()
obj.add_component(renderable)
c = Colider()
c.dump_data(create_data_quad2D((-0.02, -0.07, 0), (0.02, -0.07, 0), (0.02, 0.07, 0)), impact_quad2D, translocate_quad2D)
obj.add_component(c)
#((0, 0, 0), (1.26, 0, 0), (0, 0.728, 0), (1.26, 0.728, 0))
v, i = make_sprite(points=((-0.02, -0.07, 0), (0.02, -0.07, 0), (-0.02, 0.07, 0), (0.02, 0.07, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
s.spawn_entity(obj, (-1.1, 0, 0), 'LPlayer')
s.p1 = obj
""""""
cam = Entity()
s.spawn_entity(cam, (0, 0, 2), 'camera')
s.set_camera(cam)
s.player = obj
g.run()
