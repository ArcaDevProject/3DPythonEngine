import numpy as np
from ThreeDPythonEngine.Objects.utils import Vector3D, normalize

class Ray(object):

    __slots__ = ('__p', '__d', '__t')

    def __init__(self, p, d, t= None):
        self.__p, self.__d, self.__t = Vector3D(p), normalize(Vector3D(d)), t
        pass

    @property
    def data(self):
        return self.__p, self.__d, self.__t

    @property
    def P(self):
        return self.__p

    @property
    def D(self):
        return self.__d

    @property
    def T(self):
        return self.__t

    def __repr__(self):
        if self.__t:
            return f'Ray with origin {str(self.P)}, direction {str(self.D)} and distance {self.T}'
        return f'Ray with origin {str(self.P)} and direction {str(self.D)}'