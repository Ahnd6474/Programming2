
# platformer.py

import pygame, random
from pygame.locals import *
from pygame.font import *


# some colors
BLACK = (   0,   0,   0)
GRAY  = (185, 185, 185)
WHITE = ( 255, 255, 255)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)

GRAVITY = 1
BLOCK_SIZE = 30
PLAYER_STEP = 8
JUMP_STEP = 20
NUM_BALLS = 3

# player moves
NONE = 0
RIGHT = 1 
LEFT = 2


# -------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    # the player doesn't move left or right, the world moves instead,
    # but the player can jump up

    def __init__(self, pt):
        super().__init__()
        self.left = pygame.image.load("lidiaLeft.png").convert_alpha() 
        self.right = pygame.image.load("lidiaRight.png").convert_alpha() 
        self.image = self.right
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound("jump.wav")
        self.rect.x = pt[0]
        self.rect.y = pt[1]-self.rect.height  # so feet resting on platform
        self.yStep = 0


    def turn(self, move):
        if move == LEFT:
            self.image = self.left
        elif move == RIGHT:
            self.image = self.right
    

    def yMove(self):
        # calculates the y-axis movement for the player
        if (world.hitPlatform(self) and self.yStep >= 0) or \
           self.rect.bottom >= scrHeight-1:
            self.yStep = 0   # stop vertical movement
        else:   # in the air
            self.yStep += GRAVITY

        if self.yStep > JUMP_STEP:   # terminal velocity
            self.yStep = JUMP_STEP

        self.rect.y += self.yStep

        if self.rect.bottom > scrHeight-1:   # stand on floor
            self.rect.bottom = scrHeight-1



    def jump(self):
        # player jumps, but only if on a platform or floor
        if (world.hitPlatform(self) and self.yStep == 0) or \
           self.rect.bottom >= scrHeight-1:
            self.yStep = -JUMP_STEP
            self.rect.y += self.yStep
            self.sound.play()


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# -------------------------------------------------------------


class BlockSprite(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.start = (x, y)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


# --------------------------------------------------------

class World():
    # holds the platforms and goals extracted from a map
    # the world moves left and right instead of the player

    def __init__(self, map):
        self.platforms = []
        self.goals = []
        y = 0
        for line in map:
            x = 0
            for ch in line:
                if ch == "-":    # a platform block
                    self.platforms.append( 
                         BlockSprite(x, y, BLOCK_SIZE, BLOCK_SIZE, GRAY))
                elif ch == "G":  # a goal block
                    self.goals.append(
                         BlockSprite(x, y, BLOCK_SIZE, BLOCK_SIZE, BLUE))
                x += BLOCK_SIZE
            y += BLOCK_SIZE


    def xMove(self, dist):
        # move the world horizontally
        for block in self.platforms + self.goals:
            block.rect.x += dist


    def startPlatform(self):
        # get topleft of left-most platform
        x = scrWidth; y = 0
        for block in self.platforms:
            if x > block.rect.x:
                x,y = block.rect.topleft
        return (x,y)


    def hitPlatform(self, player):
        # has the player hit any platform?
        for block in self.platforms:
            if pygame.sprite.collide_rect(player, block):
                return True
        return False


    def hitGoal(self, player):
        # has the player hit any goal?
        for block in self.goals:
            if pygame.sprite.collide_rect(player, block):
                return True
        return False



    def draw(self, screen):
        # draw the goals and platforms
        for block in self.platforms + self.goals:
            block.draw(screen)


# -------------------------------------------------------------

class Fireball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("flame.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()


    def reset(self):
        # place the fireball a random distance across the screen 
        # and give it a random step
        self.yStep = random.randint(3, 7)
        x = random.randint(0, scrWidth-1-self.rect.width)
        self.rect.bottomleft = (x, 0)


    def xMove(self, dist):
        # move the fireball horizontally
        self.rect.x += dist
        if (self.rect.x < -self.rect.width) or (self.rect.x > scrWidth):
            self.reset()


    def yMove(self):
        # move the fireball down
        self.rect.y += self.yStep
        if self.rect.y > scrHeight:
            self.reset()


# -------------------------------------------------------------

class Fireballs():
    # manage the fireballs

    def __init__(self, numBalls):
        self.fireballs = []
        for i in range(numBalls):  
            self.fireballs.append( Fireball() )
        self.sprites = pygame.sprite.Group( self.fireballs )


    def yMove(self):
        # move fireballs down
        for fb in self.fireballs:
            fb.yMove()


    def xMove(self, dist):
        # move fireballs left/right
        for fb in self.fireballs:
            fb.xMove(dist)


    def draw(self, screen):
        self.sprites.draw(screen)


    def hasHit(self, player):
        # player has been hit by a fireball
        fb = pygame.sprite.spritecollideany(player, self.sprites)
        if fb is not None:
            fb.reset()
            return True
        else:
            return False



# -------------------------------------------------------------

class Scenery():
    # for drawing the background and moving it
    # assumes image is bigger than the window and
    # only moves left and right

    def __init__(self, fnm):  # clouds.png is 1000 x 400
        self.image = pygame.image.load(fnm).convert()
        self.rect = self.image.get_rect()


    def xMove(self, dist):
        self.rect.x += dist
        if (self.rect.right < 0) or \
           (self.rect.x > self.rect.width):
            self.rect.x = 0


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if (self.rect.right < scrWidth):   # draw extra image on right
            screen.blit(self.image, (self.rect.right, 0))
        elif (self.rect.x > 0):            # draw extra image on left
            screen.blit(self.image, (self.rect.x - self.rect.width,0))


# -------------------------------------------------------------


def centerImage(screen, im):
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))


# -------------------------------------------------------------
# main

pygame.init()
screen = pygame.display.set_mode((600,400))
screen.fill(BLACK)
pygame.display.set_caption("Platformer")

scrWidth, scrHeight = screen.get_size()

map=[
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                                                            ",
    "                    ---                         ----   G",
    "         -- --        ---             ------",
    " -- -                        -------            "]

# initialize sprites
scenery = Scenery("clouds.png")
world = World(map)
balls = Fireballs(NUM_BALLS) 
player = Player( world.startPlatform())

# game vars
gameOver = False
move = NONE
isJumping = False
lives = 10

font = pygame.font.Font(None, 48)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                isJumping = True
            if event.key == K_LEFT or event.key == K_a:   # up and left/right possible
                move = LEFT 
            elif event.key == K_RIGHT or event.key == K_d:
                move = RIGHT 

        elif event.type == KEYUP:
            move = NONE


    # update game
    if not gameOver:
        player.turn(move)
  
        if isJumping:
            player.jump()
            isJumping = False

        if move == LEFT:   # game objects move the opposite way
            world.xMove(PLAYER_STEP)    # right
            balls.xMove(PLAYER_STEP)
            scenery.xMove(PLAYER_STEP/2)  # slower since 'further away'
        elif move == RIGHT:
            world.xMove(-PLAYER_STEP)
            balls.xMove(-PLAYER_STEP)
            scenery.xMove(-PLAYER_STEP/2)
        
        player.yMove()
        balls.yMove()

        if balls.hasHit(player):
            lives -= 1
       
        if world.hitGoal(player) or lives == 0:
            gameOver = True
      

    # redraw
    scenery.draw(screen)
    world.draw(screen)
    player.draw(screen)
    balls.draw(screen)

    screen.blit(font.render("Lives: " +str(lives), 1, BLUE), [10, 10])

    if gameOver:
        centerImage(screen, font.render("Game Over", True, RED))

    pygame.display.update()

pygame.quit()




