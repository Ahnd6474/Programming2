
# invaders.py

import pygame, random, os
from pygame.locals import *


# colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = (   0,   0, 255)
YELLOW =( 255, 255,   0)

# distance between alien sprites
ALIEN_SEP = 20


# (width, height) sizes
BULLET_SIZE  = (7, 20)
MISSILE_SIZE = (7, 10)




class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = (scrWidth/2) - (self.rect.width/2)
        self.rect.y = 520
        self.step = 7
        self.firedTime = 0     # when player last fired a shot

    def update(self):
        self.rect.x += playerDir * self.step
        if self.rect.x < 0:      # stay visible
            self.rect.x = 0
        elif self.rect.x > (scrWidth - self.rect.width):
            self.rect.x = scrWidth - self.rect.width


# --------------------------------------------------


class Alien(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.numMoves = [0, 0]   # in x- and y- directions
        self.dir = 1             # or -1  in x-direction
        self.step = self.image.get_width() - 7  # in x-direction
        self.moveDelay = 700    # time delay between moves (in ms)
        self.movedTime = 0      # when alien last moved


    def update(self):
        # move the alien to the left and right, and downwards;
        # the alien can move 12 steps horizontally and 4 steps down;
        # a move can occur every moveDelay ms
        currTime = pygame.time.get_ticks()
        if (currTime - self.movedTime) > self.moveDelay:
            if self.numMoves[0] < 12:
                self.rect.x += self.dir * self.step   # move horizontally
                self.numMoves[0] += 1
            else:
                if self.numMoves[1] < 4:
                    self.rect.y += ALIEN_SEP  # move down
                    self.numMoves[1] += 1
                self.dir *= -1         # change x- direction
                self.numMoves[0] = 0    # reset num of x moves
                self.moveDelay -= 20    # reduce delay between moves
            self.movedTime = currTime


# --------------------------------------------------


class Ammo(pygame.sprite.Sprite):
    def __init__(self, color, size, x, y, step):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.step = step

    def update(self):
        self.rect.y += self.step
        if (self.rect.y < 0) or (self.rect.y > scrHeight):
            self.kill()    # if ammo has left screen, kill it


# --------------------------------------------------


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])  # size is 10 x 10
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()



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




# --------------------------------------------------



def createWall(rows, columns, sep):
    for r in range(rows):
        for c in range(columns):
            block = Block()
            block.rect.x = (55 + (200 * sep)) + (c * block.rect.width)
            block.rect.y = 450 + (r * block.rect.height)
            walls.add(block)
            sprites.add(block)



def createAliens(rows, columns, sep):
    for r in range(rows):
        for c in range(columns):
            alien = Alien()
            alien.rect.x = sep + (c * (alien.rect.width + sep))
            alien.rect.y = 65 + (r * (alien.rect.height + sep))
            aliens.add(alien)
            sprites.add(alien)


def playerShoot():
    global canFire
    currTime = pygame.time.get_ticks()
    if (currTime - player.firedTime) > 500:   # shoot only after 500 ms
        x, y = player.rect.midtop
        x -= BULLET_SIZE[0]
        y -= BULLET_SIZE[1]
        bullet = Ammo(BLUE, BULLET_SIZE, x, y, -26)  # bullets move up
        bullets.add(bullet)
        sprites.add(bullet)
        player.firedTime = currTime
        bullet_fx.play()
    canFire = False


def alienShoot():
    if len(aliens):
        if random.random() <= 0.05:
            shooter = random.choice([ alien for alien in aliens])
                   # randomly choose from aliens group as a list
            x, y = shooter.rect.midbottom
            x -= MISSILE_SIZE[0]
            y += MISSILE_SIZE[1]
            missile = Ammo(RED, MISSILE_SIZE, x, y, 10)  # missiles move down
            missiles.add(missile)
            sprites.add(missile)



def checkCollisions():
    global score, numLives
    pygame.sprite.groupcollide(bullets, walls, True, True)   # do-kill args
        # a player bullet hits a walls brick

    pygame.sprite.groupcollide(missiles, walls, True, True)
        # a missile hits a walls brick

    for z in pygame.sprite.groupcollide(bullets, aliens, True, True):
        # a player bullet hits an alien
        alienExplo.setPosition(z.rect.center)
        alienExplo.setVisible(True)
        boom_fx.play()
        score += 10

    if pygame.sprite.groupcollide(playerGroup, missiles, False, True):
        # a missile hits the player
        playerExplo.setPosition(player.rect.center)
        playerExplo.setVisible(True)
        explosion_fx.play()
        numLives -= 1




def isGameOver():
    global finalMsg
    if numLives == 0:
        finalMsg = "The war is lost! You scored: " + str(score)
        return True
    elif len(aliens) == 0:
        finalMsg = "You win! You scored: " + str(score)
        return True
    else:
        return False



# ----------------------------------------------


# main

pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Invaders')
scrWidth, scrHeight = screen.get_size()

# game fonts
pygame.font.init()
gameFont = pygame.font.Font('Orbitracer.ttf', 28)
splashFont = pygame.font.Font('Orbitracer.ttf', 72)

# load game images
startIm = pygame.image.load('startScreen.jpg').convert()
background = pygame.image.load('background.jpg').convert()

# load game sounds
pygame.mixer.music.load('arpanauts.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

bullet_fx = pygame.mixer.Sound('fire.wav')
explosion_fx = pygame.mixer.Sound('explode.wav')
boom_fx = pygame.mixer.Sound('boom.wav')
# explosion_fx.set_volume(0.5)


# game vars
showStartScreen = True
gameOver = False
finalMsg = ""

# player vars
playerDir = 0
canFire = False
score = 0
numLives = 20


# create sprite groups
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
missiles = pygame.sprite.Group()
walls = pygame.sprite.Group()
sprites = pygame.sprite.Group()


# create player, walls, and alien sprites
player = Player()
playerGroup = pygame.sprite.Group(player)
sprites.add(player)

for spacing in range(4):   # create 4 walls
    createWall(3, 9, spacing)
    # a wall is 3 x 9 bricks (rows x cols)

createAliens(4, 10, ALIEN_SEP)
    # create grid of 4 x 10 aliens  (rows x cols)


# create explosion sprites
playerExplo = AnimSprite('exploSheet.png', 9)
alienExplo = AnimSprite('alienExploSheet.png', 10)


# pygame.mouse.set_visible(False)
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
            elif event.key == K_LEFT:
                playerDir = -1
            elif event.key == K_RIGHT:
                playerDir = 1
            elif event.key == K_SPACE:
                if showStartScreen:
                    showStartScreen = False
                else:
                    canFire = True

        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                playerDir = 0

    # update game
    if not showStartScreen and not gameOver:
        for i in sprites:
           i.update()
        alienShoot()
        if canFire:
            playerShoot()
        checkCollisions()
        gameOver = isGameOver()

    # redraw game
    if showStartScreen:
        screen.blit(startIm, [0, 0])
        screen.blit(splashFont.render(
                   "Invaders", 1, WHITE), (265, 120))
        screen.blit(gameFont.render(
                    "Press space to play", 1, WHITE), (274, 191))
    else:
        screen.blit(background, [0, 0])
        sprites.draw(screen)

        playerExplo.draw(screen)
        alienExplo.draw(screen)

        screen.blit(gameFont.render(
                    "SCORE " + str(score), 1, WHITE), (10, 8))
        screen.blit(gameFont.render(
                    "LIVES " + str(numLives + 1), 1, RED), (355, 575))
        if gameOver:
            screen.blit(gameFont.render(finalMsg,  1, RED), (200, 15))

    pygame.display.update()


pygame.quit()

