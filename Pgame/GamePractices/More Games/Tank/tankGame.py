
import pygame, random, math
from pygame.locals import *
from pygame.font import *

from math import sin, cos


# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)
YELLOW =( 255, 255,   0)


WALL_SIZE = 20

# player moves
NONE = 0
FORWARD = 1
BACKWARD = 2
CW = 3   # clockwise
CCW = 4  # counter clockwise


# 20 x 15, scaled later to be 640 x 480 pixels
walls_map =\
["....................",
 ".....x..............",
 ".....xxxxxx.........",
 "..........x.........",
 "....................",
 "..........x.........",
 "..........xxxx......",
 "....................",
 "..........xxxx......",
 "..........x.........",
 "..........x.........",
 "..........x.........",
 "..........xxxxxxxxx.",
 "...............x....",
 "...................."]

  
 
class BlockSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



# --------------------------------------------------


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([8, 8])  # size is 8 x 8
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()


# ----------------------------------------------------------------



class AnimSprite(pygame.sprite.Sprite):

    def __init__(self, fnm, numPics):
        # assume that sheet in fnm is a single column of numPics pics
        super().__init__()
        self.sheet = pygame.image.load(fnm).convert_alpha()
        self.numPics = numPics
        self.frameHeight = self.sheet.get_height()/numPics
        self.isVisible = False
        self.isRepeating = False
        self.frameNo = 0
        self.image = self.sheet.subsurface(0,
                            self.frameNo * self.frameHeight,
                            self.sheet.get_width(),
                            self.frameHeight)
        self.rect = self.image.get_rect()


    def setVisible(self, isVisible):
        self.isVisible = isVisible

    def setRepeating(self, isRepeating):
        self.isRepeating = isRepeating

    def setPosition(self, pos):
        self.rect.center = pos

    def draw(self, screen):
        if self.isVisible:
           screen.blit(self.image, [self.rect.x, self.rect.y])
           self.frameNo = (self.frameNo + 1) % self.numPics
           self.image = self.sheet.subsurface(0,
                            self.frameNo * self.frameHeight,
                            self.sheet.get_width(),
                            self.frameHeight)
           if self.frameNo == 0 and not self.isRepeating:
               self.isVisible = False



# -------------------------------------------------------

class Tank(pygame.sprite.Sprite):

    def __init__(self, map):
        super().__init__()
        
        self.origIm = pygame.image.load('tank.png').convert_alpha()
        self.image = self.origIm
        self.rect = self.image.get_rect()
        self.rect.topleft = findSpace(map)
        self.origIm = pygame.transform.rotate(self.origIm, -90)
        
        ss = pygame.display.get_surface()
        self.size = ss.get_width(), ss.get_height()
        
        self.step = 6       # linear pixels per frame
        self.rotStep = 3    # degrees rotated per frame
        self.angle = 90     # degrees (it starts facing up)


    
    def update(self, move):
        oldAngle = self.angle
        oldCenter = self.rect.center

        radAngle = math.pi * self.angle / 180.

        if move == FORWARD:
            self.rect = self.rect.move(self.step * cos(radAngle), \
                                      -self.step * sin(radAngle))
        elif move == BACKWARD: 
            self.rect = self.rect.move(-self.step * cos(radAngle), \
                                       self.step * sin(radAngle))
        elif move == CW:   # rotate clockwise
            self.angle -= self.rotStep
        elif move == CCW:  # rotate counter clockwise
            self.angle += self.rotStep

        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360

        if oldAngle != self.angle:
            currCenter = self.rect.center
            self.image = pygame.transform.rotate(self.origIm, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = currCenter
        

        ratio = pygame.sprite.collide_circle_ratio(0.7)
        if pygame.sprite.spritecollide(self, walls, False, ratio) or \
           pygame.sprite.spritecollideany(self, sides):  # reset old pos/angle
            self.image = pygame.transform.rotate(self.origIm, oldAngle)
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter
            self.angle = oldAngle


    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ----------------------------------------------------------------


class Shell(pygame.sprite.Sprite):
  
    def __init__(self, player):
        super().__init__()
        
        self.image = pygame.Surface( (10,10) )  # red ball image
        self.image.set_colorkey( BLACK )
        pygame.draw.circle(self.image, RED, (5,5), 5)
        self.rect = self.image.get_rect()

        self.rect.center = player.rect.center
        self.radAngle = math.pi * player.angle / 180.

        self.dest = (player.rect.centerx + 300*cos(self.radAngle), 
                     player.rect.centery - 300*sin(self.radAngle) )
    
    
    def update(self):
        dist = self.distApart(self.dest, self.rect.center)
        brick = pygame.sprite.spritecollideany(self, walls)
        if dist < 5 or pygame.sprite.spritecollideany(self, sides) or \
                       brick is not None:
            self.kill()
            if brick is not None:
                brick.kill()
            shellExplo.setPosition(self.rect.center)
            shellExplo.setVisible(True)
            explosion.play()
        else:
            self.rect = self.rect.move( 8*cos(self.radAngle), 
                                       -8*sin(self.radAngle))



    def distApart(self, pt1, pt2):
        return math.sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )


