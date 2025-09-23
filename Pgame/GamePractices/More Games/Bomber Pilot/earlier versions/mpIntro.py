''' mpIntro
    step 8 of mailPlane

    build intro screen
    add state management
'''

import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

# -------------------------------------------------------------


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("yay.ogg")
            self.sndThunder = pygame.mixer.Sound("thunder.ogg")
            self.sndEngine = pygame.mixer.Sound("engine.ogg")
            self.sndEngine.set_volume(.05)
            self.sndEngine.play(-1)

    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)

# -------------------------------------------------------------


class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("island.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

        self.dy = 5

    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(0, screen.get_width())

# -------------------------------------------------------------


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cloud.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)

# -------------------------------------------------------------


class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ocean.gif")
        self.rect = self.image.get_rect()
        self.dy = 5
        self.reset()

    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1440:
            self.reset()

    def reset(self):
        self.rect.top = -960


# -------------------------------------------------------------

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)

    def update(self):
        self.text = "planes: %d, score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()


# -------------------------------------------------------------


def game():
    pygame.display.set_caption("Mail Pilot! mpIntro - Add intro and game states")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    plane = Plane()
    island = Island()
    cloud1 = Cloud()
    cloud2 = Cloud()
    cloud3 = Cloud()
    ocean = Ocean()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.Group(ocean, island, plane)
    cloudSprites = pygame.sprite.Group(cloud1, cloud2, cloud3)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        #check collisions

        if plane.rect.colliderect(island.rect):
            plane.sndYay.play()
            island.reset()
            scoreboard.score += 100

        hitClouds = pygame.sprite.spritecollide(plane, cloudSprites, False)
        if hitClouds:
            plane.sndThunder.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
            for theCloud in hitClouds:
                theCloud.reset()

        friendSprites.update()
        cloudSprites.update()
        scoreSprite.update()

        friendSprites.draw(screen)
        cloudSprites.draw(screen)
        scoreSprite.draw(screen)

        pygame.display.flip()

    #turn off engine noise
    plane.sndEngine.stop()
    #show mouse cursor
    pygame.mouse.set_visible(True)
    return scoreboard.score


def instructions(score):
    plane = Plane()
    ocean = Ocean()

    allSprites = pygame.sprite.Group(ocean, plane)
    insFont = pygame.font.SysFont(None, 50)

    instructions = (
    "Mail Pilot.     Last score: %d" % score ,
    "Instructions:  You are a mail pilot,",
    "delivering mail to the islands.",
    "",
    "Fly over an island to drop the mail,",
    "but be careful not to fly too close",
    "to the clouds. Your plane will fall ",
    "apart if it is hit by lightning too",
    "many times.",
    "",
    "good luck!",
    "",
    "click to start, escape to quit..."
    )

    insLabels = []
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)

    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True

        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()

    plane.sndEngine.stop()
    pygame.mouse.set_visible(True)
    return donePlaying


def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()

if __name__ == "__main__":
    main()

