from ThreeDPythonEngine.Objects.Quad import Quad
from ThreeDPythonEngine.Objects.utils import *


class Quad2D(Quad):

    __slots__ = ('__abN', '__bcN', '__cdN', '__daN')

    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        self.__abN = normalize(perpendicular(self.A-self.B,self.N))
        self.__bcN = normalize(perpendicular(self.B-self.C,self.N))
        self.__cdN = normalize(perpendicular(self.C-self.D,self.N))
        self.__daN = normalize(perpendicular(self.D-self.A,self.N))
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
                    0 <= np.dot(self.N, np.cross(self.CD, phit - self.C)) and
                    0 <= np.dot(self.N, np.cross(self.DA, phit - self.D))
                    , t, phit, self.N)
        denom = np.dot(self.__abN, l)
        if 0 < abs(denom):
            t = np.dot(self.A - l0, self.__abN) / denom
            phit = l0 + t * l
            if((0 < t if not _t else 0 <= t <= _t) and
                    0 <= np.dot(self.N, np.cross(-self.__abN, phit - self.A)) and
                    0 <= np.dot(self.N, np.cross(self.__abN, phit - self.B))):
                return True, t, phit, self.__abN
        denom = np.dot(self.__bcN, l)
        if 0 < abs(denom):
            t = np.dot(self.B - l0, self.__bcN) / denom
            phit = l0 + t * l
            if((0 < t if not _t else 0 <= t <= _t) and
                    0 <= np.dot(self.N, np.cross(-self.__bcN, phit - self.B)) and
                    0 <= np.dot(self.N, np.cross(self.__bcN, phit - self.C))):
                return True, t, phit, self.__bcN
        denom = np.dot(self.__cdN, l)
        if 0 < abs(denom):
            t = np.dot(self.C - l0, self.__cdN) / denom
            phit = l0 + t * l
            if((0 < t if not _t else 0 <= t <= _t) and
                    0 <= np.dot(self.N, np.cross(-self.__cdN, phit - self.C)) and
                    0 <= np.dot(self.N, np.cross(self.__cdN, phit - self.D))):
                return True, t, phit, self.__cdN
        denom = np.dot(self.__daN, l)
        if 0 < abs(denom):
            t = np.dot(self.D - l0, self.__daN) / denom
            phit = l0 + t * l
            if((0 < t if not _t else 0 <= t <= _t) and
                    0 <= np.dot(self.N, np.cross(-self.__daN, phit - self.D)) and
                    0 <= np.dot(self.N, np.cross(self.__daN, phit - self.A))):
                return True, t, phit, self.__daN
        return False, None, None, None