import numpy as np

class Colision(object):

    __slots__ = ('__n', '__p0','__l0','__l', '__t', '__contact_function')

    def __init__(self, plane, ray):
        self.__p0, self.__n = plane
        self.__l0, self.__l, self.__t = ray
        self.__contact_function = self.__contact
        if(self.__t):
            self.__contact_function = self.__contact_limited
        pass

    def __contact_limited(self):
        denom = np.dot(self.__n, self.__l)
        if(0.0001 < abs(denom)):
            t = np.dot(self.__p0 - self.__l0, self.__n) / denom
            return 0 <= t and t <= self.__t
        return False

    def __contact(self):
        denom = np.dot(self.__n, self.__l)
        if(0.0001 < abs(denom)):
            return 0 <= np.dot(self.__p0 - self.__l0, self.__n) / denom
        return False

    @property
    def impact(self):
        t = np.dot(self.__p0 - self.__l0, self.__n) / np.dot(self.__n, self.__l)
        return self.hasContact, t, self.__l0 + t * self.__l, self.__n
        return None, None

    @property
    def hasContact(self):
        return self.__contact_function()
    """
    bool intersectPlane(const Vec3f &n, const Vec3f &p0, const Vec3f &l0, const Vec3f &l, float &t)
    {
        // assuming vectors are all normalized
        float denom = dotProduct(n, l);
        if (denom > 1e-6) {
            Vec3f p0l0 = p0 - l0;
            t = dotProduct(p0l0, n) / denom; 
            return (t >= 0);
        }
    
        return false;
    }
    """