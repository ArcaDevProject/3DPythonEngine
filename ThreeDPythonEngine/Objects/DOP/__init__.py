import numpy as np


def Vector3D(vector):
    return np.array(vector, dtype=np.float32)


def normalize(vector):
    return vector / np.linalg.norm(vector)


def perpendicular(a, b):
    return np.cross(a, b)


vector_length = np.linalg.norm


translocate_quad2D = (False, True, True, True, True, False, False, False, False, False, False, False, False)


def create_data_ray(p, d, t=None):
    """
    :param p: Origin
    :param d: Direction
    :param t: Distance
    :return: Ray as data
    """
    return Vector3D(p), normalize(Vector3D(d)), t


def create_data_plane(a, b, c):
    """
    :param a: point in space
    :param b: point in space
    :param c: point in space
    :return: plain containing a, b and c
    """
    return (Vector3D(c) - Vector3D(a), Vector3D(a), normalize(perpendicular(Vector3D(b) - Vector3D(a)))), ()


def impact_plane(element, ray):
    """
    :param element: plain data
    :param ray: ray data
    :return: impact data (colision, distance, position and normal)
    """
    n, p = element
    l0, l, _t = ray
    denom = np.dot(n, l)
    t = np.dot(p - l0, n) / denom if denom else 1
    if 0.0001 < abs(denom) and 0 < t if not _t else 0 <= t <= _t:
        return True, t, l0 + t * l, n
    return False, None, None, None


def create_data_tri(a, b, c):
    """
    :param a: point in space
    :param b: point in space
    :param c: point in space
    :return: triangle generated by a, b and c
    """
    n, a, b, c = (normalize(perpendicular(Vector3D(b) - Vector3D(a), Vector3D(c) - Vector3D(a))), Vector3D(a),
                  Vector3D(b), Vector3D(c))
    ab, bc, ca = b - a, c - b, a - c
    return (n, a, b, c, ab, bc, ca), (create_data_ray(a, ab, vector_length(ab)),
                                      create_data_ray(b, bc, vector_length(bc)),
                                      create_data_ray(c, ca, vector_length(ca)))


def impact_tri(element, ray):
    """
    :param element: tri data
    :param ray: ray data
    :return: impact data (colision, distance, position and normal)
    """
    n, a, b, c, ab, bc, ca = element
    l0, l, _t = ray
    denom = np.dot(n, l)
    t = np.dot(a - l0, n) / denom if denom else 1
    phit = l0 + t * l
    if (0.0001 < abs(denom) and (0 < t if not _t else 0 <= t <= _t) and
            0 <= np.dot(n, np.cross(ab, phit - a)) and
            0 <= np.dot(n, np.cross(bc, phit - b)) and
            0 <= np.dot(n, np.cross(ca, phit - c))):
        return True, t, phit, n
    return False, None, None, None


def create_data_quad(a, b, c):
    """
    :param a: point in space
    :param b: point in space
    :param c: point in space
    :return: quad generated by a, b and c
    """
    n, a, b, c, d = (normalize(perpendicular(Vector3D(b) - Vector3D(a), Vector3D(c) - Vector3D(a))), Vector3D(a),
                     Vector3D(b), Vector3D(c), Vector3D(c) - Vector3D(b) + Vector3D(a))
    ab, bc, cd, da = b - a, c - b, d - c, a - d
    return (n, a, b, c, d, ab, bc, cd, da), (create_data_ray(a, ab, vector_length(ab)),
                                             create_data_ray(b, bc, vector_length(bc)),
                                             create_data_ray(c, cd, vector_length(cd)),
                                             create_data_ray(d, da, vector_length(da)))


def impact_quad(element, ray):
    """
    :param element: quad data
    :param ray: ray data
    :return: impact data (colision, distance, position and normal)
    """
    n, a, b, c, d, ab, bc, cd, da = element
    l0, l, _t = ray
    denom = np.dot(n, l)
    t = np.dot(a - l0, n) / denom if denom else 1
    phit = l0 + t * l
    if (0.0001 < abs(denom) and (0 < t if not _t else 0 <= t <= _t) and
            0 <= np.dot(n, np.cross(ab, phit - a)) and
            0 <= np.dot(n, np.cross(bc, phit - b)) and
            0 <= np.dot(n, np.cross(cd, phit - c)) and
            0 <= np.dot(n, np.cross(da, phit - d))):
        return True, t, phit, n
    return False, None, None, None


def create_data_quad2D(a, b, c):
    """
    :param a: point in space
    :param b: point in space
    :param c: point in space
    :return: quad2D generated by a, b and c
    """
    n, a, b, c, d = (normalize(perpendicular(Vector3D(b) - Vector3D(a), Vector3D(c) - Vector3D(a))), Vector3D(a),
                     Vector3D(b), Vector3D(c), Vector3D(c) - Vector3D(b) + Vector3D(a))
    ab, bc, cd, da = b - a, c - b, d - c, a - d
    abN, bcN, cdN, daN = (normalize(perpendicular(a-b,n)), normalize(perpendicular(b-c,n)),
                          normalize(perpendicular(c-d,n)), normalize(perpendicular(d-a,n)))
    return (n, a, b, c, d, ab, bc, cd, da, abN, bcN, cdN, daN), (create_data_ray(a, ab, vector_length(ab)),
                                             create_data_ray(b, bc, vector_length(bc)),
                                             create_data_ray(c, cd, vector_length(cd)),
                                             create_data_ray(d, da, vector_length(da)))


def impact_quad2D(element, ray):
    """
    :param element: quad2D data
    :param ray: ray data
    :return: impact data (colision, distance, position and normal)
    """
    n, a, b, c, d, ab, bc, cd, da, abN, bcN, cdN, daN = element
    l0, l, _t = ray
    denom = np.dot(n, l)
    if 0.0001 < abs(denom):
        t = np.dot(a - l0, n) / denom
        phit = l0 + t * l
        if ((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(n, np.cross(ab, phit - a)) and
                0 <= np.dot(n, np.cross(bc, phit - b)) and
                0 <= np.dot(n, np.cross(cd, phit - c)) and
                0 <= np.dot(n, np.cross(da, phit - d))):
            return True, t, phit, n
    denom = np.dot(abN, l)
    if 0 < abs(denom):
        t = np.dot(a - l0, abN) / denom
        phit = l0 + t * l
        if ((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(n, np.cross(-abN, phit - a)) and
                0 <= np.dot(n, np.cross(abN, phit - b))):
            return True, t, phit, abN
    denom = np.dot(bcN, l)
    if 0 < abs(denom):
        t = np.dot(b - l0, bcN) / denom
        phit = l0 + t * l
        if ((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(n, np.cross(-bcN, phit - b)) and
                0 <= np.dot(n, np.cross(bcN, phit - c))):
            return True, t, phit, bcN
    denom = np.dot(cdN, l)
    if 0 < abs(denom):
        t = np.dot(c - l0, cdN) / denom
        phit = l0 + t * l
        if ((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(n, np.cross(-cdN, phit - c)) and
                0 <= np.dot(n, np.cross(cdN, phit - d))):
            return True, t, phit, cdN
    denom = np.dot(daN, l)
    if 0 < abs(denom):
        t = np.dot(d - l0, daN) / denom
        phit = l0 + t * l
        if ((0 < t if not _t else 0 <= t <= _t) and
                0 <= np.dot(n, np.cross(-daN, phit - d)) and
                0 <= np.dot(n, np.cross(daN, phit - a))):
            return True, t, phit, daN
    return False, None, None, None
