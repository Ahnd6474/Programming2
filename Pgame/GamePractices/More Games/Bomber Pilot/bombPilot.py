
# bombPilot.py


import pygame, random
from pygame.locals import *
from pygame.font import *

# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)
YELLOW =( 255, 255,   0)


# -------------------------------------------------------------


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("plane.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.sndBoom = pygame.mixer.Sound("boom.wav")
        self.sndThunder = pygame.mixer.Sound("thunder.wav")
        self.rect.centery = scrHeight-50
        self.rect.centerx = scrWidth/2


    def update(self, dir):
        self.rect.centerx += (dir*5)

# -------------------------------------------------------------


class Island(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("island.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()
        self.dy = 5

    def reset(self):
        self.rect.bottom = 0
        self.rect.x = random.randrange(0, screen.get_width())


    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > scrHeight-1:
            self.reset()


# -------------------------------------------------------------


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Cloud.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()


    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, scrWidth-1)
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)


    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > scrHeight-1:
            self.reset()


# -------------------------------------------------------------


class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("ocean.gif").convert()
                 # ocean.gif is 640 x 1440 big
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()


    def reset(self):
        self.rect.top = scrHeight - self.rect.height    # -960  
            # this places the bottom of the ocean image at the
            # bottom of the window, which means the top of the 
            # ocean image is way above the top of the window


    def update(self):
        self.rect.bottom += self.dy   # move image down
        if self.rect.top >= 0:  # if top of image is at top of screen
            self.reset()



# --------------------------------------------------


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


    def update(self):
        # movement function needed since using AnimSprite in a top-scroller
        if self.rect.y < scrHeight:   # if above bottom of window
            self.rect.y += 5    # move down
        else:
            self.setVisible(False)




# --------------------------------------------------



def renderInstructions(instructions):
    insIms = []
    for line in instructions:
        insIms.append(font.render(line, True, YELLOW))
    return insIms


def centerText(screen, msg):
    im = font.render(msg, True, WHITE)
    x = (scrWidth-im.get_width())/2
    y = (scrHeight-im.get_height())/2
    screen.blit(im, (x,y))




# ------------------------------------------
# main


pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill(WHITE)
pygame.display.set_caption("Bomber Pilot!")

scrWidth, scrHeight = screen.get_size()


# load game sounds
pygame.mixer.init()
pygame.mixer.music.load('biplane-flying.mp3')


# create sprites
ocean = Ocean()
island = Island()
cloud1 = Cloud()
cloud2 = Cloud()
cloud3 = Cloud()
plane = Plane()

# create animated sprites
playerExplo = AnimSprite('exploSheet.png', 9)
lightning = AnimSprite('lightningSheet.png', 6)


# group the sprites
cloudSprites = pygame.sprite.Group(cloud1, cloud2, cloud3)
sprites = pygame.sprite.OrderedUpdates(ocean, island, cloudSprites, plane)

font = pygame.font.SysFont(None, 30)

insIms = renderInstructions((
                "", 
                "Bomber Pilot",
                "",
                "Fly over an island to drop a bomb, but be",
                "careful not to fly too close to the clouds.",
                "You lose a life everytime your plane is hit",
                "by lightning.",
                "",
                "Use the left and right arrow keys to fly.", "",
                "Good Luck!",
                "",
                "Press space to start..."
             ))


# game vars
showStartScreen = True
gameOver = False
lives = 5
score = 0
moveDir = 0    # -1 means left; 1 means right

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
            elif event.key == K_SPACE:
                if showStartScreen:
                    showStartScreen = False
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.7)
            elif event.key == K_LEFT or event.key == K_a:
                moveDir = -1
            elif event.key == K_RIGHT or event.key == K_d:
                moveDir = 1

        elif event.type == KEYUP: 
            moveDir = 0


    # -------------- update game ---------------------

    if not showStartScreen and not gameOver:
        ocean.update()
        island.update()
        cloudSprites.update()
        plane.update(moveDir)

        playerExplo.update()
        lightning.update()
        
        # check collisions
        if plane.rect.collidepoint(island.rect.center):
            playerExplo.setPosition(island.rect.center)
            playerExplo.setVisible(True)
            plane.sndBoom.play()
            island.reset()
            score += 100
        
        hitClouds = pygame.sprite.spritecollide(plane, cloudSprites, False,
                                  pygame.sprite.collide_circle_ratio(0.7))
        if hitClouds:
            lightning.setPosition(hitClouds[0].rect.midbottom)
            lightning.setVisible(True)
            plane.sndThunder.play()
            lives -= 1
            for theCloud in hitClouds:
                theCloud.reset()

        if lives <= 0:
            gameOver = True



    # ----------------- redraw game ---------------------------

    screen.fill(BLUE) 
    if showStartScreen:
        for i in range(len(insIms)):
            screen.blit(insIms[i], (50, 30*i))

    else:
        sprites.draw(screen)

        playerExplo.draw(screen)
        lightning.draw(screen)

        status = "Lives: " + str(lives) + "; score: " + str(score)
        screen.blit(font.render(status, True, YELLOW), (10,10))

        if gameOver:
            centerText(screen, "Game Over")

    pygame.display.update()


pygame.mixer.music.stop()
pygame.quit()
