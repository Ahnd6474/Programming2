
# WhackAMole.py
# Whack-a-mole game using pygame


import pygame, random
from pygame.locals import *
from pygame.font import *



# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
DARKGRAY = ( 47, 79, 79)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)




# ---------------------------------------------------------

class Mole(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("mole.gif").convert_alpha()
        self.rect = self.image.get_rect()


    # move mole to a new random location
    # after it is hit
    def flee(self):
        x = random.randint(0, scrWidth-1-self.rect.width)
        y = random.randint(0, scrHeight-1-self.rect.height)
        self.rect.topleft = (x,y)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ---------------------------------------------------------


class Shovel(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("shovel.gif").convert_alpha()
        self.rect = self.image.get_rect()


    # did the shovel hit the mole?
    def hit(self, target):
        return self.rect.colliderect(target)


    # follows the mouse cursor
    def update(self, pt):
        self.rect.center = pt


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# -----------------------------------


def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))



# ---------- main -------------

pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(DARKGREEN)
pygame.display.set_caption("Whack-a-mole")

scrWidth, scrHeight = screen.get_size()


# hide the mouse cursor
# pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 40)

hitSnd = pygame.mixer.Sound('hit.wav')
hitSnd.set_volume(1)


# create sprites and a group
mole = Mole()
shovel = Shovel()

# game vars
hits = 0
mousePos = (scrWidth/2, scrHeight/2)
isPressed = False

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
    shovel.update(mousePos)

    if isPressed:
      isPressed = False
      if shovel.hit(mole):
          hitSnd.play()
          mole.flee()
          hits += 1


    # redraw game
    screen.fill(DARKGREEN)
    mole.draw(screen)
    shovel.draw(screen)
    
    # time elapsed (in secs)
    time = int(pygame.time.get_ticks()/1000)
    timeIm = font.render(str(time), True, WHITE)
    screen.blit(timeIm, (10,10))

    hitIm = font.render("Hits = " + str(hits), True, WHITE)
    centerImage(screen, hitIm)

    pygame.display.update()


pygame.quit()
