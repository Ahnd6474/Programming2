
# BadDay.py


import pygame
from pygame.locals import *

from Fred import Fred
from Barrel import Barrel


# colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = (   0,   0, 255)
YELLOW =( 255, 255,   0)

MAX_BARREL_SEP_TIME = 500


# --------------------------------------------------



def updateBarrels(currTime):
    global barrelsList, prevBarrelTime

    # make a new barrel if enough time has passed
    if currTime - prevBarrelTime > barrelTimeSep:
        barrelsList.append(Barrel())
        prevBarrelTime = currTime


    # move all barrels and note if they need deleting
    delIndicies = []
    for idx, barrel in enumerate(barrelsList):
        barrel.move()

        if not barrel.isBroken:
            if pygame.sprite.collide_rect(barrel, fred):
                barrel.split()
                fred.hit(currTime)

        if barrel.rect.y > scrHeight:
            delIndicies.append(idx)

    # delete barrels in reverse order by indicies
    indexes = sorted(delIndicies, reverse=True)
    for index in indexes:
        del barrelsList[index]



# --------------------------------------------------

# main

pygame.init()
screen = pygame.display.set_mode([1000,768], pygame.FULLSCREEN)
pygame.display.set_caption('fred\'s Bad Day')
scrWidth, scrHeight = screen.get_size()
# print(scrWidth, " ", scrHeight)

font = pygame.font.SysFont("monospace", 50)


# load images
startScreen = pygame.image.load("assets/startgame.png")
endScreen = pygame.image.load("assets/gameover.png")
background = pygame.image.load("assets/background.png")


# load background music; set volume
pygame.mixer.music.load("assets/mi.mp3") 
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)   # Play forever



# game vars
showStartScreen = True
startTime = 0
gameFinishedTime = 0
gameOver = False

# barrels vars
barrelsList = []
prevBarrelTime = 0
barrelTimeSep = MAX_BARREL_SEP_TIME

dir = 0   # -1 means left, 1 means right

# create sprites
fred = Fred(scrWidth, scrHeight)


clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    # ---------------- handle events -------------------------------

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT or event.key == K_a:
                dir = -1
            elif event.key == K_RIGHT or event.key == K_d:
                dir = 1

            elif event.key == K_RETURN:
                if showStartScreen:
                    showStartScreen = False
                    startTime = pygame.time.get_ticks()
                elif gameOver:   # to restart the game
                    gameOver = False
                    fred.reset()
                    barrelsList = []
                    barrelTimeSep = MAX_BARREL_SEP_TIME
                    startTime = pygame.time.get_ticks()

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_a or \
               event.key == K_RIGHT or event.key == K_d:
                dir = 0




    # --------------- update game -------------------------

    if not showStartScreen and not gameOver:

        currTime = pygame.time.get_ticks()

        updateBarrels(currTime)

        if fred.health <= 0:
            gameOver = True
            gameFinishedTime = int((currTime - startTime)/1000)

        fred.move(dir, currTime)



    # ----------------- redraw game ---------------------------

    screen.fill(BLACK)

    if showStartScreen:
        screen.blit(startScreen, (0, 0))

    elif gameOver:
        screen.blit(endScreen, (0, 0))
        screen.blit(font.render(str(gameFinishedTime), True, BLUE), (495, 430))

    else:   # in the middle of the game
        screen.blit(background, (0, 0))

        fred.draw(screen)

        for idx, barrel in enumerate(barrelsList):
            barrel.draw(screen)

        # health bar
        pygame.draw.rect(screen, YELLOW,
            (0, scrHeight-10, (scrWidth/100)*fred.health, 10))


    pygame.display.update()

pygame.quit()


