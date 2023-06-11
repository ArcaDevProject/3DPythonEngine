import numpy as np
import pyrr

default_vertex_src = """
# version 330

layout (location=0) in vec3 a_position;
layout (location=1) in vec3 a_normal;
layout (location=1) in vec3 a_color;
layout (location=2) in vec2 a_uv;

uniform mat4 model;
uniform mat4 projection;

out vec3 v_color;
void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
}
"""

default_fragment_src = """
# version 330
in vec3 v_color;
out vec4 out_color;
void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

class EntityComponent(object):
    """
    Base component class
    """

    def update(self, entity):
        """
        :param entity: Owner of self component
        :return: None
        """
        pass

    @property
    def name(self):
        """
        :return: name
        """
        return self.__class__.__name__

    @property
    def call_on_update(self):
        """
        :return: component has to be called on update? False by default
        """
        return False

    @property
    def call_on_render(self):
        """
        :return: component has to be called on render? False by default
        """
        return False

    @property
    def isColider(self):
        """
        :return: component has to be called on colisions? False by default
        """
        return False

class MeshComponent(EntityComponent):
    """
    Contains mesh data
    """

    __slots__ = ('vertices', 'indices')

    def set_model(self, vi):
        """
        :param vi: tuple of vertices and face indices
        :return: None
        """
        v, i = vi
        self.vertices = v
        self.indices = i

class TextureComponent(EntityComponent):
    """
    Contains texture data
    """

    __slots__ = ('texture',)

    def __init__(self):
        self.texture = None


class ShaderComponent(EntityComponent):
    """
    Contains shader program
    """

    __slots__ = ('program', )

    def __init__(self):
        self.program = None

class Renderable(EntityComponent):
    """
    Manages renderable related components
    """

    __slots__ = ('mesh_component', 'shader_component', 'texture_component')

    def __init__(self):
        self.mesh_component = MeshComponent()
        self.shader_component=ShaderComponent()
        self.texture_component=TextureComponent()

    @property
    def mesh(self):
        """
        :return: mesh vertices and mesh indices
        """
        return self.mesh_component.vertices, self.mesh_component.indices

    @property
    def shader(self):
        """
        :return: shader program and texture
        """
        return self.shader_component.program, self.texture_component.texture

    @property
    def call_on_render(self):
        return True

class SpriteAnimator(Renderable):
    """
    Renderable able to change uv coordinates over time
    """

    __slots__ = ('__frames', '__states', '__active_state', '__active_frame')

    def __init__(self):
        super().__init__()
        self.__active_frame, self.__active_state = -1, 0

    def set_frames(self, frames):
        """
        :param frames: Arraylike containing uv coordinates for sprites
        :return: None
        """
        self.__frames = np.array([np.array(uv, dtype=np.float32) for uv in frames])

    def set_states(self, states):
        """
        :param states: Arraylike containing Arraylike sequence of frames per state
        :return: None
        """
        self.__states = [np.array(i) for i in states]
        pass

    def set_active_state(self, index):
        """
        :param index: index of the state
        :return:
        """
        self.__active_state = index

    @property
    def states(self):
        return self.__states

    @property
    def mesh(self):
        self.__active_frame = (self.__active_frame+1)%len(self.__states[self.__active_state])
        """print(self.__states[self.__active_state][self.__active_frame], len(self.__states[self.__active_state]))
        print(self.mesh_component.vertices, len(self.mesh_component.vertices))
        print(self.mesh_component.vertices+self.__states[self.__active_state][self.__active_frame])"""
        """
        self.mesh_component.vertices
        self.__frames[self.__states[self.__active_state][self.__active_frame]]
        """
        return self.mesh_component.vertices+self.__frames[self.__states[self.__active_state][self.__active_frame]], self.mesh_component.indices

    def begin(self):
        """
        :return:
        """
        for v in range(len(self.mesh_component.vertices)//11):
            self.mesh_component.vertices[v*11+9], self.mesh_component.vertices[v*11+10] = 0, 0
            pass


class EntityComponentRenderable(EntityComponent):
    """
    Deprecated renderable component
    """

    def __init__(self, vertices=list(), texture=None):
        self._vertices = vertices
        self.__texture = texture
        pass

    @property
    def vertices(self):
        return self._vertices

    @property
    def texture(self):
        return self.__texture

class ColiderComponent(EntityComponent):
    """
    Manages any colision related event
    """

    __slots__ = ('__data', '__rays', '__impact_method','__datap')

    @property
    def data(self):
        return self.__data

    @property
    def rays(self):
        return self.__rays

    @property
    def isColider(self):
        return True

    @property
    def method(self):
        return self.__impact_method

    def dump_data(self, data, impact, datap):
        """
        :param data: ray data
        :param impact: impact method
        :param datap: mesh data
        :return:
        """
        self.__impact_method, self.__datap = impact, datap
        self.__data, self.__rays = data

    def translocated_data(self, pivot):
        """
        :param pivot: point of reference
        :return: data with new point of reference
        """
        t = pyrr.matrix44.create_from_translation(
            vec=np.array(pivot), dtype=np.float32
        )
        return [(pyrr.matrix44.apply_to_vector(t, v) if isPoint else v) for v, isPoint in zip(self.data, self.__datap)]

    def translocated_rays(self, pivot):
        """
        :param pivot: point of reference
        :return: ray with new point of reference
        """
        t = pyrr.matrix44.create_from_translation(
            vec=np.array(pivot), dtype=np.float32
        )
        return [(pyrr.matrix44.apply_to_vector(t, p), v, l) for p, v, l in self.__rays]

    def impact(self, ray, pivot = np.array((0, 0, 0), dtype=np.float32)):
        """
        :param ray: ray
        :param pivot: pivot
        :return: ray colides with mesh?
        """
        return self.__impact_method(self.translocated_data(pivot), ray)
