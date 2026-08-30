from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

CHUNK_SIZE = 600
CHUNK_COUNT = 16


class Car:

    def __init__(self, x, y, z, quadric):

        self.x = x
        self.y = y
        self.z = z

        # speed[0] = x speed, speed[1] = y speed, speed[2] = z speed
        self.speed = [0, 0, 0]

        # how much speed builds up per frame while a key is held
        self.accelration = 0.3

        # how much speed decays per frame once the key is released
        self.decelration = 0.2

        # top speed in any direction
        self.max_speed = 12

        # how fast the car rotates (degrees per frame) while
        # LEFT/RIGHT is held
        self.turn_speed = 3


        self.player_angle = 0.0
        self.wheel_spin_angle = 0.0
        self.wheel_spin_speed = 5.0
        self.quadric = quadric


    def draw_car(self):

        glPushMatrix()

        # ----------------------------------------------------
        # CAR POSITION
        # ----------------------------------------------------

        glTranslatef(
            self.x,
            self.y,
            self.z
        )

        # ----------------------------------------------------
        # CAR ROTATION
        #
        # The car's front points toward -Z
        # ----------------------------------------------------

        glRotatef(
            self.player_angle,
            0,
            1,
            0
        )

        # ====================================================
        # CAR BODY
        # ====================================================

        glPushMatrix()

        glScalef(1.5, 0.5, 2.0)

        glColor3f(
            0.05,
            0.15,
            0.85
        )

        glutSolidCube(60)

        glPopMatrix()

        # ====================================================
        # CABIN
        # ====================================================

        glPushMatrix()

        glTranslatef(0, 35, 0)
        glScalef(1.0, 0.5, 1.0)

        glColor3f(
            0.05,
            0.05,
            0.05
        )

        glutSolidCube(50)

        glPopMatrix()

        # ====================================================
        # FRONT WINDSHIELD
        # ====================================================

        glPushMatrix()

        # Front of car is -Z
        glTranslatef(0, 35, -25)
        glScalef(0.75, 0.5, 0.05)

        glColor3f(
            0.1,
            0.4,
            0.8
        )

        glutSolidCube(50)

        glPopMatrix()

        # ====================================================
        # FRONT BUMPER
        # ====================================================

        glPushMatrix()

        glTranslatef(0, 5, -63)
        glScalef(1.4, 0.15, 0.15)

        glColor3f(
            0.02,
            0.02,
            0.02
        )

        glutSolidCube(60)

        glPopMatrix()

        # ====================================================
        # HEADLIGHTS
        # ====================================================

        glColor3f(
            1.0,
            1.0,
            0.2
        )

        # Left headlight

        glPushMatrix()

        glTranslatef(-35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()

        # Right headlight

        glPushMatrix()

        glTranslatef(35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()

        # ====================================================
        # WHEELS
        # ====================================================

        wheel_positions = [

            (-45, -25, -45),
            (30, -25, -45),
            (-45, -25, 45),
            (30, -25, 45)

        ]

        for x, y, z in wheel_positions:

            self.draw_wheel(x, y, z)

        glPopMatrix()

    def update(self, keys):

        if GLUT_KEY_UP in keys:

            self.speed[2] += self.accelration

            if self.speed[2] > self.max_speed:

                self.speed[2] = self.max_speed

        elif GLUT_KEY_DOWN in keys:

            self.speed[2] -= self.accelration

            if self.speed[2] < -self.max_speed:

                self.speed[2] = -self.max_speed

        else:

            if self.speed[2] > 0:

                self.speed[2] -= self.decelration

                if self.speed[2] < 0:

                    self.speed[2] = 0

            elif self.speed[2] < 0:

                self.speed[2] += self.decelration

                if self.speed[2] > 0:

                    self.speed[2] = 0

   

        if GLUT_KEY_LEFT in keys:

            self.player_angle += self.turn_speed

        if GLUT_KEY_RIGHT in keys:

            self.player_angle -= self.turn_speed

   

        angle_rad = math.radians(self.player_angle)

        self.x -= math.sin(angle_rad) * self.speed[2]
        self.z -= math.cos(angle_rad) * self.speed[2]

        self.y += self.speed[1]

    def draw_circle_cap(self, z, radius=15):

        segments = 15
        spoke_every = 4

        glBegin(GL_TRIANGLE_FAN)

        # Center point of the fan (hub color)
        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(0, 0, z)

        for i in range(segments + 1):

            angle = (
                2 * math.pi
                * i / segments
            )

            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            if i % spoke_every == 0:

                glColor3f(0.0, 0.0, 0.0)

            else:

                glColor3f(0.7, 0.7, 0.7)

            glVertex3f(x, y, z)

        glEnd()

    def show_car(self):

        self.draw_car()



    def draw_wheel(self, x, y, z):

        glPushMatrix()

        glTranslatef(
            x,
            y,
            z
        )

        # Wheels are along X axis
        glRotatef(
            90,
            0,
            1,
            0
        )

        # ----------------------------------------------------
        # SPIN (rotates the tread pattern around the axle)
        # ----------------------------------------------------

        glRotatef(
            self.wheel_spin_angle,
            0,
            0,
            1
        )

        glColor3f(
            0.02,
            0.02,
            0.02
        )

        # ----------------------------------------------------
        # TUBE
        # ----------------------------------------------------

        gluCylinder(
            self.quadric,
            15,
            15,
            15,
            10,
            10
        )


        self.draw_circle_cap(-0.5)
        self.draw_circle_cap(15.5)

        glPopMatrix()


class CarWarfare:

    def __init__(self):

        # ----------------------------------------------------
        # GLUT INITIALIZATION
        # ----------------------------------------------------

        glutInit()

        glutInitDisplayMode(
            GLUT_DOUBLE |
            GLUT_RGB |
            GLUT_DEPTH
        )

        glutInitWindowSize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        glutInitWindowPosition(0, 0)

        glutCreateWindow(
            b"Car Warfare"
        )

        # Enable depth testing
        glEnable(GL_DEPTH_TEST)

        # Background
        glClearColor(
            0.50,
            0.75,
            1.0,
            1.0
        )

        # ----------------------------------------------------
        # HELD ARROW KEYS (tracked so the car can accelerate
        # smoothly while a key is held down)
        # ----------------------------------------------------

        self.keys = set()

        # ----------------------------------------------------
        # CAMERA PAN OFFSET (controlled by arrow keys)
        # ----------------------------------------------------

        self.arrow = [0, 0]

        # ----------------------------------------------------
        # WORLD / CHUNKS
        # ----------------------------------------------------

        self.chunks = {}

        self.generate_world()

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.camera_height = 220
        self.camera_distance = 350

        # The camera's own angle, separate from the car's.
        # It gradually chases player_angle instead of
        # snapping to it, creating a smooth swing effect
        # when the car turns.
        self.camera_angle = 0.0

        # How quickly the camera catches up each frame.
        # Smaller = more lag/swing, larger = snappier.
        self.camera_smoothing = 0.1

        # ----------------------------------------------------
        # QUADRIC (used for wheels) + PLAYER CAR
        # ----------------------------------------------------

        quadric = gluNewQuadric()
        self.quadric = quadric

        self.player = Car(0, 40, 0, quadric)

        glutSpecialFunc(self.specialKeyDown)
        glutSpecialUpFunc(self.specialKeyUp)

        glutDisplayFunc(
            self.showScreen
        )

        glutIdleFunc(
            self.idle
        )


        glutMainLoop()

    # ========================================================
    # CHUNK GENERATION
    # ========================================================

    def get_chunk_seed(self, chunk_x, chunk_z):

        return (
            chunk_x * 73856093 +
            chunk_z * 19349663
        )

    def generate_chunk(self, chunk_x, chunk_z):

        # Deterministic chunk information
        return {
            "x": chunk_x,
            "z": chunk_z
        }

    def generate_world(self):

        self.chunks = {}

        half = CHUNK_COUNT // 2

        for x in range(-half, half):

            for z in range(-half, half):

                self.chunks[(x, z)] = self.generate_chunk(
                    x,
                    z
                )

    # ========================================================
    # GROUND / CHUNK BORDER
    # ========================================================

    def draw_ground(self):

        half = CHUNK_SIZE / 2

        glColor3f(
            0.25,
            0.55,
            0.20
        )

        glBegin(GL_QUADS)

        glVertex3f(-half, 0, -half)
        glVertex3f(half, 0, -half)
        glVertex3f(half, 0, half)
        glVertex3f(-half, 0, half)

        glEnd()

    def draw_chunk_border(self):

        half = CHUNK_SIZE / 2

        glColor3f(
            0.15,
            0.15,
            0.15
        )

        glLineWidth(1)

        glBegin(GL_LINE_LOOP)

        glVertex3f(-half, 1, -half)
        glVertex3f(half, 1, -half)
        glVertex3f(half, 1, half)
        glVertex3f(-half, 1, half)

        glEnd()

    # ========================================================
    # WORLD
    # ========================================================

    def draw_world(self):

        for key, chunk in self.chunks.items():

            chunk_x = chunk["x"]
            chunk_z = chunk["z"]

            # Convert chunk coordinates to world coordinates

            world_x = (
                chunk_x * CHUNK_SIZE
            )

            world_z = (
                chunk_z * CHUNK_SIZE
            )

            glPushMatrix()

            glTranslatef(
                world_x,
                0,
                world_z
            )

            self.draw_ground()
            self.draw_chunk_border()

            glPopMatrix()

    # ========================================================
    # CAMERA (follows the car)
    # ========================================================

    def setupCamera(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(
            70,
            WINDOW_WIDTH / WINDOW_HEIGHT,
            0.1,
            10000
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # ----------------------------------------------------
        # CAMERA ANGLE (smoothed -- lags behind the car's
        # actual angle, giving a swinging follow effect)
        # ----------------------------------------------------

        player = self.player
        angle = math.radians(self.camera_angle)

        # ----------------------------------------------------
        # CAMERA BEHIND CAR
        #
        # Car faces -Z.
        # Therefore camera goes toward +Z.
        # Arrow keys nudge the camera around via self.arrow.
        # ----------------------------------------------------

        camera_x = (player.x + math.sin(angle) * self.camera_distance) 

        camera_z = (player.z + math.cos(angle) * self.camera_distance) 

        camera_y = self.camera_height

        # ----------------------------------------------------
        # CAMERA LOOKS AT CAR
        # ----------------------------------------------------

        target_x = player.x
        target_y = player.y
        target_z = player.z

        gluLookAt(

            camera_x,
            camera_y,
            camera_z,

            target_x,
            target_y,
            target_z,

            0,
            1,
            0
        )

    # ========================================================
    # UPDATE (IDLE)
    # ========================================================

    def idle(self):

        self.player.wheel_spin_angle += self.player.wheel_spin_speed

        if self.player.wheel_spin_angle >= 360:

            self.player.wheel_spin_angle -= 360
        self.player.update(self.keys)

   
        angle_diff = self.player.player_angle - self.camera_angle

        self.camera_angle += angle_diff * self.camera_smoothing


        glutPostRedisplay()

    # ========================================================
    # DISPLAY
    # ========================================================

    def showScreen(self):

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        glLoadIdentity()

        glViewport(
            0,
            0,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        # Camera
        self.setupCamera()

        # World
        self.draw_world()

        # Car
        self.player.show_car()

        glutSwapBuffers()

    def specialKeyDown(self, key, x, y):
        """
        Called once when an arrow key goes down. We just
        remember that it's held -- the actual movement
        happens continuously in Car.update().
        """

        self.keys.add(key)

    def specialKeyUp(self, key, x, y):
        """
        Called when an arrow key is released.
        """

        if key in self.keys:

            self.keys.remove(key)


def main():

    CarWarfare()


if __name__ == "__main__":

    main()