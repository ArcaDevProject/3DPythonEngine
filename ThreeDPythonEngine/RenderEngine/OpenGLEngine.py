import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

vertex_src = """
# version 330

layout (location=0) in vec3 a_position;
layout (location=1) in vec3 a_normal;
layout (location=2) in vec3 a_color;
layout (location=3) in vec2 a_uv;

uniform mat4 local;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 v_color;
out vec3 v_n;
out vec2 v_uv;
void main()
{
    gl_Position = projection * view * model * local * vec4(a_position, 1.0);
    v_color = a_color;
    v_n = a_normal;
    v_uv = a_uv;
}
"""
#de gl position a position (reverse)
# v_color = a_color;
fragment_src = """
# version 330
in vec3 v_color;
in vec3 v_n;
in vec2 v_uv;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_uv); // * vec4(v_color, 1.0f);
}
"""

default_orthogonal_matrix = pyrr.matrix44.create_orthogonal_projection(
    left=-1.2, right=1.2, bottom=-0.75, top=0.75, near=0.1, far=100, dtype=np.float32
)

default_perspective_matrix= pyrr.matrix44.create_perspective_projection_matrix(
    fovy= 40, aspect= 520/300, near=0.1, far=100, dtype=np.float32
)
class OpenGLApi():
    """
    API to comunicate with the graphics card
    """

    def __init__(self):
        #self.__VAO = glGenVertexArrays(1)
        #glBindVertexArray(self.__VAO)
        self.__VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.__VBO)
        self.__EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__EBO)
        #self.__IMG = glGenTextures(1)
        #glBindTexture(GL_TEXTURE_2D, self.__IMG)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(24))

        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(36))

        self.default_shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glClearColor(0, 0.1, 0.1, 1)

        self.localMatrixLocation = glGetUniformLocation(self.default_shader,"local")

        self.modelMatrixLocation = glGetUniformLocation(self.default_shader,"model")

        self.viewMatrixLocation = glGetUniformLocation(self.default_shader,"view")

        self.projlMatrixLocation = glGetUniformLocation(self.default_shader,"projection")

        glUseProgram(self.default_shader)

        glUniformMatrix4fv(self.localMatrixLocation, 1, GL_FALSE, pyrr.matrix44.create_identity())

        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glAlphaFunc(GL_GREATER, 0.9)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_ALPHA_TEST)

        #glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, np.identity(4, dtype=np.float32))
        #print(default_orthogonal_matrix)
        glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, default_orthogonal_matrix)
        glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, default_perspective_matrix)
        pass

    def v1render(self, vertices):
        """
        DEPRECATED
        :param vertices: vertices to render
        :return:
        """
        v = np.array(vertices, dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        pass

    def use_program(self, program):
        """
        :param program: shader to use
        :return:
        """
        glUseProgram(program)

    def render(self, info):
        """
        :param info: info from the element to render to the scene
        :return:
        """
        position, mesh, program = info
        vertices, indices = mesh
        shader, texture = program
        texture, w, h = texture
        glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, pyrr.matrix44.create_from_translation(
            vec=np.array(position), dtype=np.float32
        ))
        if texture:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)


    def clear(self):
        """
        clear color and depth buffer
        :return:
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def set_projection_matrix(self, matrix):
        pass

    def set_camera_transforms(self, position, rotation):
        """
        :param position: 4x4 matrix
        :param rotation: 4x4 matrix
        :return:
        """
        self.__camera_position = position
        #glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, pyrr.matrix44.create_identity())

        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, pyrr.matrix44.multiply(pyrr.matrix44.create_from_translation(
            vec=-self.__camera_position, dtype=np.float32
        ), rotation))

    def flush(self):
        glFlush()

    @property
    def projection_matrix(self):
        return self.__projection_matrix

    def destroy(self):
        """
        Destroys vertex and element buffers
        :return:
        """
        #glDeleteVertexArrays(1, (self.__VAO,))
        glDeleteBuffers(1,(self.__VBO,))
        glDeleteBuffers(1,(self.__EBO,))
"""
    #print(default_orthogonal_matrix, default_orthogonal_matrix[0][3])
    
    class OpenGLApi():
    
        def __init__(self):
            #self.__VAO = glGenVertexArrays(1)
            #glBindVertexArray(self.__VAO)
            self.__VBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.__VBO)
            self.__EBO = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.__EBO)
            self.__IMG = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.__IMG)
    
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(0))
    
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(12))
    
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(24))
    
            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 44, ctypes.c_void_p(36))
    
            self.default_shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
            self.modelMatrixLocation = glGetUniformLocation(self.default_shader,"model")
    
            self.projlMatrixLocation = glGetUniformLocation(self.default_shader,"projection")
    
            glUseProgram(self.default_shader)
    
            glClearColor(0, 0.1, 0.1, 1)
            glEnable(GL_DEPTH_TEST)
    
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
            #glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, np.identity(4, dtype=np.float32))
            #print(default_orthogonal_matrix)
            glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, default_orthogonal_matrix)
            glUniformMatrix4fv(self.projlMatrixLocation, 1, GL_FALSE, default_perspective_matrix)
            pass
    
        def v1render(self, vertices):
            v = np.array(vertices, dtype=np.float32)
            glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            pass
    
        def use_program(self, program):
            glUseProgram(program)
    
        def render(self, info):
            position, mesh, program = info
            vertices, indices = mesh
            shader, texture = program
            texture, w, h = texture
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, pyrr.matrix44.create_from_translation(
                vec=np.array(position)-self.__camera_position, dtype=np.float32
            ))
            if texture:
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
            glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    
    
        def clear(self):
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
        def set_projection_matrix(self, matrix):
            pass
    
        def set_camera_position(self, position):
            self.__camera_position = position
    
        def flush(self):
            glFlush()
    
        @property
        def projection_matrix(self):
            return self.__projection_matrix
    
        def destroy(self):
            #glDeleteVertexArrays(1, (self.__VAO,))
            glDeleteBuffers(1,(self.__VBO,))
            glDeleteBuffers(1,(self.__EBO,))"""

