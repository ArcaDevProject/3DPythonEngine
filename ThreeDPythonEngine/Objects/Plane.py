import numpy as np
from ThreeDPythonEngine.Objects.utils import Vector3D, normalize, perpendicular

class Plane(object):

    __slots__ = ('__p', '__n')

    def __init__(self, a, b, c):
        self.__p, v1, v2 = Vector3D(a), Vector3D(b) - Vector3D(a), Vector3D(c) - Vector3D(a)
        self.__n = normalize(perpendicular(v1, v2))
        pass

    def impact(self, ray):
        l0, l, _t = ray
        denom = np.dot(self.__n, l)
        t = np.dot(self.__p - l0, self.__n) / denom if denom else 1
        return 0.0001 < abs(denom) and 0 < t if not _t else 0 <= t <= _t, t, l0 + t * l, self.__n

    @property
    def data(self):
        return self.__p, self.__n

    @property
    def P(self):
        return self.__p

    @property
    def N(self):
        return self.__n

    def __repr__(self):
        return f'plane with origin {str(self.P)} and normal {str(self.N)}'