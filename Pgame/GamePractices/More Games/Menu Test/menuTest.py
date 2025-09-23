

import pygame, sys, random
from pygame.locals import *


# colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = (   0,   0, 255)
YELLOW =( 255, 255,   0)



class Button(pygame.sprite.Sprite):

    def __init__(self, label, pos):
        super().__init__() 
        self.image = pygame.image.load("button.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.over = pygame.image.load("buttonOver.png").convert_alpha()
        self.isHighlighted = False

        font = pygame.font.Font(None, 24)
        self.label = label
        self.labelIm = font.render(label, True, YELLOW)
        self.labelRect = self.labelIm.get_rect()
        self.labelRect.x = self.rect.x + \
                      (self.rect.width - self.labelIm.get_width())/2
        self.labelRect.y = self.rect.y + \
                      (self.rect.height - self.labelIm.get_height())/2


    def setHighlight(self, isOn):
        self.isHighlighted = isOn


    def hasHit(self, pos):
        return self.rect.collidepoint(pos)
    

    def draw(self, screen):
        if self.isHighlighted:
            screen.blit(self.over, self.rect)
        else:
            screen.blit(self.image, self.rect)
        screen.blit(self.labelIm, self.labelRect)

# --------------------------------------------------

def getButtonIdx(pos):
    for i, button in enumerate(buttons):
        if button.hasHit(pos):
            return i
    return -1


def setHighlight(idx, isOn):
    if idx != -1:
        buttons[idx].setHighlight(isOn)


# --------------- main --------------------

# main

pygame.init()
screen = pygame.display.set_mode([250, 400])
pygame.display.set_caption('Menu Test')
scrWidth, scrHeight = screen.get_size()

font = pygame.font.Font(None, 50)

click = pygame.mixer.Sound('click.wav')
click.set_volume(1)


# I'm going to create 5 buttons, and brHeight represents the
# vertical distance between the buttons' centers
brHeight = scrHeight/5

buttons = []
  # the position of a button in this list is its index position

buttons.append( Button("Load", (scrWidth/2, brHeight/2)))
buttons.append( Button("Options", (scrWidth/2, brHeight*3/2)))
buttons.append( Button("Help", (scrWidth/2, brHeight*5/2)))
buttons.append( Button("Save", (scrWidth/2, brHeight*7/2)))
buttons.append( Button("Quit", (scrWidth/2, brHeight*9/2)))

prevIdx = -1       # the button that was previously highlighted
currIdx = 0        # currently highlighted button

pressedIdx = -1    # which button was pressed


clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False

        if event.type == MOUSEMOTION:
            idx = getButtonIdx(pygame.mouse.get_pos())
            if idx != -1:
                prevIdx = currIdx
                currIdx = idx

        if event.type == MOUSEBUTTONDOWN:
            idx = getButtonIdx(pygame.mouse.get_pos())
            if idx != -1:
                prevIdx = currIdx
                currIdx = idx
                pressedIdx = currIdx

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP or event.key == K_w:
                prevIdx = currIdx
                currIdx = (currIdx - 1) % len(buttons)
            elif event.key == K_DOWN or event.key == K_s:
                prevIdx = currIdx
                currIdx = (currIdx + 1) % len(buttons)
            elif event.key == K_RETURN:
                pressedIdx = currIdx


    # update menu
    setHighlight(prevIdx, False)
    setHighlight(currIdx, True)

    if pressedIdx != -1:
        print("pressed button", pressedIdx, ":", buttons[pressedIdx].label)
        click.play()
        pressedIdx = -1


    # redraw menu
    screen.fill(WHITE)
    for i in range(len(buttons)):
        buttons[i].draw(screen)

    pygame.display.update()

pygame.quit()

