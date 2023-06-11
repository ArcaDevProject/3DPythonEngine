from ThreeDPythonEngine.Objects.Plane import Plane
from ThreeDPythonEngine.Objects.utils import *


class Triangle(Plane):

    __slots__ = ('__a', '__b', '__c', '__ab', '__bc', '__ca')

    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        self.__a, self.__b, self.__c = Vector3D(a), Vector3D(b), Vector3D(c)
        self.__ab, self.__bc, self.__ca = self.__b - self.__a, self.__c - self.__b, self.__a - self.__c
        pass

    def impact(self, ray):
        l0, l, _t = ray
        denom = np.dot(self.N, l)
        t = np.dot(self.P - l0, self.N) / denom if denom else 1
        phit = l0 + t * l
        #e0, e1, e2 = self.__b - self.__a, self.__c - self.__b, self.__a - self.__c
        #f0, f1, f2 = phit - self.__a, phit - self.__b, phit - self.__c
        return (0.0001 < abs(denom) and (0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(self.N, np.cross(self.__ab, phit - self.__a)) and
                0 <= np.dot(self.N, np.cross(self.__bc, phit - self.__b)) and
                0 <= np.dot(self.N, np.cross(self.__ca, phit - self.__c))
                , t, phit, self.N)

    @property
    def A(self):
        return self.__a

    @property
    def B(self):
        return self.__b

    @property
    def C(self):
        return self.__c

    @property
    def AB(self):
        return self.__ab

    @property
    def BC(self):
        return self.__bc

    @property
    def CA(self):
        return self.__ca
