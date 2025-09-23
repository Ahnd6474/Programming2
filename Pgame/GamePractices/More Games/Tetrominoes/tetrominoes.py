
# Tetrominoes (a Tetris clone)
# based on code by Al Sweigert in Ch 7 of
# "Making Games with Python and Pygame"


import random, time, pygame, sys
from pygame.locals import *

from TetBoard import TetBoard
from TetPiece import TetPiece


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOXSIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20


# slow down key repeats
KEY_FREQ = 0.1  # in secs


# colors        R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)


# -------------------------------------------------------------------------

def centerText(screen, msg):
    im = font.render(msg, True, WHITE)
    centerImage(screen, im)


def centerImage(screen, im):
    x = (WINDOW_WIDTH-im.get_width())/2
    y = (WINDOW_HEIGHT-im.get_height())/2
    screen.blit(im, (x,y))


def midText(screen, msg, y):
    im = font.render(msg, True, WHITE)
    midImage(screen, im, y)


def midImage(screen, im, y):
    x = (WINDOW_WIDTH-im.get_width())/2
    screen.blit(im, (x,y))



def calcLevelAndDown(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a piece moves down one space.
    level = int(score/10) + 1
    downFreq = 0.27-(level * 0.02)
    return level, downFreq



def drawStatus(screen, score, level):
    # draw the score abd level values
    scoreIm = font.render('Score: %s' % score, True, WHITE)
    screen.blit(scoreIm, (WINDOW_WIDTH-190, 20))

    levelIm = font.render('Level: %s' % level, True, WHITE)
    screen.blit(levelIm, (WINDOW_WIDTH-190, 70))



# ----------------------------------------------

# main


pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetromino')

font = pygame.font.Font('freesansbold.ttf', 36)
bigFont = pygame.font.Font('freesansbold.ttf', 100)


# load game music
if random.randint(0, 1) == 0:
    pygame.mixer.music.load('tetrisb.mid')
else:
    pygame.mixer.music.load('tetrisc.mid')
pygame.mixer.music.play(-1, 0.0)


# create game objects
board = TetBoard()
p = TetPiece()



# game vars

moveDir = 0    # -1 means left; 1 means right
rotDir = 0     # -1 mean CCW (to left); 1 mean CW (to right)
dropDist = 0   # 1 means drop 1 space; 2 means drop to bottom

showStartScreen = True
isPaused = False
gameOver = False
showHelp = False

score = 0
level, downFreq = calcLevelAndDown(score)
lastDownTime = time.time()   # time returned in seconds
lastKey = time.time()

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

            elif event.key == K_p:
                isPaused = not isPaused   # toggle
            elif event.key == K_h:
                showHelp = not showHelp   # toggle
                isPaused = showHelp

            elif event.key == K_LEFT or event.key == K_a:
                moveDir = -1
            elif event.key == K_RIGHT or event.key == K_d:
                moveDir = 1
            elif event.key == K_UP or event.key == K_w:
                rotDir = 1
            elif event.key == K_q:
                rotDir = -1
            elif event.key == K_DOWN or event.key == K_s:
                dropDist = 1
            elif event.key == K_SPACE:
                if showStartScreen:
                    showStartScreen = False
                else:
                    dropDist = 2

        elif event.type == KEYUP:
            moveDir = 0; rotDir = 0
            dropDist = 0



    # --------------- update game -------------------------

    if not board.isValidPos(p):
       gameOver = True   # can't fit piece on board, so game over


    if not showStartScreen and not gameOver and not isPaused:

        # let the user do something if enough time has passed
        if (time.time()-lastKey > KEY_FREQ):  # time-constraint

            # move the piece sideways
            if (moveDir != 0):
                if moveDir < 0 and board.isValidPos(p, -1, 0):
                    p.xMove(-1)
                elif moveDir > 0 and board.isValidPos(p, 1, 0):
                    p.xMove(1)


            # rotate the piece if there's room
            if rotDir > 0:
                p.rotateRight()
                if not board.isValidPos(p):
                    p.rotateLeft()
            elif rotDir < 0:
                p.rotateLeft()
                if not board.isValidPos(p):
                    p.rotateRight()


            # make the piece fall faster
            if dropDist == 1:
                if board.isValidPos(p, 0, 1):
                        p.moveDown(1)
            elif dropDist > 1:
                for i in range(1, BOARD_HEIGHT):
                    if not board.isValidPos(p, 0, i):
                        break
                p.moveDown(i-1)

            lastKey = time.time()  # record key time


        # move the piece move down 1 space if it's time
        if (time.time()-lastDownTime > downFreq):  # time-constraint
            if not board.isValidPos(p, 0, 1):
                # piece has landed, so add to the board
                board.add(p)
                score += board.removeCompleteLines()
                level, downFreq = calcLevelAndDown(score)
                p = TetPiece()    # start next piece
                lastKey = time.time()    # reset key time
            else: # did not land, just move the piece down
                p.moveDown(1)

            lastDownTime = time.time()   # record move time



    # ----------------- redraw game ---------------------------

    screen.fill(BLACK)

    if showStartScreen:
        midText(screen, "Tetrominoes!", 120)
        midText(screen, "Press space to play", 191)

    else:
        board.draw(screen)
        drawStatus(screen, score, level)

        if gameOver:
            centerText(screen, "Game Over")
        elif isPaused:
            if showHelp:
                centerText(screen, "Use the arrow keys")
            else:
                centerText(screen, 'Paused...')
        else:
            p.draw(screen)

    pygame.display.update()


pygame.mixer.music.stop()
pygame.quit()


