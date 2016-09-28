"""AsteroidsGame implemented by Malwina Strenkowska
as a final project for an online course
An Introduction to Interactive Programming in Python
(Rice University via Coursera)"""

"""PLEASE USE GOOGLE CHROME AS A BROWSER! 
Animations slow down in other browsers
CLICK UPPER LEFT BUTTON TO START A PROGRAM (RUN/PLAY)!"""

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
ANGLE_VEL_INC = 0.05
lives = 3 
score = 0
explosion_group = set([])


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    if started == True:
        for item in list(group):
            item.update()
            item.draw(canvas)
            if item.update() == True:
                group.remove(item)
        
def group_collide(group, other_object):
    global explosion_group
    if started == True: 
        for i in list(group):
            if i.collide(other_object) == True:
                group.remove(i)
                an_explosion = Sprite(i.pos, [0,0], 0, 0, explosion_image, explosion_info)
                explosion_group.add(an_explosion)
                explosion_sound.play()
                return True 
        return False
    
            
def group_group_collide(group_1, group_2):
    global score 
    if started == True: 
        for i in list(group_1):        
            if group_collide(group_2, i) == True:
                group_1.discard(i)
                score += 1
                return True
        return False

def reset():
    global lives, score
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0.0, ship_image, ship_info)
    #a_rock = Sprite([WIDTH/3, HEIGHT/3], [1, 1], 0, 0, asteroid_image, asteroid_info)
    rock_groups = set([])
    #a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
    missile_group = set([])
    

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = ship_thrust_sound
        self.angle_velocity_inc = 0
        self.acceleration = 0
#        self.position = [pos[0],pos[1]]
        
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        
        
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.vel[0] -= 0.01*self.vel[0]
        self.vel[1] -= 0.01*self.vel[1]
        
        if self.thrust == True:
            self.acceleration = angle_to_vector(self.angle)
            self.vel[0] += 0.1*self.acceleration[0]
            self.vel[1] += 0.1*self.acceleration[1]
        elif self.thrust == False:
            self.acceleration = 0                   
       
        self.angle += self.angle_vel
        
    def ship_ang_inc(self):
        self.angle_vel += ANGLE_VEL_INC
   
    def ship_ang_dec(self):
        self.angle_vel -= ANGLE_VEL_INC
    
    def stop_rotations(self):
        self.angle_vel = 0
      
    def thrust_on(self):
        self.thrust = True
        self.sound.play()
        
    def thrust_off(self):
        self.thrust = False
        self.sound.rewind()
    
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0] + self.radius * forward[0],
                            self.pos[1] + self.radius * forward[1]],
                           [self.vel[0] + 6*angle_to_vector(self.angle)[0], self.vel[1] + 6*angle_to_vector(self.angle)[1]],
                           self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos

        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()        
   
    def draw(self, canvas):
        if self.animated == True:
            EXPLOSION_DIM = 24
            explosion_index = self.age % EXPLOSION_DIM // 1
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index * self.image_size[0], self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)
            self.age += 1
        else:            
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0])%WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1])%HEIGHT
        self.vel[0] += 0.001*score
        self.vel[1] += 0.001*score
        
        self.angle += self.angle_vel
        self.age += 0.2
        if self.age < self.lifespan:
            return False
        else:
            return True
        
                                     
    def collide(self, other_object):
        center_1 = other_object.get_position()
        center_2 = self.get_position()
        radius_1 = other_object.get_radius()
        radius_2 = self.get_radius()
        if dist(center_1, center_2) < (radius_1 + radius_2):
            return True
        return False
        
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos


           
def draw(canvas):
    global time, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_groups, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    
    # update after collisions 
    group_group_collide(missile_group, rock_groups)
    if group_collide(rock_groups, my_ship) == True:
        if lives > 0:
            lives -= 1
            return lives
        else:
            started = False
            timer.stop()
            reset()
            soundtrack.rewind()
    

    
    # user interface
    canvas.draw_text("LIVES", [WIDTH/15, HEIGHT/9], 30, 'White', 'sans-serif')
    canvas.draw_text("SCORE", [12*WIDTH/15, HEIGHT/9], 30, 'White', 'sans-serif')
    canvas.draw_text(str(lives), [WIDTH/15, HEIGHT/6], 30, 'White', 'sans-serif')
    canvas.draw_text(str(score), [12*WIDTH/15, HEIGHT/6], 30, 'White', 'sans-serif')      

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        canvas.draw_text("implementation of Asteroids game by Malwina Strenkowska - final project for An Introduction to Interactive Programming in Python course, Coursera, 2015",
                     [45, HEIGHT-20], 10, 'White', 'sans-serif')
    
    
    
    
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.ship_ang_dec()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.ship_ang_inc()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on()        
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    global angle_velocity_inc
    if key == simplegui.KEY_MAP["left"]:
        my_ship.stop_rotations()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.stop_rotations()
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_off()       
        

        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()
        timer.start()
    
        
        
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = Sprite([random.randrange(0, WIDTH), random.randrange(0, HEIGHT)], [random.random() * 0.6 - 0.3, random.random() * 0.6 - 0.3], 0, random.random()*0.2 - 0.1 , asteroid_image, asteroid_info)
    if len(rock_groups) < 12 and a_rock.collide(my_ship) == False:
        rock_groups.add(a_rock)
   
        

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0.0, ship_image, ship_info)
#a_rock = Sprite([WIDTH/3, HEIGHT/3], [1, 1], 0, 0, asteroid_image, asteroid_info)
rock_groups = set([])
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
