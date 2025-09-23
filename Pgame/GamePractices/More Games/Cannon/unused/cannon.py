
# mouse cannon

import pygame, math
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
BROWN = (139,  69,  19)


WALL_SIZE = 20



class BlockSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


# ----------------------------------------------------------------

class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([8, 8])  # size is 8 x 8
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()



# ----------------------------------------------------------------

class Shell(pygame.sprite.Sprite):
  
    def __init__(self, center, angle):
        super().__init__()
        
        self.image = pygame.Surface( (16,15) )  # red ball image
        self.image.set_colorkey( BLACK )
        pygame.draw.circle(self.image, RED, (8,8), 8)
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.radAngle = math.pi * angle / 180.

        self.dest = (center[0] + 300*cos(self.radAngle), 
                     center[1] - 300*sin(self.radAngle) )
    
    
    def update(self):
        dist = self.distApart(self.dest, self.rect.center)
        brick = pygame.sprite.spritecollideany(self, bricks)
        if dist < 5 or pygame.sprite.spritecollideany(self, sides) or \
                       brick is not None:
            self.kill()
            if brick is not None:
                brick.kill()
            explosion.play()
        else:
            self.rect = self.rect.move( 12*cos(self.radAngle), 
                                       -12*sin(self.radAngle))



    def distApart(self, pt1, pt2):
        return math.sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )



# ----------------------------------------------------------------


def rotateCenter(im, angle):
    # rotate a square image while keeping its center and size
    origRect = im.get_rect()
    rotIm = pygame.transform.rotate(im, angle)
    rotRect = origRect.copy()
    rotRect.center = rotIm.get_rect().center
    rotIm = rotIm.subsurface(rotRect).copy()
    return rotIm


def getAngle(imCenter, mPos):
    # Return degree angle between im and mouse pos in range 0-360
    yDiff = imCenter[1] - mPos[1] 
    xDiff = mPos[0] - imCenter[0] 
    angle = math.atan2(yDiff, xDiff)*180/math.pi
    # print(int(angle))
    return angle


def makeBricks(xStart, yStart):
    for x in range(4):
        for y in range(4):
            b = Brick()
            b.rect.x = xStart + (x * b.rect.width)
            b.rect.y = yStart + (y * b.rect.height)
            bricks.add(b)



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


explosion = pygame.mixer.Sound("shell.ogg")         


# create wall sprites flush with sides
top    = BlockSprite(0, -WALL_SIZE, scrWidth, WALL_SIZE)
bottom = BlockSprite(0, scrHeight, scrWidth, WALL_SIZE)
left   = BlockSprite(-WALL_SIZE, 0, WALL_SIZE, scrHeight)
right  = BlockSprite(scrWidth, 0, WALL_SIZE, scrHeight)

sides = pygame.sprite.Group(top, bottom, left, right)


# player related sprites (add Shell(s) later)
cannonIm = pygame.image.load("gun.png").convert_alpha()
wheelIm = pygame.image.load("wheel.png").convert_alpha()
cannonPos = (30 + wheelIm.get_width()/2, scrHeight - wheelIm.get_height())

shells = pygame.sprite.Group()


# bricks
bricks = pygame.sprite.Group()
makeBricks(scrWidth/2, scrHeight/2)

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
    angle = getAngle(cannonPos, mousePos)

    # rotate a copy of the cannon image
    rotatedIm = rotateCenter(cannonIm, angle)
    rect = rotatedIm.get_rect()
    rect.center = cannonPos

    if isPressed:
        if len(shells.sprites()) < 5:   # 5 shells max
            shells.add( Shell(cannonPos, angle))
        isPressed = False

    shells.update()

    # redraw
    screen.fill(SKY_BLUE)
    bricks.draw(screen);

    shells.draw(screen)

    screen.blit(rotatedIm, rect)  # draw rotated cannon
    screen.blit(wheelIm, (30, scrHeight-wheelIm.get_height()) )

    drawCrossHairs(screen, mousePos)

    pygame.display.update()

pygame.quit()
