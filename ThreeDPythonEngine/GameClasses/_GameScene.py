import numpy as np


class GameScene(object):
    """
    The scene active to display and interact
    """

    def __init__(self):
        self.__entities = []
        self.__renderables = []
        self.__colidables = []

    def update(self, inputs, time):
        """
        Method to display every frame
        :param inputs: inputs elements
        :param time: time elapsed between frames
        :return:
        """
        #print(1/time)
        self.input(inputs, time)
        for e in self.__entities:
            e.update()

    def mouse_update(self, inputs, time):
        #print(1/time)
        pass

    def detect_colisions(self):
        """
        Detect every impact in scene
        :return:
        """
        colidables = [(e, e.colider.translocated_data(e.position),
                       e.colider.translocated_rays(e.position), e.colider.method)for e in self.__colidables]
        """for e, data, rays in colidables:
            impacts = []
            for o, odata, orays in colidables:
                if e != o:
                    for r in rays:
                        impacted, d, p, n = o.colider.impact(r)
                        #print(impacted, d, p, n)
                        if impacted:
                            impacts.append((impacted, d, p, n, o))"""
        """for e, data, rays, impact in colidables:
            impacts = []
            for o, odata, orays, om in colidables:
                if e != o:
                    for r in orays:
                        #p, d, t = r
                        #print(impacted, d, p, n)
                        #impacted, d, p, n = e.colider.impact(r, e.position)
                        impacted, d, p, n = impact(data, r)
                        if impacted:
                            impacts.append((impacted, d, p, n, o))"""
        for e, data, rays, impact in colidables:
            impacts = []
            for o, odata, orays, om in colidables:
                if e != o:
                    for r in rays:
                        # p, d, t = r
                        # print(impacted, d, p, n)
                        # impacted, d, p, n = e.colider.impact(r, e.position)
                        impacted, d, p, n = om(odata, r)
                        if impacted:
                            impacts.append((impacted, d, p, n, o))
            e.set_impacts(impacts)

    def add_entity(self, entity):
        """
        DEPRECATED
        :param entity: new entity for the scene
        :return:
        """
        self.__entities.append(entity)
        if entity.call_on_render:
            self.__renderables.append(entity)
            if entity.components['ShaderComponent'].program is None:
                entity.components['ShaderComponent'].program = self.GPU.default_shader

    def spawn_entity(self, entity, position=list((0,0,0)),name=None):
        """
        Spawns an entity on a designed position of the scene
        :param entity: new entity
        :param position: position
        :param name: name of the new entity
        :return:
        """
        self.__entities.append(entity)
        entity.set_name(name)
        entity.set_position(np.array(position, dtype=np.float32))
        if entity.call_on_render:
            self.__renderables.append(entity)
            if entity.components['ShaderComponent'].program is None:
                entity.components['ShaderComponent'].program = self.GPU.default_shader
        if entity.colider:
            self.__colidables.append(entity)
        pass

    def input(self, inputs, time):


        """if(key in set([262, 263, 264, 265])):
            print(key, scancode, action, mods)
            if(key==262):
                print('right')
            if(key==263):
                print('left')
            if(key==264):
                print('down')
            if(key==265):
                print('up')"""
        pass

    def set_GPU(self, gpu):
        """
        :param gpu: new gpu comunicating object
        :return:
        """
        self.__GPU = gpu

    def toGPU(self, gpuApi):
        """
        Sends the scene data to the gpu object
        :param gpuApi:
        :return:
        """
        gpuApi.v1render(self.vertices)
        pass

    def render(self):
        """
        Renders the scene
        :return:
        """
        self.GPU.set_camera_transforms(self.__camera_entity.position, self.__camera_entity.rotation_from_eulers)
        for renderable in self.__renderables:
            self.__GPU.render(renderable.render)

    def set_camera(self, entity):
        """
        :param entity: New camera
        :return:
        """
        self.__camera_entity = entity

    @property
    def GPU(self):
        return self.__GPU

    @property
    def camera_entity(self):
        return self.__camera_entity

