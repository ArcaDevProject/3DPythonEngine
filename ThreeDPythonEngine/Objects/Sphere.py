from ThreeDPythonEngine.Objects.utils import *

class Sphere(object):

    __slots__ = ('__center', '__radius', '__rad2')

    def __init__(self, center, radius):
        self.__center, self.__radius, self.__rad2 = Vector3D(center), radius, (radius + 0.000001)*(radius + 0.000001)

    def impact(self, ray):
        l0, l, _t = ray
        #// geometric solution
        L = self.center - l0
        tca = np.dot(L, l)
        if (tca < 0):
            return False, None, None, None
        d2 = np.dot(L, L) - tca * tca
        if (d2 > self.__rad2):
            return False, None, None, None
        thc = np.sqrt(self.__rad2 - d2)
        t = min(tca - thc, tca + thc)
        phit = l0 + t * l

        return 0 < t <= _t if _t else 0 < t, t, phit, normalize(phit-self.center)


    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius