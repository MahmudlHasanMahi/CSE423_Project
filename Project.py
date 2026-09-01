from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

import math


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

CHUNK_SIZE = 600
CHUNK_COUNT = 16

TREE_RADIUS = 40
STONE_RADIUS = 35
MAX_PROJECTILE_DISTANCE = (CHUNK_COUNT // 2) * CHUNK_SIZE
class Projectile:
    def __init__(self, x, y, z, angle, quadric):
        self.x = x
        self.y = y
        self.z = z

        self.angle = angle
        self._speed = 75

        self.quadric = quadric

        self.alive = True
    @property
    def speed(self):
        return self._speed
    def update(self):
    
        angle_rad = math.radians(self.angle)
        self.x -= math.sin(angle_rad) * self.speed
        self.z -= math.cos(angle_rad) * self.speed

    def set_speed(self,speed):
        self._speed = speed    



class Grenade(Projectile):
    
    def __init__(self, x, y, z, angle, quadric):

        super().__init__(x, y, z, angle, quadric)

        angle_rad = math.radians(angle)

        speed = 25
        self.vx = -math.sin(angle_rad) * speed
        self.vz = -math.cos(angle_rad) * speed
        self.vy = 10

        self.gravity = 0.6

        self.exploded = False
        self.explosion_timer = 0
        self.explosion_duration = 7

    def update(self):

        if self.exploded:

            self.explosion_timer -= 1

            if self.explosion_timer <= 0:
                self.alive = False
            return


        self.vy -= self.gravity

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

        if self.y <= 10:

            self.y = 10
            self.exploded = True
            self.explosion_timer = self.explosion_duration

    def draw(self):

        glPushMatrix()

        glTranslatef(
            self.x,
            self.y,
            self.z
        )

        if not self.exploded:

            glColor3f(0.1, 0.35, 0.1)

            glutSolidSphere(
                8,
                12,
                12
            )

        else:

            t = self.explosion_timer / self.explosion_duration
            radius = (1 - t) * 150

            glColor3f(1.0, 0.5 * t + 0.2, 0.0)

            glutSolidSphere(
                radius,
                14,
                14
            )

        glPopMatrix()
class Bullet(Projectile):
    
    def __init__(self, x, y, z, angle, quadric):
        super().__init__(x, y, z, angle, quadric)
        

    def draw(self):

        glPushMatrix()

        glTranslatef(
            self.x,
            self.y,
            self.z
        )

        glColor3f(
            1.0,
            1.0,
            0.0
        )

        glutSolidSphere(
            4,
            10,
            10
        )

        glPopMatrix()


class BaseCar:
    
    wheel_positions = [
        (-45, -25, -45),
        (30, -25, -45),
        (-45, -25, 45),
        (30, -25, 45)
    ]

    def __init__(self, x, y, z, quadric):

        self.x = x
        self.y = y
        self.z = z

        self.angle = 0.0
        self.wheel_spin_angle = 0.0

        self.gun_rotation = 0.0

        self.quadric = quadric
        self.radius = 35
        self.muzzle_flash_timer = 0
        self.muzzle_flash_duration = 4

    def draw_body(self):

        glPushMatrix()

        glScalef(1.5, 0.5, 2.0)

        glColor3f(0.05, 0.15, 0.85)

        glutSolidCube(60)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 35, 0)
        glScalef(1.0, 0.5, 1.0)

        glColor3f(0.05, 0.05, 0.05)

        glutSolidCube(50)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 35, -25)
        glScalef(0.75, 0.5, 0.05)

        glColor3f(0.1, 0.4, 0.8)

        glutSolidCube(50)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 5, -63)
        glScalef(1.4, 0.15, 0.15)

        glColor3f(0.02, 0.02, 0.02)

        glutSolidCube(60)

        glPopMatrix()

        glColor3f(1.0, 1.0, 0.2)

        glPushMatrix()

        glTranslatef(-35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()

    def draw_circle_cap(self, z, radius=15):

        segments = 15
        spoke_every = 4

        glBegin(GL_TRIANGLE_FAN)

        glColor3f(0.0, 0.0, 0.0)
        glVertex3f(0, 0, z)

        for i in range(segments + 1):

            angle = 2 * math.pi * i / segments

            x = radius * math.cos(angle)
            y = radius * math.sin(angle)

            if i % spoke_every == 0:
                glColor3f(0.0, 0.0, 0.0)
            else:
                glColor3f(0.7, 0.7, 0.7)

            glVertex3f(x, y, z)

        glEnd()

    def draw_wheel(self, x, y, z):

        glPushMatrix()

        glTranslatef(x, y, z)

        glRotatef(90, 0, 1, 0)

        glRotatef(
            self.wheel_spin_angle,
            0,
            0,
            1
        )

        glColor3f(0.02, 0.02, 0.02)

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

    def draw_extras(self):
        pass   

    def draw_car(self):

        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 1, 0)

        self.draw_body()

        for wx, wy, wz in self.wheel_positions:
            self.draw_wheel(wx, wy, wz)

        self.draw_extras()

        glPopMatrix()
    

    def _draw_machine_gun(self):
        
        glPushMatrix()
        glTranslatef(0, 55, 0)
        glColor3f(0.15, 0.15, 0.15)
        glutSolidCube(35)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 60, 0)
        glRotatef(self.gun_rotation, 0, 0, 1)

        radius = 5
        w = 20

        for angle in [0, 90, 180, 270]:

            glPushMatrix()

            angle_rad = math.radians(angle)
            x = math.cos(angle_rad) * radius
            y = math.sin(angle_rad) * radius

            glTranslatef(x, y, 0)
            glRotatef(180, 1, 0, 0)

            for i in range(4):

                if i == 0:
                    glColor3f(71/255, 195/255, 230/255)
                elif i == 1:
                    glColor3f(1, 1, 0)
                elif i == 2:
                    glColor3f(0, 0, 0)
                else:
                    glColor3f(1, 1, 1)
                    if self.muzzle_flash_timer > 0:
                        glColor3f(219/255, 80/255, 61/255)

                glPushMatrix()
                glTranslatef(0, 0, i * w)

                gluCylinder(self.quadric, 2, 2, w, 10, 10)

                glPopMatrix()

            glPopMatrix()

        glPopMatrix()

