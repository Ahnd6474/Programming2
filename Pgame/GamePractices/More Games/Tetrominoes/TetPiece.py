

# TetPiece.py

import random, time, pygame, sys
from pygame.locals import *

# sizes 
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOXSIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

XMARGIN = int((WINDOW_WIDTH-BOARD_WIDTH * BOXSIZE)/2)
TOPMARGIN = WINDOW_HEIGHT-(BOARD_HEIGHT * BOXSIZE)-5


# colors        R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)

RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)

GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)

BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)

YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)


# template info for pieces
TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

BLANK = '.'

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}



class TetPiece():

    def __init__(self):
        # create a piece with a random shape, rotation, and color
        self.shape = random.choice(list(PIECES.keys()))
        self.rotation = random.randint(0, len(PIECES[self.shape])-1)

        self.x = int(BOARD_WIDTH/2)-int(TEMPLATE_WIDTH/2)
        self.y = -2    # start it above the board (i.e. less than 0)

        self.color = random.randint(0, len(COLORS)-1)

    def xMove(self, step):
        self.x += step

    def moveDown(self, step):
        self.y += step

    def rotateLeft(self):
        self.rotation = (self.rotation-1) % len(PIECES[self.shape])

    def rotateRight(self):
        self.rotation = (self.rotation + 1) % len(PIECES[self.shape])


    def getShape(self):
        return PIECES[self.shape][self.rotation]


    def draw(self, screen):
        shapeToDraw = PIECES[self.shape][self.rotation]
        xPix, yPix = self.toPixels(self.x, self.y)
    
        # draw each of the boxes that make up the piece
        for x in range(TEMPLATE_WIDTH):
            for y in range(TEMPLATE_HEIGHT):
                if shapeToDraw[y][x] != BLANK:
                    self.drawBox(screen, self.color, 
                                            xPix + (x * BOXSIZE), 
                                            yPix + (y * BOXSIZE))
    


    def toPixels(self, x, y):
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (XMARGIN + (x * BOXSIZE)), (TOPMARGIN + (y * BOXSIZE))
    
    
    def drawBox(self, screen, color, xPix, yPix):
        # draw a single box (each tetromino piece has four boxes)
        # at xPix & yPix
        if color == BLANK:
            return
        pygame.draw.rect(screen, COLORS[color], 
                           (xPix + 1, yPix + 1, BOXSIZE-1, BOXSIZE-1))
        pygame.draw.rect(screen, LIGHTCOLORS[color], 
                           (xPix + 1, yPix + 1, BOXSIZE-4, BOXSIZE-4))
    

