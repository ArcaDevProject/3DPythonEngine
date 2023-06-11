from ThreeDPythonEngine.Objects.utils import *

class Box(object):

    __slots__ = ('__bmin', '__bmax', '__bounds')

    def __init__(self, bmin, bmax):
        self.__bmin, self.__bmax = Vector3D(bmin), Vector3D(bmax)
        self.__bounds = self.__bmin, self.__bmax

    @property
    def bounds(self):
        return self.__bounds

    def impact(self, ray):
        l0, l, _t = ray