# ----------------------------------------------------------------


def readMap(map):
    for y, row in enumerate(map):
        for x, ch in enumerate(row):
            if ch == 'x':
                makeBricks(x, y)


def makeBricks(xStart, yStart):
    # the map is 20 x 15 (x,y), scaled x32 to be 640 x 480 pixels
    # so make 4 x 4 bricks for each 'x'
    # since each brick is 8x8 pixels
    for x in range(4):
        for y in range(4):
            b = Brick()
            b.rect.x = (xStart*4 + x) * b.rect.width
            b.rect.y = (yStart*4 + y) * b.rect.height
            walls.add(b)


def findSpace(map):
  while True:
      x = random.randint(0, 19)   # map is 20 x 15
      y = random.randint(0, 14)
      if isSpace(map, x, y):
          return (x*32, y*32)  # scale by x32



def isSpace(map, x, y):
    row = map[y]
    return list(row)[x] == '.'



def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))



# -----------------------------------------------------------
# main

pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(DARKGREEN)
pygame.display.set_caption("Tank")

scrWidth, scrHeight = screen.get_size()


# Load music and other sounds
# pygame.mixer.music.load("music1.ogg") 
# pygame.mixer.music.play(-1)   # Play forever

explosion = pygame.mixer.Sound("shell.ogg")         


# create wall sprites flush with sides
top    = BlockSprite(0, -WALL_SIZE, scrWidth, WALL_SIZE)
bottom = BlockSprite(0, scrHeight, scrWidth, WALL_SIZE)
left   = BlockSprite(-WALL_SIZE, 0, WALL_SIZE, scrHeight)
right  = BlockSprite(scrWidth, 0, WALL_SIZE, scrHeight)

sides = pygame.sprite.Group(top, bottom, left, right)


# player related sprites (add Shell(s) later)
player = Tank(walls_map)
shells = pygame.sprite.Group()

# create explosion sprites
shellExplo = AnimSprite('exploSheet.png', 9)

walls = pygame.sprite.Group()
readMap(walls_map)


# game vars
winMsg = ""
gameOver = False
move = NONE

font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()

running = True    
while running:
    clock.tick(50)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
    
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                  if len(shells.sprites()) < 5:   # 5 shells max
                      shells.add( Shell(player))
            elif event.key == K_UP or event.key == K_w:
                move = FORWARD 
            elif event.key == K_DOWN or event.key == K_s:
                move = BACKWARD 
            elif event.key == K_LEFT or event.key == K_a:
                move = CCW 
            elif event.key == K_RIGHT or event.key == K_d:
                move = CW 

        elif event.type == KEYUP:
            move = NONE


    # update game
    if not gameOver:
        player.update(move)
        shells.update()
        

    # redraw
    screen.fill(DARKGREEN)     

    walls.draw(screen);
    player.draw(screen)
    shells.draw(screen)

    shellExplo.draw(screen)

    if gameOver:
        centerImage(screen, font.render(winMsg, True, RED))

    pygame.display.update()

pygame.quit()




