import numpy as np
import pyrr

class GameEntity(object):
    """
    Basic game entity, contains Entity components
    """

    def __init__(self, position=list([0, 0, 0]), name=''):
        self.__shader = None
        self.__mesh = None
        self.__position = position
        self.__components = {}
        self.__render = None
        self.__name = name
        self.__colider = None
        self.__impacts = []
        self.__rotation = np.array(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        self.__eulers = np.array((0, 0, 0), dtype=np.float32)

    def set_name(self, name):
        """
        :param name: New name
        :return:
        """
        self.__name = name

    def set_position(self, position):
        """
        :param position: new position
        :return:
        """
        self.__position = position

    def set_rotation(self, rotation):
        """
        :param rotation: new orientation
        :return:
        """
        self.__rotation = rotation

    def set_impacts(self, impacts):
        """
        :param impacts: sets list of impacts
        :return:
        """
        self.__impacts = impacts

    def move_position(self, vector):
        """
        :param vector: vector that moves the entity
        :return:
        """
        self.__position += np.array(vector, dtype=np.float32)

    def update(self):
        """
        method that updates the components
        :return:
        """
        for cmp in self.components.values():
            cmp.update(self)

    def add_component(self, cmp):
        """
        :param cmp: new component
        :return:
        """
        if cmp.name not in self.components:
            self.__components[cmp.name] = cmp
            if cmp.call_on_render:
                self.__render = cmp
                self.__mesh = cmp.mesh_component
                self.__shader = cmp.shader_component
                self.__components['MeshComponent'] = cmp.mesh_component
                self.__components['ShaderComponent']=cmp.shader_component
                self.__components['TextureComponent']=cmp.texture_component
            if cmp.isColider:
                self.__colider = cmp

    def add_eulers(self, o):
        self.__eulers += o

    @property
    def position(self):
        return self.__position

    @property
    def rotation(self):
        return self.__rotation

    @property
    def rotation_from_eulers(self):
        return pyrr.matrix44.create_from_eulers(self.__eulers)

    @property
    def components(self):
        return self.__components

    @property
    def render(self):
        return self.position, self.__render.mesh, self.__render.shader

    @property
    def colider(self):
        return self.__colider

    @property
    def call_on_render(self):
        return self.__render is not None

    @property
    def impacts(self):
        return self.__impacts

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return f"Entity {self.__name} at {self.position}"

class PremadeEntity(object):
    """
    Not implemented
    """

    def __init__(self, components=set(), attr=list()):
        self.__components = components
        self.__attr = attr

    def spawn(self, position):
        entity = GameEntity(position= position)
        for component in self.__components:
            entity.add_component(component())
        for component, attribute, value in self.__attr:
            setattr(entity.components[component], attribute, value)
        return entity