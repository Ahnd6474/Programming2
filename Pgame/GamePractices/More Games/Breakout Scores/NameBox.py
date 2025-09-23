
# NameBox.py

import pygame, string
from pygame.locals import *
from pygame.font import *

# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)


BOX_HEIGHT = 34
BOX_WIDTH = 400
GAP = 4

class NameBox():

    def __init__(self, scrWidth, scrHeight):
        self.scrWidth = scrWidth
        self.scrHeight = scrHeight
        self.currChars = []
        self.font = pygame.font.Font(None,40)
        self.question = "Enter Name: "
    

    def draw(self, screen):
      pygame.draw.rect(screen, BLACK,
                       ((self.scrWidth - BOX_WIDTH)/2,
                        (self.scrHeight - BOX_HEIGHT)/2, 
                         BOX_WIDTH, BOX_HEIGHT), 0)
      pygame.draw.rect(screen, WHITE,
                       ((self.scrWidth - BOX_WIDTH - GAP)/2,
                        (self.scrHeight - BOX_HEIGHT - GAP)/2, 
                        BOX_WIDTH + GAP, BOX_HEIGHT + GAP), 1)

      msg = self.question + "".join(self.currChars)
      screen.blit(self.font.render(msg, True, WHITE),
                    ((self.scrWidth - BOX_WIDTH)/2,
                        (self.scrHeight - BOX_HEIGHT)/2))


    def addChar(self, key):
        if key <=127:
            self.currChars.append( chr(key) )


    def backspace(self):
        self.currChars = self.currChars[0:-1]


    def getName(self):
        return "".join(self.currChars)

