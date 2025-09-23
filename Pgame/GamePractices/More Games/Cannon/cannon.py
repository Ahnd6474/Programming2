
# mouse cannon

import pygame, math, random
from pygame.locals import *
from pygame.font import *

from math import sin, cos


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


# ----------------------------------------------------------------

class Shell(pygame.sprite.Sprite):
  
    def __init__(self, cannon):
        super().__init__()
        
        self.image = pygame.Surface( (16,16) )
        self.image.set_colorkey( BLACK )
        pygame.draw.circle(self.image, RED, (8,8), 8)   # red ball
        self.rect = self.image.get_rect()

        self.radAngle = math.pi * cannon.angle / 180.

        barrelLen = cannon.cannonIm.get_width()/2
        self.rect.center = \
            ( cannon.pivot[0] + barrelLen*cos(self.radAngle),
              cannon.pivot[1] - barrelLen*sin(self.radAngle) )

        self.dest = (self.rect.centerx + 1000*cos(self.radAngle), 
                     self.rect.centery - 1000*sin(self.radAngle) )
    
    
    def update(self):
        dist = self.distApart(self.dest, self.rect.center)
        brick = pygame.sprite.spritecollideany(self, bricks)
        if (dist < 5) or (brick is not None) or \
           self.beyondWindow():
            self.kill()
            if brick is not None:
                brick.kill()
        else:
            self.rect = self.rect.move( 15*cos(self.radAngle), 
                                       -15*sin(self.radAngle))


    def beyondWindow(self):
        xc = self.rect.centerx
        yc = self.rect.centery
        return (xc < 0) or (xc > scrWidth-1) or \
               (yc < 0) or (yc > scrHeight-1)
 


    def distApart(self, pt1, pt2):
        return math.sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )



# ----------------------------------------------------------------


def makeBricks():
    y = scrHeight-1
    makeColumn(scrWidth/2, y, 5)
    makeColumn(scrWidth/2+100, y, 5)

    y -= (6*10)
    b = Brick(scrWidth/2, y, 120, 10)
    bricks.add(b)

    makeColumn(scrWidth/2, y, 5)
    makeColumn(scrWidth/2+100, y, 5)

    y -= (6*10)
    b = Brick(scrWidth/2, y, 120, 10)
    bricks.add(b)



def makeColumn(x, y, num):
    width = 20
    height = 10
    y -= height
    for i in  range(num):
        b = Brick(x, y, width, height)
        bricks.add(b)
        y -= height



def drawCrossHairs(screen, pos):
    # draw cross hairs at the mouse pos
    mx = pos[0]
    my = pos[1]
    pygame.draw.line(screen, BLACK, (mx-10, my), (mx+10, my))
    pygame.draw.line(screen, BLACK, (mx, my-10), (mx, my+10))


# ---------- main -------------


pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(SKY_BLUE)
pygame.display.set_caption("Mouse Cannon")

scrWidth, scrHeight = screen.get_size()


# cannon; add Shell(s) later
cannon = Cannon()
shells = pygame.sprite.Group()

# bricks
bricks = pygame.sprite.Group()
makeBricks()

# game vars
isPressed = False
mousePos = (scrWidth/2, scrHeight/2)



clock = pygame.time.Clock()

running = True    
while running:
    clock.tick(30)

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
        if len(shells.sprites()) < 5:   # 5 shells max
            shells.add( Shell(cannon))
        isPressed = False
    shells.update()


    # redraw
    screen.fill(SKY_BLUE)
    bricks.draw(screen)

    shells.draw(screen)
    cannon.draw(screen)

    drawCrossHairs(screen, mousePos)

    pygame.display.update()

pygame.quit()
