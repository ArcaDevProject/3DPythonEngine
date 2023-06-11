import glfw
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
from ThreeDPythonEngine.RenderEngine.OpenGLEngine import OpenGLApi as GPU
from ThreeDPythonEngine.GameClasses._GameScene import GameScene

class Game(object):

    def __init__(self, w=512, h=512, title='Game Window', a=None, b=None, scene=GameScene()):
        """
        :param w: screen width
        :param h: screen height
        :param title: Game name
        :param a: Unused
        :param b: Unused
        :param scene: first scene
        """

        # Cancels run if
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # unlock framerate
        #glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, False)
        self.__window = glfw.create_window(w, 300, title, a, b)

        if not self.__window:
            raise Exception("glfw can not be initialized!")

        glfw.set_window_pos(self.__window, 400, 200)

        glfw.make_context_current(self.__window)

        self.should_close = glfw.window_should_close

        glfw.set_key_callback(self.__window, self.key_callback)

        self.__inputs = []

        self.__gpu = GPU()

        self.__scene = scene
        self.__scene.set_GPU(self.__gpu)

    def set_scene(self, scene):
        """
        :param scene: set new scene
        :return:
        """
        self.__scene = scene
        self.__scene.set_GPU(self.__gpu)

    def run(self):
        """
        runs the game
        :return:
        """
        now = 0
        previous = 0
        while not self.should_close(self.__window):
            previous, now = now, glfw.get_time()
            self.__inputs = []
            glfw.poll_events()
            self.__scene.detect_colisions()
            self.__scene.mouse_update(glfw.get_cursor_pos(self.__window), now-previous)
            self.__scene.update(self.__inputs, now-previous)
            """The clear"""
            self.__gpu.clear()
            """The render"""
            self.scene.render()
            glfw.swap_buffers(self.__window)
            """The flush""" # use instead of swapbuffer if framerate unlocked
            #self.__gpu.flush()
        self.__gpu.destroy()
        glfw.terminate()

    def key_callback(self, window, key, scancode, action, mods):
        """
        gets keyboard input
        :param window: window
        :param key: key pressed
        :param scancode: scancode
        :param action: action
        :param mods: mods
        :return:
        """
        self.__inputs.append((key, scancode, action, mods))
        #print((key, scancode, action, mods))
        pass

    @property
    def scene(self):
        return self.__scene