class EnemyCar(BaseCar):
    
    def __init__(self, x, z, quadric):

        super().__init__(x, 40, z, quadric)

        self.move_speed = 5
        self.alive = True
        self.close_to_player =1000

        self.health = 100

        self.bullets = []
        self.fire_range = 1000 
        self.fire_rate = 40        
        self.fire_delay= 0


    def fire_bullet(self):
    
        angle_rad = math.radians(self.angle)
        distance = 70

        bullet_x = self.x - math.sin(angle_rad) * distance
        bullet_z = self.z - math.cos(angle_rad) * distance
        bullet_y = self.y + 60

        self.bullets.append(
            Bullet(bullet_x, bullet_y, bullet_z, self.angle, self.quadric)
        )

        self.muzzle_flash_timer = self.muzzle_flash_duration


    def update(self, player_x, player_z):

        detect_radius= CHUNK_COUNT * CHUNK_SIZE

        dx = player_x - self.x
        dz = player_z - self.z

        dist = math.hypot(dx, dz)

        if dist < detect_radius :

            self.angle = math.degrees(math.atan2(-dx, -dz))
            if  dist > self.close_to_player:
                angle_rad = math.radians(self.angle)

                self.x -= math.sin(angle_rad) * self.move_speed
                self.z -= math.cos(angle_rad) * self.move_speed

                self.wheel_spin_angle += self.move_speed
                
            if dist < self.fire_range and self.fire_delay <= 0:
        
                self.fire_bullet()
                self.fire_delay = self.fire_rate

        self.gun_rotation += 5
        if self.fire_delay > 0:
            self.fire_delay -= 1

        for bullet in self.bullets:
            bullet.update()

            bx = bullet.x - self.x
            bz = bullet.z - self.z

            if math.hypot(bx, bz) > MAX_PROJECTILE_DISTANCE:
                bullet.alive = False

        self.bullets = [bul for bul in self.bullets if bul.alive]

        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= 1

    def draw_extras(self):
        self._draw_machine_gun()
        for bullet in self.bullets:
                    bullet.draw()
    
    def draw_body(self):
        # return super().draw_body()
        glPushMatrix()

        glScalef(1.5, 0.5, 2.0)

        glColor3f(128/255, 26/255, 19/255)

        glutSolidCube(60)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 35, 0)
        glScalef(1.0, 0.5, 1.0)

        glColor3f(0.05, 0.05, 0.05)

        glutSolidCube(50)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 35, -25)
        glScalef(0.75, 0.5, 0.05)

        glColor3f(0.1, 0.4, 0.8)

        glutSolidCube(50)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(0, 5, -63)
        glScalef(1.4, 0.15, 0.15)

        glColor3f(0.02, 0.02, 0.02)

        glutSolidCube(60)

        glPopMatrix()

        glColor3f(1.0, 1.0, 0.2)

        glPushMatrix()

        glTranslatef(-35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()

        glPushMatrix()

        glTranslatef(35, 10, -60)
        glScalef(0.3, 0.25, 0.15)

        glutSolidCube(60)

        glPopMatrix()
    


    def draw(self):
    
        self.draw_car()

        for bullet in self.bullets:
            bullet.draw()
        
    
class PlayerCar(BaseCar):
    
    def __init__(self, x, y, z, quadric):

        super().__init__(x, y, z, quadric)

        self.speed = [0, 0, 0]

        self.accelration = 0.07
        self.decelration = 0.2
        self.max_speed = 30
        self.turn_speed = 1.5

        self.health = 100
        self.was_colliding = False

     
        self.bullets = []
     

        self.grenades = []
        self.weapon_types = ["gun", "grenade"]
        self.weapon_index = 0
        self.grenade_cooldown = 0
        self.grenade_fire_rate = 60

    def switch_weapon(self):
        self.weapon_index = 1 - self.weapon_index

    def fire_bullet(self):
    
        if self.weapon_types[self.weapon_index] == "gun":
            self._fire_gun()
        else:
            if self.grenade_cooldown <= 0:
                self._fire_grenade()
                self.grenade_cooldown = self.grenade_fire_rate

    def _fire_gun(self):

        angle_rad = math.radians(self.angle)
        distance = 110

        bullet_x = self.x - math.sin(angle_rad) * distance
        bullet_z = self.z - math.cos(angle_rad) * distance
        bullet_y = self.y + 60

        self.bullets.append(
            Bullet(bullet_x, bullet_y, bullet_z, self.angle, self.quadric)
        )

        self.muzzle_flash_timer = self.muzzle_flash_duration

    def _fire_grenade(self):

        angle_rad = math.radians(self.angle)
        distance = 90

        x = self.x - math.sin(angle_rad) * distance
        z = self.z - math.cos(angle_rad) * distance
        y = self.y + 55

        self.grenades.append(
            Grenade(x, y, z, self.angle, self.quadric)
        )

        self.muzzle_flash_timer = self.muzzle_flash_duration

    def draw_extras(self):
        self.draw_gun()

    def draw_gun(self):
        if self.weapon_types[self.weapon_index] == "gun":
            self._draw_machine_gun()
        else:
            self._draw_grenade_launcher()

    

    def _draw_grenade_launcher(self):

        glPushMatrix()
        glTranslatef(0, 55, 0)
        glColor3f(0.2, 0.25, 0.15)
        glutSolidCube(35)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 60, 0)
        glTranslatef(0, 0, -80)

        glColor3f(0.15, 0.2, 0.1)

        if self.muzzle_flash_timer > 0:
            glColor3f(219/255, 80/255, 61/255)

        gluCylinder(self.quadric, 10, 10, 70, 12, 12)

        glPopMatrix()

    def draw_bullets(self):

        for bullet in self.bullets:
            bullet.draw()

        for grenade in self.grenades:
            grenade.draw()

    def draw_health_bar(self, x, y, width, height):

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(0.2, 0.2, 0.2)

        glBegin(GL_QUADS)
        glVertex3f(x, y, -0.5)
        glVertex3f(x + width, y, -0.5)
        glVertex3f(x + width, y + height, -0.5)
        glVertex3f(x, y + height, -0.5)
        glEnd()

        health_ratio = self.health / 100
        filled_width = width * health_ratio

        if health_ratio > 0.5:
            glColor3f(0.2, 0.8, 0.2)
        elif health_ratio > 0.25:
            glColor3f(0.9, 0.7, 0.1)
        else:
            glColor3f(0.9, 0.1, 0.1)

        glBegin(GL_QUADS)
        glVertex3f(x, y, 0.0)
        glVertex3f(x + filled_width, y, 0.0)
        glVertex3f(x + filled_width, y + height, 0.0)
        glVertex3f(x, y + height, 0.0)
        glEnd()

        glColor3f(1, 1, 1)

        glBegin(GL_LINE_LOOP)
        glVertex3f(x, y, 0.5)
        glVertex3f(x + width, y, 0.5)
        glVertex3f(x + width, y + height, 0.5)
        glVertex3f(x, y + height, 0.5)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_text(self, x, y, text, font=GLUT_BITMAP_HELVETICA_18):

        glColor3f(1, 1, 1)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluOrtho2D(0, 1000, 0, 800)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glRasterPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ord(ch))

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def update(self, keys, collision_check):

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

        if self.speed[2] < 0:
            if GLUT_KEY_LEFT in keys:
                self.angle -= self.turn_speed
            if GLUT_KEY_RIGHT in keys:
                self.angle += self.turn_speed
        else:
            if GLUT_KEY_LEFT in keys:
                self.angle += self.turn_speed
            if GLUT_KEY_RIGHT in keys:
                self.angle -= self.turn_speed

        angle_rad = math.radians(self.angle)

        new_x = self.x - math.sin(angle_rad) * self.speed[2]
        new_z = self.z - math.cos(angle_rad) * self.speed[2]

        flag, coord = collision_check(new_x, new_z)

        if flag:

            current_speed = self.speed[2]
            self.speed[2] = 0

            if not self.was_colliding:
                self.health = max(0, self.health - int(20 * current_speed / self.max_speed))

            self.was_colliding = True

        else:

            self.was_colliding = False
            self.x = new_x
            self.z = new_z

        self.y += self.speed[1]
        self.gun_rotation += 5

        for bullet in self.bullets:
            bullet.update()
            dx = bullet.x - self.x
            dz = bullet.z - self.z
            if math.hypot(dx, dz) > MAX_PROJECTILE_DISTANCE:
                bullet.alive = False

        for grenade in self.grenades:
            grenade.update()
            dx = grenade.x - self.x
            dz = grenade.z - self.z
            if math.hypot(dx, dz) > MAX_PROJECTILE_DISTANCE:
                grenade.alive = False

        self.bullets = [b for b in self.bullets if b.alive]
        self.grenades = [g for g in self.grenades if g.alive]

        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= 1
        if self.grenade_cooldown > 0:
            self.grenade_cooldown -= 1

        self.wheel_spin_angle += self.speed[2]

    def show_car(self):

        self.draw_car()

        self.draw_text(10, 770, f"Speed {int(abs(self.speed[2]))}")
        self.draw_text(10, 750, "Health")
        self.draw_health_bar(90, 745, 150, 18)

        self.draw_bullets()
