
# mouse cannon

import pygame, math, random
from pygame.locals import *
from pygame.font import *

from math import sin, cos

import pymunk as pm



# set up a bunch of constants
# some colors
BLACK = (   0,   0,   0)
DARKGRAY = (128, 128, 128)
WHITE = ( 255, 255, 255)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)
SKY_BLUE = (135, 206, 250)
YELLOW =( 255, 255,   0)


WALL_SIZE = 20

# cannon coordinates
X_OFFSET = 30      # of the left edge of the cannon base
BASE_RADIUS = 40   # of gray circle acting as the cannon's base


# ----------------------------------------------------------------


class Cannon(pygame.sprite.Sprite):
    # no pymunk changes

    def __init__(self):
        self.cannonIm = pygame.image.load("gun.png").convert_alpha()
        self.pivot = (X_OFFSET + BASE_RADIUS, 
                      scrHeight - 1 - BASE_RADIUS)
        self.angle = 0
        self.aimCannon()


    def aimCannon(self):
        # rotate the cannon image around the pivot
        self.image = pygame.transform.rotate(self.cannonIm, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pivot



    def update(self, mPos):
        # set angle between the cannon and mouse pos
        yDiff = self.rect.centery - mPos[1] 
        xDiff = mPos[0] - self.rect.centerx 
        self.angle = math.atan2(yDiff, xDiff)*180./math.pi
        # print(int(self.angle))
        self.aimCannon()
    
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # the base is a gray semi-circle with a black border
        # resting on the floor
        pygame.draw.circle(screen, DARKGRAY, 
            (X_OFFSET + BASE_RADIUS, scrHeight-1), BASE_RADIUS)   
        pygame.draw.circle(screen, BLACK, 
            (X_OFFSET + BASE_RADIUS, scrHeight-1), BASE_RADIUS, 1)   





# ----------------------------------------------------------------

class Brick(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(DARKGRAY)
        pygame.draw.rect(self.image, WHITE, (0,0,width,height), 1) # white border
        self.rect = self.image.get_rect()
        xc = x + width/2
        yc = y + height/2
        self.rect.center = (xc,yc)

        # pymunk box 
        points = [(-width/2, -height/2), (-width/2, height/2), 
                  (width/2, height/2), (width/2, -height/2)]
        mass = (width * height)/2
        moment = pm.moment_for_poly(mass, points, (0,0))
        # print(moment)
        body = pm.Body(mass, moment)
        body.position = toPymunk([xc, yc])

        shape = pm.Poly(body, points, (0,0))
        shape.friction = 0.6
        space.add(body, shape)
        self.shape = shape   # save pymunk shape



    def draw(self, screen):
        pos = toPygame(self.shape.body.position)
        self.rect.center = pos
        screen.blit(self.image, self.rect)


# ----------------------------------------------------------------

class Shell(pygame.sprite.Sprite):
  
    def __init__(self, cannon):
        super().__init__()
        
        radius = 8
        self.image = pygame.Surface( (radius*2,radius*2) )
        self.image.set_colorkey( BLACK )
        pygame.draw.circle(self.image, RED, (radius,radius), radius)   # red ball
        self.rect = self.image.get_rect()

        self.radAngle = math.pi * cannon.angle / 180.
        barrelLen = cannon.cannonIm.get_width()/2
        self.rect.center = \
            ( cannon.pivot[0] + barrelLen*cos(self.radAngle),
              cannon.pivot[1] - barrelLen*sin(self.radAngle) )

        # pymunk physics
        mass = radius*3
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, 8)
        body.position = toPymunk(self.rect.center)

        impulse = 10000 * pm.Vec2d(1,0)
        body.apply_impulse(impulse.rotated(self.radAngle))

        shape = pm.Circle(body, radius, (0,0))
        space.add(body, shape)
        self.shape = shape   # save pymunk shape


    def hasStopped(self):
        vel = self.shape.body.velocity
        smallVel = 1e-6
        return (vel.x < smallVel and vel.y < smallVel)


    def draw(self, screen):
        pos = toPygame(self.shape.body.position)
        self.rect.center = pos
        screen.blit(self.image, self.rect)


# ----------------------------------------------------------------


def makeBricks():   # replaced group by bricks list
    y = scrHeight-1
    makeColumn(scrWidth/2, y, 5)
    makeColumn(scrWidth/2+100, y, 5)

    y -= (6*10)
    b = Brick(scrWidth/2, y, 120, 10)
    bricks.append(b)

    makeColumn(scrWidth/2, y, 5)
    makeColumn(scrWidth/2+100, y, 5)

    y -= (6*10)
    b = Brick(scrWidth/2, y, 120, 10)
    bricks.append(b)



def makeColumn(x, y, num):
    width = 20
    height = 10
    y -= height
    for i in  range(num):
        b = Brick(x, y, width, height)
        bricks.append(b)
        y -= height



def deleteStoppedShell(shells):
    # remove any shell that has stopped moving
    for s in shells:
        # print(s.shape.body.velocity)
        if s.hasStopped():
            shells.remove(s)
            space.remove(s.shape.body, s.shape)
            return


def drawCrossHairs(screen, pos):
    # draw cross hairs at the mouse pos
    mx = pos[0]
    my = pos[1]
    pygame.draw.line(screen, BLACK, (mx-10, my), (mx+10, my))
    pygame.draw.line(screen, BLACK, (mx, my-10), (mx, my+10))


# y- coordinate translation between modules

def toPygame(pos):
    return int(pos.x), int(scrHeight-pos.y)


def toPymunk(pt):
    return int(pt[0]), int(scrHeight-pt[1])


# ---------- main -------------


pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(SKY_BLUE)
pygame.display.set_caption("Mouse Cannon")

scrWidth, scrHeight = screen.get_size()


# initialize pymunk space
space = pm.Space()
gravity = -100.0    # down
space.gravity = (0.0, gravity)



# the sides in pymunk coords
sides = \
  [  pm.Segment(space.static_body, (0, -WALL_SIZE/2-1), 
                      (scrWidth-1, -WALL_SIZE/2-1), WALL_SIZE),   # floor

     pm.Segment(space.static_body, (0, scrHeight+WALL_SIZE/2), 
                      (scrWidth-1, scrHeight+WALL_SIZE/2), WALL_SIZE), # top

     pm.Segment(space.static_body, (-WALL_SIZE/2, 1), 
                      (-WALL_SIZE/2, scrHeight-2), WALL_SIZE),   # left

     pm.Segment(space.static_body, (scrWidth-2+WALL_SIZE/2, 0), 
                       (scrWidth-2+WALL_SIZE/2, scrHeight-2), WALL_SIZE)  # right
  ]  

for s in sides:
    s.elasticity = 0.2 
    s.friction = 0.8

sides[0].elasticity = 0


space.add(sides)


# cannon; add Shell(s) later
cannon = Cannon()
shells = []

# bricks
bricks = []
makeBricks()

# game vars
isPressed = False
mousePos = (scrWidth/2, scrHeight/2)


clock = pygame.time.Clock()
FPS = 30

running = True    
while running:
    clock.tick(FPS)
    space.step(1./FPS)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN:
            isPressed = True



    # update game
    cannon.update(mousePos)

    if isPressed:
        if len(shells) < 5:   # 5 shells max
            shells.append( Shell(cannon))
        isPressed = False

    deleteStoppedShell(shells)


    # redraw
    screen.fill(SKY_BLUE)
    for b in bricks:
        b.draw(screen)

    for s in shells:
        s.draw(screen)

    cannon.draw(screen)

    drawCrossHairs(screen, mousePos)

    pygame.display.update()

pygame.quit()
