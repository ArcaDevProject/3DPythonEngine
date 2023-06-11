import numpy as np
from ThreeDPythonEngine.Objects.utils import Vector3D


def make_mesh(points, normals, uvs, faces):
    """
    :param points: vertices
    :param normals: normals for each vertex
    :param uvs: uv for each vertex
    :param faces: list of vertices forming faces
    :return: An array with the vertices from a model, and an array containing the faces
    """
    return (
    np.array((tuple(xyz + ijk + (1, 1, 1) + uv for xyz, ijk, uv in zip(points, normals, uvs)))).reshape(-1).astype(
        dtype=np.float32),
    np.array(faces).reshape(-1).astype(dtype=np.uint32))
    pass

def load_mesh(filename:str):
    """
    :param filename: File to load
    :return: An array with the vertices from a model, and an array containing the faces
    """
    v = []
    vt = []
    vn = []

    vertices = []
    faces = []
    fcount = 0

    with open(filename, "r") as file:

        line = file.readline()

        while line:

            words = line.split(" ")
            if words[0] == "v":
                v.append([float(words[1]), float(words[2]), float(words[3])])
            elif words[0] == "vt":
                vt.append([float(words[1]), float(words[2])])
            elif words[0] == "vn":
                vn.append([float(words[1]), float(words[2]), float(words[3])])
            elif words[0] == "f":
                # f 1/1/1 5/5/1 7/9/1 3/3/1
                triangleCount = len(words) - 3

                #self.make_corner(words[1], v, vt, vn, vertices)
                a, b, c = words[1].split("/")
                vertices = vertices + v[int(a)-1] + vn[int(c)-1] + [1, 1, 1] + vt[int(b)-1]
                #self.make_corner(words[2 + i], v, vt, vn, vertices)
                a, b, c = words[2].split("/")
                vertices = vertices + v[int(a)-1] + vn[int(c)-1] + [1, 1, 1] + vt[int(b)-1]
                #self.make_corner(words[3 + i], v, vt, vn, vertices)
                a, b, c = words[3].split("/")
                vertices = vertices + v[int(a)-1] + vn[int(c)-1] + [1, 1, 1] + vt[int(b)-1]
                if triangleCount == 2:
                    lf = fcount
                    faces = faces + [lf+3, lf, lf+2]
                    fcount = fcount+3
                    a, b, c = words[4].split("/")
                    vertices = vertices + v[int(a)-1] + vn[int(c)-1] + [1, 1, 1] + vt[int(b)-1]
                    faces = faces + [lf, lf+1, lf+2]
                    fcount = fcount+1
                else:
                    lf = fcount
                    faces = faces + [lf+3, lf, lf+2]
                    fcount = fcount+3


            line = file.readline()
    return np.array(vertices, dtype=np.float32), np.array(faces)

def make_colision_mesh(vertices, indices):
    """
    :param vertices: vertices
    :param indices: list of vertices for the faces
    :return: vertices, center and max distance from any vertex to the center
    """
    center = np.array(vertices).mean(axis=0)
    return np.array(vertices, dtype= np.float32), np.array(indices, dtype=np.uint32), center,\
           np.array(tuple(np.linalg.norm(center-point) for point in vertices)).max()

def make_sprite(points=None, texture=None, pixels_per_unit=32, max_size=None, pivot=0, offset=(0, 0)):
    """
    Generates new sprite
    :param points: (optional) points of the sprite in space
    :param texture: sprite texture
    :param pixels_per_unit: pixels per unit (default 32)
    :param max_size: max shape
    :param pivot: pivot
    :param offset: offset from the pivot
    :return: mesh data
    """
    if not points:
        shape = np.array((32,32), dtype=np.uint32)
        if texture is not None:
            shape = texture.shape
        shape = shape[0] / pixels_per_unit, shape[1] / pixels_per_unit, 0
        if max_size is not None:
            shape = max(max_size[0], shape[0]), max(max_size[1], shape[1]), 0
        if pivot == 0:
            pivot_point = shape[0] / 2, shape[1] / 2, 0
        if pivot == 12:
            pivot_point = shape[0]/2, shape[1], 0
        if pivot == 2:
            pivot_point = shape[0], shape[1], 0
        if pivot == 3:
            pivot_point = shape[0], shape[1]/2, 0
        if pivot == 4:
            pivot_point = shape[0], 0, 0
        if pivot == 6:
            pivot_point = shape[0]/2, 0, 0
        if pivot == 8:
            pivot_point = 0, 0, 0
        if pivot == 9:
            pivot_point = 0, shape[1]/2, 0
        if pivot == 10:
            pivot_point = 0, shape[1], 0
        pivot_point = np.array(pivot_point, dtype=np.float32)-np.array(offset+(0,), dtype=np.float32)
        points = ((0,0,0),(shape[0],0,0),(0, shape[1],0),shape)
        points = [ tuple(np.array(p, dtype=np.float32) - pivot_point) for p in points]
    else:
        points = [ tuple(np.array(p, dtype=np.float32)) for p in points]

    normals = ((0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1))

    uvs = ((0.0, 1.0),(1.0, 1.0),(0.0, 0.0),(1.0, 0.0))

    faces = (0, 1, 2), (1, 2, 3)

    return make_mesh(points, normals, uvs, faces)

def sprite_frames_by_grid(grid=(1, 1)):
    """
    :param grid: grid that generates the sprite sheet
    :return: a list of masks containing every sprite state
    """
    xf, yf = grid
    frames = []
    for h in range(yf):
        top, bot = h/yf, (h+1)/yf
        for w in range(xf):
            lef, rig = w/xf, (w+1)/xf
            frames.append(np.array((0, 0, 0, 0, 0, 0, 0, 0, 0, lef, bot,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, rig, bot,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, lef, top,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, rig, top), dtype=np.float32))
    return frames

def load_texture(route:str):
    """
    :param route: route of the texture file
    :return: texture as a numpy array
    """
    from PIL import Image
    im = Image.open(route)
    im = (im.convert("RGBA").tobytes(),) + im.size
    return im


