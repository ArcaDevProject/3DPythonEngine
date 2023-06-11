from ThreeDPythonEngine import Game
from ThreeDPythonEngine import Scene, Entity, Render
from ThreeDPythonEngine.GameUtils import make_mesh, make_sprite, sprite_frames_by_grid, make_colision_mesh
from ThreeDPythonEngine.GameClasses._EntityComponent import Renderable, SpriteAnimator, ColiderComponent as Colider
from PIL import Image


class myscene(Scene):

    def __init__(self):
        super().__init__()
        self.a = 0

    def input(self, inputs, time):
        for key, scancode, action, mods in inputs:
            if (key in set([262, 263, 264, 265])):
                # print(key, scancode, action, mods)
                if (key == 262):
                    # print('right')
                    # print(dir(self))
                    # self._GameScene.player.addposition([1,0,0])
                    """self._GameScene__entities[0].components[0]._vertices[0] += 0.1
                    self._GameScene__entities[0].components[0]._vertices[6] += 0.1
                    self._GameScene__entities[0].components[0]._vertices[12] += 0.1"""
                    self.camera_entity.move_position((0.1, 0, 0))
                    # print(self._GameScene__entities[0].components[0]._vertices)
                if (key == 263):
                    # print('left')
                    """self._GameScene__entities[0].components[0]._vertices[0] -= 0.1
                    self._GameScene__entities[0].components[0]._vertices[6] -= 0.1
                    self._GameScene__entities[0].components[0]._vertices[12] -= 0.1"""
                    self.camera_entity.move_position((-0.1, 0, 0))
                if (key == 264):
                    # print('down')
                    """self._GameScene__entities[0].components[0]._vertices[1] -= 0.1
                    self._GameScene__entities[0].components[0]._vertices[7] -= 0.1
                    self._GameScene__entities[0].components[0]._vertices[13] -= 0.1"""
                    self.camera_entity.move_position((0, -0.1, 0))
                if (key == 265):
                    # print('up')
                    """self._GameScene__entities[0].components[0]._vertices[1] += 0.1
                    self._GameScene__entities[0].components[0]._vertices[7] += 0.1
                    self._GameScene__entities[0].components[0]._vertices[13] += 0.1"""
                    self.camera_entity.move_position((0, 0.1, 0))
            if key == 32 and action == 1:
                self.a = (self.a + 1) % len(self.player.components['SpriteAnimator'].states)
                self.player.components['SpriteAnimator'].set_active_state(self.a)

                # print(posi glo, posi cam)


custom_scene = scene = myscene()

# print(make_mesh(((0, 0, 0), (0, 0, 1)), ((0, 0, 0), (0, 0, 1)), ((0, 0), (1, 1)), (1, 2)))
"""im = Image.open(r"./textures/Tumora.png")
im = Image.open(r"./textures/pngwing.com.png")
im = Image.open(r"./textures/pngwing2.png")
im = Image.open(r"./textures/Tumora2.png")"""
im = Image.open(r"./textures/pngwing.com.png")
im = (im.convert("RGBA").tobytes(),) + im.size
obj = Entity()
obj2 = Entity()
cam = Entity()
renderable = Renderable()
renderable = SpriteAnimator()
renderable2 = Renderable()
obj.add_component(renderable)
obj2.add_component(renderable2)
"""obj.components['MeshComponent'].vertices = np.array([
                    -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0,
                     0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                     -0.5,  0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                     0.5,  0.5, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0
                                                     ], dtype=np.float32)"""
"""v, i = make_mesh(points=((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (-0.5,  0.5, 0.0), (0.5,  0.5, 0.0)),
                 normals=((0.0, 0.0, 1.0),(0.0, 0.0, 1.0),(0.0, 0.0, 1.0),(0.0, 0.0, 1.0)),
                 uvs=((0.0, 0.0),(0.0, 0.0),(0.0, 0.0),(0.0, 0.0)),
                 faces=((0, 1, 2), (1, 2, 3)))"""
v, i = make_sprite(points=((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)))
obj.components['MeshComponent'].vertices = v
obj.components['MeshComponent'].indices = i
"""obj.components['MeshComponent'].indices = np.array([
                    0, 1, 2,
                    1, 2, 3], dtype=np.uint32)"""
v, i = make_sprite()
obj2.components['MeshComponent'].vertices = v
obj2.components['MeshComponent'].indices = i
obj.components['TextureComponent'].texture = im
im2 = Image.open(r"./textures/Tumora2.png")
obj2.components['TextureComponent'].texture = (im2.convert("RGBA").tobytes(),) + (im2.size)
# print(v,i)
g = Game(scene=custom_scene)
# custom_scene.add_entity(obj)
custom_scene.spawn_entity(obj, (0, 0, -0.5), 'player')
custom_scene.spawn_entity(obj2, (1.1, 0, -1), 'player2')
custom_scene.spawn_entity(cam, (0, 0, 2), 'camera')
custom_scene.set_camera(cam)
custom_scene.player = obj
# print(obj.components['MeshComponent'].vertices)
renderable.set_frames(sprite_frames_by_grid((6, 4)))
# print(sprite_frames_by_grid((6, 4))[0])
renderable.set_states(((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4),
                       (6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
                        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                        8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                        10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10),
                       (12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                        13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
                        14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
                        15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                        16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,
                        17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17),
                       (18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                        19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
                        20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                        21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
                        22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22)))
""" renderable.begin()
#print(obj.components['MeshComponent'].vertices)
g.run()
print(make_colision_mesh(((-0.5, -0.4, 0.0), (0.5, -0.4, 0.0), (-0.5,  0.6, 0.0), (0.5,  0.6, 0.0)),
                         ((0, 1, 2), (1, 2, 3))))
                         """
pass
"""c1 = Colider()
c2 = Colider()
c1.dump_data(make_colision_mesh(((1, 2, 0.5), (1.5, -0.5, 2), (0.5, -2, 2.5)), ((0, 1, 2),)))
c2.dump_data(make_colision_mesh(((2, 1, 1.5), (0.5, 0.5, 2), (1.5, -1, 0)), ((0, 1, 2),)))
print(c1.get_colision(c2.data))"""
renderable.begin()
#print(obj.components['MeshComponent'].vertices)
g.run()