

# breakoutScores.py
# added name entry screen and high score screen


import pygame, random
from pygame.locals import *
from pygame.font import *

from NameBox import NameBox
from HighScores import HighScores


# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
DARKGRAY = ( 47, 79, 79)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)

WALL_SIZE = 10
BAT_STEP = 20




class Bat(pygame.sprite.Sprite):

    def __init__(self, fnm):
        super().__init__()
        self.image = pygame.image.load(fnm).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (scrWidth/2 - (self.rect.width/2), scrHeight - 20)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def move(self, step):
        if self.rect.x <= 0 and (step < 0):  
            # at left & going left
            step = 0
        elif self.rect.right >= scrWidth-1 and (step > 0):
            # at right and going right
            step = 0
        self.rect.x += step



# ---------------------------------------------------------


class Ball(pygame.sprite.Sprite):

    def __init__(self, fnm):
        super().__init__()
        self.image = pygame.image.load(fnm).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [scrWidth/2, scrHeight/2]
                       # start position of the ball in center of window
        self.xStep, self.yStep = self.randomSteps()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self):
        global lives, score

        if pygame.sprite.collide_rect(self, bat) and self.yStep > 0:
            # ball has hit the bat and is moving down
            hitSnd.play()
            self.yStep = -self.yStep    # change direction
            self.xStep = self.batRebound(self.xStep)

        if self.rect.y < 0 and self.yStep < 0:
            # at top and moving up
            hitSnd.play()
            self.yStep = -self.yStep

        if self.rect.y > scrHeight and self.yStep > 0:
            # at bottom and moving down
            lives -= 1
            # reposition
            self.xStep, self.yStep = self.randomSteps()
            self.rect.center = (scrWidth * random.random(), scrHeight / 3)

        if self.rect.x < 0 and self.xStep < 0:
            # at left and going left
            self.xStep = -self.xStep

        if self.rect.right > scrWidth and self.xStep > 0:
            # at right and going right
            self.xStep = -self.xStep


        # check if ball has hit a brick in the wall
        # if yes then delete brick and change ball direction
        index = self.rect.collidelist(wall.bricks)
        if index != -1:
            if self.rect.center[0] > wall.bricks[index].right or \
               self.rect.center[0] < wall.bricks[index].left:
                self.xStep = -self.xStep  # since hit a brick side
            else:
                self.yStep = -self.yStep  # since hit brick top/bottom
            hitSnd.play(0)
            wall.bricks[index:index + 1] = []  # remove brick
            score += 10
            if (wall.numBricks() == 0):
                wall.build()

        self.rect.x += self.xStep   # move the ball horizontally
        self.rect.y += self.yStep   # and vertically


    def batRebound(self, xstep):
        offset = self.rect.center[0] - bat.rect.center[0]
        # offset > 0 means ball has hit RHS of bat
        # vary x-step of ball depending on where ball hits bat
        if offset > 0:
            if offset > 30:
                xstep = 7
            elif offset > 23:
                xstep = 6
            elif offset > 17:
                xstep = 5
        else:
            if offset < -30:
                xstep = -7
            elif offset < -23:
                xstep = -6
            elif offset < -17:
                xstep = -5
        return xstep


    def randomSteps(self):
        # create a random pair
        x = 6
        if random.random() > 0.5:
            x = -x
        y = 6
        if random.random() > 0.5:
            y = -y
        return [x,y]


# ---------------------------------------------------------------


class Wall(pygame.sprite.Sprite):

    def __init__(self, fnm):
        super().__init__()
        self.image = pygame.image.load(fnm).convert()
        self.rect = self.image.get_rect()
        self.build()


    def build(self):
        # create the bricks
        x = 0; y = 60
        adj = 0
        self.bricks = []
        for i in range (0, 52):
            if x > scrWidth:
                if adj == 0:
                    adj = self.rect.width / 2
                else:
                    adj = 0
                x = -adj
                y += self.rect.height

            self.bricks.append(self.rect)
            self.bricks[i] = self.bricks[i].move(x, y)
            x += self.rect.width


    def numBricks(self):
        return len(self.bricks)


    def draw(self, screen):
        for i in range(0, len(self.bricks)):
            screen.blit(self.image, self.bricks[i])


# -----------------------------------


def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))



# ---------- main -------------

pygame.init()
screen = pygame.display.set_mode([640,480]) # , pygame.FULLSCREEN)
screen.fill(DARKGRAY)
pygame.display.set_caption("Breakout")

scrWidth, scrHeight = screen.get_size()


# load game sounds
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)   # Play forever

hitSnd = pygame.mixer.Sound('Blip_1-Surround-147.wav')
hitSnd.set_volume(0.5)


# create sprites
ball = Ball("ball.png")
bat = Bat("bat.png")
wall = Wall("brick.png")

nameBox = NameBox(scrWidth, scrHeight)
scores = HighScores(scrWidth, scrHeight)
scores.printScores()

# game vars
lives = 5   # used instead of gameOver boolean
score = 0

# scoring game states
enteringName = False
userName = ""
showingScores = False

font = pygame.font.Font(None, 30)
bigFont = pygame.font.Font(None, 70)

batStep = 0


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
            elif event.key == K_LEFT or event.key == K_a:
                batStep = -BAT_STEP
            elif event.key == K_RIGHT or event.key == K_s:
                batStep = BAT_STEP

            if enteringName:
                if event.key == K_BACKSPACE:
                    nameBox.backspace()
                elif event.key == K_RETURN:
                    userName = nameBox.getName()
                    scores.add(userName, score)
                    enteringName = False
                    showingScores = True
                else:
                    nameBox.addChar(event.key)


        elif event.type == KEYUP: 
            if event.key == K_LEFT or event.key == K_a or \
               event.key == K_RIGHT or event.key == K_s: 
                batStep = 0

    # update game
    if lives > 0:
        bat.move(batStep)
        ball.update()
    elif lives == 0 and not showingScores:   # game just over
        enteringName = True


    # redraw game
    screen.fill(DARKGRAY)

    wall.draw(screen)
    bat.draw(screen)
    ball.draw(screen)

    screen.blit(font.render(
             "Score: " +str(score) + "; Lives: " + str(lives), 1, WHITE), [10, 10])

    if enteringName:
        nameBox.draw(screen)
    elif lives == 0 and showingScores:
        centerImage(screen, font.render("Game Over ", True, GREEN))
        scores.draw(screen)

    pygame.display.update()


pygame.quit()


