
# skier.py
# Listing_10-1.py
# Skier program

import pygame, sys, random
from pygame.locals import *

# colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = (   0,   0, 255)
YELLOW =( 255, 255,   0)


SKIER_STEP = 6


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


    def update(self, step):
        # movement function needed since using AnimSprite in a top-scroller
        if self.rect.y > 0:   # if below top of window
            self.rect.y -= step    # move up
        else:
            self.setVisible(False)



# --------------------------------------------------



class PicsSprite(pygame.sprite.Sprite):

    def __init__(self, fnms):
        super().__init__() 
        self.images = []
        for fnm in fnms:
           self.images.append( pygame.image.load(fnm + ".png").convert_alpha() )
        self.image = self.images[0]
        self.rect = self.image.get_rect()


    def setPic(self, idx):
        center = self.rect.center
        self.image = self.images[idx]
        self.rect = self.image.get_rect()
        self.rect.center = center


# --------------------------------------------------



class Button(pygame.sprite.Sprite):

    def __init__(self, label, pos):
        super().__init__() 
        self.image = pygame.image.load("button.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        font = pygame.font.Font(None, 24)
        self.labelIm = font.render(label, True, YELLOW)
        self.labelRect = self.labelIm.get_rect()
        self.labelRect.x = self.rect.x + \
                      (self.rect.width - self.labelIm.get_width())/2
        self.labelRect.y = self.rect.y + \
                      (self.rect.height - self.labelIm.get_height())/2


    def isPressed(self, mousePos):
        return self.rect.collidepoint(mousePos)
    

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.labelIm, self.labelRect)
        

# --------------------------------------------------


class Skier(PicsSprite):

    def __init__(self, x):
        super().__init__(["down", "right1", "right2", "left2", "left1"]) 
        self.rect.center = [x, 100]
        self.initSpeed()


    def initSpeed(self):
        self.steps = [0, SKIER_STEP]
        self.setPic(0)


    def turn(self, dirChange):
        dir = self.steps[0] + dirChange
        if dir < -2:  # restrict direction to -2 to 2
            dir = -2
        if dir >  2:  
            dir =  2
        self.steps = [dir, SKIER_STEP - abs(dir)*2]
        self.setPic(dir)


    def move(self):
        # move the skier right and left
        self.rect.centerx += self.steps[0]
        if self.rect.x < 0:       # stay visible
            self.rect.x = 0
        if self.rect.x > (scrWidth - self.rect.width): 
            self.rect.x = scrWidth - self.rect.width


# --------------------------------------------------


# class for obstacle sprites (trees and flags)
class Obstacle(pygame.sprite.Sprite):

    def __init__(self, fnm, loc):
        super().__init__() 
        self.fnm = fnm
        self.image = pygame.image.load(fnm)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        self.isPassed = False


    def update(self, step):
        self.rect.y -= step
        if self.rect.y < -self.rect.height:  # if above top
            self.kill()



# --------------------------------------------------


def makeObstacles():
    # create trees/flags at random positions off the 
    # bottom of the screen
    locs = []
    for i in range(10):  # 10 obstacles
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        loc  = [(col * scrWidth/10) + 32, (row * scrWidth/10) + 32 + scrHeight] 
               # (x,y) center for an obstacle
        if not (loc in locs):  # prevent 2 obstacles from being in the same place
            locs.append(loc)
            type = random.choice(["tree", "flag"])
            if type == "tree":
                obstacles.add( Obstacle("tree.png", loc) )
            else:    # a flag
                obstacles.add( Obstacle("flag.png", loc) )



def checkCollisions():
    global score
    hits =  pygame.sprite.spritecollide(skier, obstacles, False)
    if hits:
        if not hits[0].isPassed:
            explo.setPosition( hits[0].rect.center )
            explo.setVisible(True)
            boom.play()
            hits[0].isPassed = True

            if hits[0].fnm == "tree.png":  # hit a tree
                score -= 10
                skier.initSpeed()
            else:   # hit a flag
                score += 10
                hits[0].kill() # remove the flag




def isGameOver():
    global finalMsg
    if score < -90:
        finalMsg = "Game Over! You lost"
        return True
    elif score > 90:
        finalMsg = "Game Over! You won"
        return True
    else:
        return False


def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))


# ----------------------------------------------

# main

pygame.init()
screen = pygame.display.set_mode([640, 640])
pygame.display.set_caption('Skier')
scrWidth, scrHeight = screen.get_size()

font = pygame.font.Font(None, 50)

# load game sounds
pygame.mixer.music.load('arpanauts.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

boom = pygame.mixer.Sound('boom.wav')

# game vars
isPaused = False
showHelp = False
gameOver = False
finalMsg = ""
score = 0

# create sprites
skier = Skier(scrWidth/2)

yLandPos = 0   # y position of skier on the land

# create explosion sprites
explo = AnimSprite('exploSheet.png', 10)

# create obstacles
obstacles = pygame.sprite.Group()   # group of obstacle objects
makeObstacles() 


button = Button("Help", (scrWidth-80, 40))
instructions = pygame.image.load("instructions.png").convert_alpha()


clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if button.isPressed( pygame.mouse.get_pos() ):
                # print('button pressed')
                showHelp = not showHelp    # toggle
                isPaused = showHelp

        if event.type == KEYDOWN:
            if event.key == K_p: 
                isPaused = not isPaused   # toggle
            elif event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:        # left arrow turns left
                skier.turn(-1)
            elif event.key == K_RIGHT:     # right arrow turns right
                skier.turn(1)

    # update game
    if not gameOver and not isPaused:
        skier.move() 
        
        # create new obstacles if skier is at end of old obstacles
        yLandPos += skier.steps[1]
        if yLandPos >= scrHeight:
            makeObstacles()
            yLandPos = 0
        
        checkCollisions()
        
        # update obstacles and explosion based on skier's y 'movement'
        obstacles.update( skier.steps[1] )
        explo.update(skier.steps[1] )
        
        gameOver = isGameOver()


    # redraw game
    screen.fill(WHITE)
    button.draw(screen)

    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    explo.draw(screen)

    screen.blit(font.render("Score: " +str(score), 1, BLACK), [10, 10])
    if gameOver:
        centerImage(screen, font.render(finalMsg, True, RED))
    elif isPaused:
        if showHelp:
            centerImage(screen, instructions)
        else:
            centerImage(screen, font.render('Paused...', True, BLACK))

    pygame.display.update()

pygame.quit()
