import numpy as np

def Vector3D(vector):
    """
    :param vector: array like (size=3)
    :return: numpy array
    """
    return np.array(vector, dtype=np.float32)

def normalize(vector):
    """
    :param vector: numpy array
    :return: normalized numpy array
    """
    return vector/np.linalg.norm(vector)

def perpendicular(a, b):
    """
    :param a: numpy array (size=3)
    :param b: numpy array (size=3)
    :return: numpy array (size=3) perpendicular to a and b
    """
    return np.cross(a, b)