class CarWarfare:
    
    def __init__(self):
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

        glEnable(GL_DEPTH_TEST)

        glClearColor(
            0.50,
            0.75,
            1.0,
            1.0
        )
        self.GAMEOVER = False

        self.keys = set()

        self.arrow = [0, 0]
        self.chunks = {}
        self.enemy_cars = {}


        self.camera_height = 220
        self.camera_distance = 350

        self.camera_angle = 0.0

        self.camera_smoothing = 0.06

        quadric = gluNewQuadric()
        self.quadric = quadric

        self.generate_world()
        self.player = PlayerCar(0, 40, 0, quadric)
        self.pov = False
        glutSpecialFunc(self.specialKeyDown)
        glutSpecialUpFunc(self.specialKeyUp)
        glutKeyboardFunc(self.keyboardListener)

        glutDisplayFunc(
            self.showScreen
        )

        glutIdleFunc(
            self.idle
        )

        glutMainLoop()

    def get_chunk_seed(self, chunk_x, chunk_z):

        return (
            chunk_x * 73856093 +
            chunk_z * 19349663
        )

    def generate_chunk(self, chunk_x, chunk_z):

        ran = random.Random(self.get_chunk_seed(chunk_x, chunk_z))

        trees = []
        stones = []
        enemies = []

  
        if random.random() < 0.25:
            for i in range(random.randrange(1, 3, 1)):

                x = ran.uniform(
                    -CHUNK_SIZE / 2 + 50,
                    CHUNK_SIZE / 2 - 50
                )

                z = ran.uniform(
                    -CHUNK_SIZE / 2 + 50,
                    CHUNK_SIZE / 2 - 50
                )

                # Random tree size
                scale = ran.uniform(0.8, 1.4)

                trees.append({
                    "x": x,
                    "z": z,
                    "scale": scale
                })

            # -----------------------------
            # Generate stones
            # -----------------------------
        if random.random() < 0.1:

                x = ran.uniform(
                    -CHUNK_SIZE / 2 + 30,
                    CHUNK_SIZE / 2 - 30
                )

                z = ran.uniform(
                    -CHUNK_SIZE / 2 + 30,
                    CHUNK_SIZE / 2 - 30
                )

                scale = ran.uniform(0.5, 1.5)

                stones.append({
                    "x": x,
                    "z": z,
                    "scale": scale
                })
            # -----------------------------
        if chunk_x != 0 or chunk_z != 0: 

            if ran.random() < 0.01:


                x = ran.uniform(
                    -CHUNK_SIZE / 2 + 60,
                    CHUNK_SIZE / 2 - 60
                )

                z = ran.uniform(
                    -CHUNK_SIZE / 2 + 60,
                    CHUNK_SIZE / 2 - 60
                )

                enemies.append({
                    "x": x,
                    "z": z
                })
                

        return {
            "x": chunk_x,
            "z": chunk_z,
            "trees": trees,
            "stones": stones,
            "enemies": enemies
        }

    def draw_tree(self):

        # Tree trunk
        glPushMatrix()

        glColor3f(0.35, 0.18, 0.05)

        glTranslatef(0, 45, 0)

        glScalef(0.25, 1.5, 0.25)

        glutSolidCube(40)

        glPopMatrix()

        # Tree leaves
        glPushMatrix()

        glColor3f(0.05, 0.45, 0.05)

        glTranslatef(0, 120, 0)

        glutSolidSphere(60, 12, 12)

        glPopMatrix()

    def draw_stone(self):

        glPushMatrix()

        glColor3f(0.35, 0.35, 0.35)

        glScalef(1.5, 0.8, 1.2)

        glutSolidSphere(25, 10, 10)

        glPopMatrix()

    def generate_world(self):

        self.chunks_metadata = {}
        player_chunk_x = 0
        player_chunk_z = 0

        half = CHUNK_COUNT // 2

        for x in range(player_chunk_x - half, player_chunk_x + half + 1):

            for z in range(player_chunk_z - half, player_chunk_z + half + 1):

                chunk = self.generate_chunk(x, z)
                self.chunks_metadata[(x, z)] = chunk

                self.spawn_enemies_for_chunk(x, z, chunk)

    
    def spawn_enemies_for_chunk(self, chunk_x, chunk_z, chunk):
    
        world_x = chunk_x * CHUNK_SIZE
        world_z = chunk_z * CHUNK_SIZE

        car_list = []

        for enemy in chunk["enemies"]:

            ex = world_x + enemy["x"]
            ez = world_z + enemy["z"]

            car_list.append(EnemyCar(ex, ez, self.quadric))

        self.enemy_cars[(chunk_x, chunk_z)] = car_list

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

    def get_player_chunk(self):
        chunk_x = math.floor(
            self.player.x / CHUNK_SIZE + 0.5
        )

        chunk_z = math.floor(
            self.player.z / CHUNK_SIZE + 0.5
        )
        return chunk_x, chunk_z

    def update_chunks(self):

        p_chunk_x, p_chunk_z = self.get_player_chunk()

        half = CHUNK_COUNT // 2

        # --------------------------------
        # Generate missing chunks
        # --------------------------------

        for x in range(p_chunk_x - half,p_chunk_x + half + 1):

            for z in range(p_chunk_z - half,p_chunk_z + half + 1):

                if (x, z) not in self.chunks_metadata:


                    chunk = self.generate_chunk(x, z)
                    self.chunks_metadata[(x, z)] = chunk

                    self.spawn_enemies_for_chunk(x, z, chunk)



        chunks_to_remove = []

        for chunk_x, chunk_z in self.chunks_metadata:

            if (
                abs(chunk_x - p_chunk_x) > half
                or
                abs(chunk_z - p_chunk_z) > half
            ):

                chunks_to_remove.append(
                    (chunk_x, chunk_z)
                )

        for chunk in chunks_to_remove:

            del self.chunks_metadata[chunk]
            if chunk in self.enemy_cars:
                del self.enemy_cars[chunk]

        return chunk_x, chunk_z

    def check_collision(self, x, z):

        player_chunk_x, player_chunk_z = self.get_player_chunk()

        for dx in (-1, 0, 1):

            for dz in (-1, 0, 1):

                chunk = self.chunks_metadata.get(
                    (player_chunk_x + dx, player_chunk_z + dz)
                )

                if chunk is None:
                    continue

                world_x = chunk["x"] * CHUNK_SIZE
                world_z = chunk["z"] * CHUNK_SIZE

                for tree in chunk["trees"]:

                    tx = world_x + tree["x"]
                    tz = world_z + tree["z"]

                    dist = math.hypot(x - tx, z - tz)

                    if dist < self.player.radius + TREE_RADIUS * tree["scale"]:

                        return True,(tx,tz)

                for stone in chunk["stones"]:

                    sx = world_x + stone["x"]
                    sz = world_z + stone["z"]

                    dist = math.hypot(x - sx, z - sz)

                    if dist < self.player.radius + STONE_RADIUS * stone["scale"]:
                        return True, (sx,sz)

        return False,()

    def remove_dead_enemies(self):
        for chunk_key, car_list in self.enemy_cars.items():
            self.enemy_cars[chunk_key] = [e for e in car_list if e.alive]

    def draw_world(self):

        for key, chunk in self.chunks_metadata.items():

            chunk_x = chunk["x"]
            chunk_z = chunk["z"]

            # Convert chunk coordinates to world coordinates
            world_x = chunk_x * CHUNK_SIZE
            world_z = chunk_z * CHUNK_SIZE

            glPushMatrix()

            glTranslatef(
                world_x,
                0,
                world_z
            )

            # -----------------------------
            # Ground
            # -----------------------------

            self.draw_ground()
            self.draw_chunk_border()

            # -----------------------------
            # Draw trees
            # -----------------------------

            for tree in chunk["trees"]:

                glPushMatrix()

                glTranslatef(
                    tree["x"],
                    0,
                    tree["z"]
                )

                glScalef(
                    tree["scale"],
                    tree["scale"],
                    tree["scale"]
                )

                self.draw_tree()

                glPopMatrix()

            # -----------------------------
            # Draw stones
            # -----------------------------

            for stone in chunk["stones"]:

                glPushMatrix()

                glTranslatef(
                    stone["x"],
                    20,
                    stone["z"]
                )

                glScalef(
                    stone["scale"],
                    stone["scale"],
                    stone["scale"]
                )

                self.draw_stone()

                glPopMatrix()

            glPopMatrix()

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

        player = self.player

        if self.pov:

            angle = math.radians(player.angle)
            camera_x = player.x
            camera_y = player.y + 65
            camera_z = player.z

            target_x = camera_x - math.sin(angle) * 100
            target_y = camera_y
            target_z = camera_z - math.cos(angle) * 100

        else:

            angle = math.radians(self.camera_angle)

            camera_x = (player.x + math.sin(angle) * self.camera_distance) + self.arrow[0]
            camera_y = self.camera_height
            camera_z = (player.z + math.cos(angle) * self.camera_distance) + self.arrow[1]

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

    def update_enemies(self):
    
        for car_list in self.enemy_cars.values():

            for enemy in car_list:

                enemy.update(self.player.x, self.player.z)

    def check_bullet_hits(self):
        
        BULLET_HIT_RADIUS = 40 

        for bullet in self.player.bullets:
            if not bullet.alive:
                continue
            for car_list in self.enemy_cars.values():
    
                for enemy in car_list:

                    if not enemy.alive:
                        continue

                    dx = bullet.x - enemy.x
                    dz = bullet.z - enemy.z

                    if math.hypot(dx, dz) < BULLET_HIT_RADIUS:

                        enemy.health -= 25
                        bullet.alive = False

                        if enemy.health <= 0:
                            enemy.alive = False

                        break
        GRENADE_BLAST_RADIUS = 150
        GRENADE_MAX_DAMAGE = 50

        for grenade in self.player.grenades:

            if not grenade.exploded:
                continue

            for car_list in self.enemy_cars.values():

                for enemy in car_list:

                    if not enemy.alive:
                        continue

                    dx = grenade.x - enemy.x
                    dz = grenade.z - enemy.z

                    dist = math.hypot(dx, dz)

                    if dist < GRENADE_BLAST_RADIUS:

                        falloff = 1 - (dist / GRENADE_BLAST_RADIUS)
                        damage = GRENADE_MAX_DAMAGE * falloff
                        print(enemy.health)

                        enemy.health -= damage
                        enemy.alive = enemy.health > 0

        for car_list in self.enemy_cars.values():

            for enemy in car_list:

                for bullet in enemy.bullets:

                    if not bullet.alive:
                        continue

                    dx = bullet.x - self.player.x
                    dz = bullet.z - self.player.z

                    if math.hypot(dx, dz) < BULLET_HIT_RADIUS:

                        self.player.health = max(0, self.player.health - 2)
                        bullet.alive = False

    def draw_enemies(self):

        for car_list in self.enemy_cars.values():
            for enemy in car_list:
                enemy.draw()

    def idle(self):

        self.player.update(self.keys, collision_check=self.check_collision)

        self.update_chunks()
        self.update_enemies()
        self.check_bullet_hits()
        self.remove_dead_enemies()


        angle_diff = self.player.angle - self.camera_angle
        # angle diff & smoothing
        self.camera_angle += angle_diff * self.camera_smoothing

        self.player.wheel_spin_angle += (self.player.speed[2] + angle_diff * self.camera_smoothing)
        glutPostRedisplay()

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

        self.setupCamera()

        self.draw_world()

        self.draw_enemies()
        self.player.show_car()
   

        glutSwapBuffers()

    def specialKeyDown(self, key, x, y):
        self.keys.add(key)

    def specialKeyUp(self, key, x, y):

        if key in self.keys:

            self.keys.remove(key)

    def keyboardListener(self, key, x, y):
        if key == b'q':
            self.pov = not self.pov
        if key== b'a':
            self.arrow[0] -= 20
        if key== b'd':
            self.arrow[0] += 20
        if key == b'w':
            self.arrow[1] += 20
        if key == b's':
            self.arrow[1] -= 20
        if key == b'v':
            self.player.switch_weapon()
        elif key == b'f':
            self.player.fire_bullet()
        


def main():

    CarWarfare()


if __name__ == "__main__":

    main()