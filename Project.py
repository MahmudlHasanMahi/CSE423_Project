from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


class Scene:
    
    def __init__(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
        glutInitWindowSize(1000, 800)  # Window size
        glutInitWindowPosition(0, 0)  # Window position
        wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

        glutDisplayFunc(self.showScreen)  # Register display function
        glutKeyboardFunc(self.keyboardListener)  # Register keyboard listener
        glutSpecialFunc(self.specialKeyListener)
        glutMouseFunc(self.mouseListener)
        glutIdleFunc(self.idle)  # Register the idle function to move the bullet automatically
        glutMainLoop()

    def showScreen(self):
        pass
    def keyboardListener(self):
        pass
    def specialKeyListener(self):
        pass
    def mouseListener(self):
        pass

    def idle(self):
        pass


def main():
    return

if __name__ == "__main__":
    main()
