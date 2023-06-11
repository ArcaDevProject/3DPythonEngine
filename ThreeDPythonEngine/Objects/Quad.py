from ThreeDPythonEngine.Objects.utils import *
from ThreeDPythonEngine.Objects.Plane import Plane

class Quad(Plane):

    __slots__ = ('__a', '__b', '__c', '__d', '__ab', '__bc', '__cd', '__da')

    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        self.__a, self.__b, self.__c, self.__d = (Vector3D(a), Vector3D(b), Vector3D(c),
                                                  Vector3D(c) - Vector3D(b) + Vector3D(a))
        self.__ab, self.__bc, self.__cd, self.__da = (self.__b - self.__a, self.__c - self.__b,
                                                      self.__d - self.__c, self.__a - self.__d)

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
                0 <= np.dot(self.N, np.cross(self.__cd, phit - self.__c)) and
                0 <= np.dot(self.N, np.cross(self.__da, phit - self.__d))
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
    def D(self):
        return self.__d

    @property
    def AB(self):
        return self.__ab

    @property
    def BC(self):
        return self.__bc

    @property
    def CD(self):
        return self.__cd

    @property
    def DA(self):
        return self.__da