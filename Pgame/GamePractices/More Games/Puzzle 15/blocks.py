
# 16-blocks

import pygame, random
from pygame.locals import *
from pygame.font import *

# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)


NUM_SIDE = 4
BOX_SIZE = 50
SPACING = 15



# -----------------------------------------

class Board:
    
    win_state = [i for i in range(1,NUM_SIDE*NUM_SIDE)] + [0]  # at end


    def __init__(self):
        # blocks list in order 0-15
        self.blocks = [Block(i,j) for j in range(NUM_SIDE) \
                                      for i in range(NUM_SIDE)]
        while True:
            random.shuffle(self.blocks)
            if self.isSolvable():
              return



    def isSolvable(self):
        # based on http://mathworld.wolfram.com/15Puzzle.html
        r = self.findBlankIdx()//NUM_SIDE   # get row
        counts = []
        for i,block in enumerate(self.blocks):
            for j in range(i):
                if 0 < self.blocks[j].val < block.val:
                    counts.append(1)
        return ((sum(counts) + r) % 2 == 0)



    def findBlankIdx(self):
        for index, block in enumerate(self.blocks):
            if block.isBlank():
                return index
        return -1



    def update(self, clickPos):
        index = self.selectedBlockIdx(clickPos)
        if (index != -1) and not self.blocks[index].isBlank():
            return self.moveBlock(index)
        return 0


    def selectedBlockIdx(self, pos):
        for index, block in enumerate(self.blocks):
            if block.contains(pos):
                return index
        return -1



    def moveBlock(self, index):
        # move block at index position in blocks's list;
        # the block must be adjacent to the blank block
        numClicks = 0
        blankIdx = self.findBlankIdx()
        if areAdjacent(index, blankIdx):  # can move
            # print("Moving from", index, "to", blankIdx)
            # print("  From", toCoord(index), "to", toCoord(blankIdx))
            # print("  Moving block", self.blocks[index].val)

            self.blocks[blankIdx], self.blocks[index] = \
                  self.blocks[index], self.blocks[blankIdx]
            numClicks = 1
        return numClicks



    def isCompleted(self):
        vals = []
        for block in self.blocks:
             vals.append(block.val)
        return (vals == Board.win_state)



    def draw(self, screen):
        for index, block in enumerate(self.blocks):
            block.draw(screen, index)



# -----------------------------------------

class Block(pygame.sprite.Sprite):

    def __init__(self, i, j):
        super().__init__() 
        self.val = i + (j * NUM_SIDE)  
              # this block always represents val, even if (i, j) change
              # val == 0 denotes the blank block

        # white square
        self.image = pygame.Surface( (BOX_SIZE, BOX_SIZE) )
        pygame.draw.rect(self.image, WHITE, (0,0, BOX_SIZE, BOX_SIZE))
        self.rect = self.image.get_rect()


    def isBlank(self):
        return (self.val == 0)


    def contains(self, pos):
        return self.rect.collidepoint(pos)


    def draw(self, screen, idx):
        coord = toCoord(idx)
        if not self.isBlank():
            self.rect.x = coord[0]
            self.rect.y = coord[1] 
            screen.blit(self.image, self.rect)

            valIm = font.render(str(self.val), True, BLACK)
            valRect = valIm.get_rect()
            valRect.center = self.rect.center
            screen.blit(valIm, valRect)

        

    # compare this block to other by val

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val


# -----------------------------------


def areAdjacent(idx1, idx2):
    # print("areAdjacent:", idx1, " ", idx2)
    if (idx1//NUM_SIDE) == (idx2//NUM_SIDE): # in the same row
        if (idx1+1 == idx2) or (idx1-1 == idx2):
            return True

    elif (idx1%NUM_SIDE) == (idx2%NUM_SIDE): # in the same column
        if (idx1+NUM_SIDE == idx2) or (idx1-NUM_SIDE == idx2):
            return True
    return False



def toPos(idx):
    j = idx//NUM_SIDE    # row
    i = idx%NUM_SIDE     # column
    return (i,j)


def toCoord(idx):
    j = idx//NUM_SIDE
    i = idx%NUM_SIDE
    x = (i+1)*SPACING + i*BOX_SIZE
    y = (j+1)*SPACING + j*BOX_SIZE 
    return (x,y)



def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))


# ----------------------------------------------
# main


pygame.init()

side = NUM_SIDE*BOX_SIZE + (NUM_SIDE + 1)*SPACING 
screen = pygame.display.set_mode((side, side+45))
screen.fill(BLACK)
pygame.display.set_caption("15-Blocks")

scrWidth, scrHeight = screen.get_size()

# sprites
board = Board()



# game vars
clicks = 0
gameOver = False

font = pygame.font.SysFont('Verdana', 20)

clock = pygame.time.Clock()

running = True    
while running:
    clock.tick(30)
    clickPos = None

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
        if event.type == MOUSEBUTTONDOWN:
            clickPos = event.pos


    # update game
    if not gameOver:
        if clickPos is not None:
            clicks += board.update(clickPos)
        gameOver = board.isCompleted()
        

    # redraw
    screen.fill(BLACK)                       
    board.draw(screen)
    screen.blit(font.render('Clicks: ' + str(clicks), True, WHITE), [20, scrHeight-40] )
    if gameOver:
        centerImage(screen, font.render("Game Over", True, RED))

    pygame.display.update()

pygame.quit()
