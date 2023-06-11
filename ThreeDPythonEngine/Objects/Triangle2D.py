import numpy as np

from ThreeDPythonEngine.Objects.Triangle import Triangle
from ThreeDPythonEngine.Objects.utils import *


class Triangle2D(Triangle):

    __slots__ = ('__abN', '__bcN', '__caN')

    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        self.__abN = normalize(perpendicular(Vector3D(a)-Vector3D(b),self.N))
        self.__bcN = normalize(perpendicular(Vector3D(b)-Vector3D(c),self.N))
        self.__caN = normalize(perpendicular(Vector3D(c)-Vector3D(a),self.N))
        pass

    def impact(self, ray):
        l0, l, _t = ray
        denom = np.dot(self.N, l)
        if denom:
            t = np.dot(self.P - l0, self.N) / denom
            phit = l0 + t * l
            #e0, e1, e2 = self.__b - self.__a, self.__c - self.__b, self.__a - self.__c
            #f0, f1, f2 = phit - self.__a, phit - self.__b, phit - self.__c
            return ((0 < t if not _t else 0 <= t <= _t) and
                    0 <= np.dot(self.N, np.cross(self.AB, phit - self.A)) and
                    0 <= np.dot(self.N, np.cross(self.BC, phit - self.B)) and
                    0 <= np.dot(self.N, np.cross(self.CA, phit - self.C))
                    , t, phit, self.N)
        t = np.dot(self.__abN, l)
        phit = l0 + t * l
        if((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(self.N, np.cross(-self.__abN, phit - self.A)) and
                0 <= np.dot(self.N, np.cross(self.__abN, phit - self.B))):
            return True, t, phit, self.__abN
        t = np.dot(self.__bcN, l)
        phit = l0 + t * l
        #print(t)
        if((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(self.N, np.cross(-self.__bcN, phit - self.B)) and
                0 <= np.dot(self.N, np.cross(self.__bcN, phit - self.C))):
            return True, t, phit, self.__bcN
        t = np.dot(self.__caN, l)
        phit = l0 + t * l
        #print(t)
        if((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(self.N, np.cross(-self.__caN, phit - self.C)) and
                0 <= np.dot(self.N, np.cross(self.__caN, phit - self.A))):
            return True, t, phit, self.__caN
        return False, None, None, None