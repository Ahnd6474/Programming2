

# TetBoard.py

import random, time, pygame, sys
from pygame.locals import *


# game sizes
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


# piece info
TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

BLANK = '.'



class TetBoard():

    def __init__(self):
        # create and return a new blank board data structure
        self.board = []
        for i in range(BOARD_WIDTH):
            self.board.append([BLANK] * BOARD_HEIGHT)



    def add(self, piece):
        # fill in the board based on piece's location, shape, and rotation
        shape = piece.getShape()
        for x in range(TEMPLATE_WIDTH):
            for y in range(TEMPLATE_HEIGHT):
                if shape[y][x] != BLANK:
                    self.board[x + piece.x][y + piece.y] = piece.color
    
    
    
    
    def isOnBoard(self, x, y):
        return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT
    
    
    def isValidPos(self, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        shape = piece.getShape()
        for x in range(TEMPLATE_WIDTH):
            for y in range(TEMPLATE_HEIGHT):
                isAboveBoard = ((y + piece.y + adjY) < 0)
                if isAboveBoard or shape[y][x] == BLANK:
                    continue
                if not self.isOnBoard(x + piece.x + adjX, y + piece.y + adjY):
                    return False
                if self.board[x + piece.x + adjX][y + piece.y + adjY] != BLANK:
                    return False
        return True
    


    def isCompleteLine(self, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARD_WIDTH):
            if self.board[x][y] == BLANK:
                return False
        return True
    
    
    def removeCompleteLines(self):
        # Remove any completed lines on the board, 
        # move everything above them down, 
        # and return the number of complete lines.
        numLinesRemoved = 0
        y = BOARD_HEIGHT-1 # start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARD_WIDTH):
                        self.board[x][pullDownY] = self.board[x][pullDownY-1]
                # Set very top line to blank.
                for x in range(BOARD_WIDTH):
                    self.board[x][0] = BLANK
                numLinesRemoved += 1
                # On the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1 # move on to check next row up
        return numLinesRemoved
    
    
    
    
    def toPixels(self, x, y):
        # Convert the given (x,y) coordinates of the board to (x,y)
        # coordinates of the location on the screen.
        return (XMARGIN + (x * BOXSIZE)), (TOPMARGIN + (y * BOXSIZE))
    
    
    def drawBox(self, screen, x, y, color):
        # draw a single box (each tetromino piece has four boxes)
        # at (x,y) coordinates on the board
        if color == BLANK:
            return
        xPix, yPix = self.toPixels(x, y)
        pygame.draw.rect(screen, COLORS[color], 
                             (xPix + 1, yPix + 1, BOXSIZE-1, BOXSIZE-1))
        pygame.draw.rect(screen, LIGHTCOLORS[color], 
                             (xPix + 1, yPix + 1, BOXSIZE-4, BOXSIZE-4))
    
    
    def draw(self, screen):
        # draw the border around the board
        pygame.draw.rect(screen, BLUE, 
                       (XMARGIN-3, TOPMARGIN-7,
                       (BOARD_WIDTH * BOXSIZE) + 8, (BOARD_HEIGHT * BOXSIZE) + 8), 5)
    
        # fill the background of the board
        pygame.draw.rect(screen, BLACK, (XMARGIN, TOPMARGIN, 
                                         BOXSIZE * BOARD_WIDTH, BOXSIZE * BOARD_HEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.drawBox(screen, x, y, self.board[x][y])
    
    