
# Fred.py

import pygame, random
from pygame.locals import *


class Fred(pygame.sprite.Sprite):



    def __init__(self, scrWidth, scrHeight):
        super().__init__() 
        self.leftImage = pygame.image.load("assets/Fred-Left.png").convert_alpha()
        self.rightImage = pygame.image.load("assets/Fred-Right.png").convert_alpha()
        self.leftImageHit = pygame.image.load("assets/Fred-Left-Hit.png").convert_alpha()
        self.rightImageHit = pygame.image.load("assets/Fred-Right-Hit.png").convert_alpha()

        self.sounds = self.loadSounds()

        self.image = self.rightImage
        self.rect = self.image.get_rect()
        self.scrWidth = scrWidth
        self.scrHeight = scrHeight
        self.reset()


    def loadSounds(self):
        # load 4 sounds effects; set their volumes
        sounds = []
    
        snd = pygame.mixer.Sound("assets/burp1.wav")
        snd.set_volume(1)
        sounds.append(snd)
    
        snd = pygame.mixer.Sound("assets/doh.wav")
        snd.set_volume(1)
        sounds.append(snd)
    
        snd = pygame.mixer.Sound("assets/huh.wav")
        snd.set_volume(1)
        sounds.append(snd)
    
        snd = pygame.mixer.Sound("assets/ouch.wav")
        snd.set_volume(1)
        sounds.append(snd)
    
        return sounds




    def reset(self):
        self.rect.x = self.scrWidth/2
        self.rect.y = self.scrHeight-1-self.rect.height

        self.isHit = False
        self.timeHit = 0
        self.health = 100

        self.isMoving = False
        self.moveRight = True
        self.step = 8


    def move(self, dir, currTime):

        if currTime - self.timeHit > 800:
            self.timeHit = 0
            self.isHit = False

        if (dir == 0):
            self.isMoving = False
        elif (dir > 0):
            self.isMoving = True
            self.moveRight = True
        else:
            self.isMoving = True
            self.moveRight = False

        if self.isMoving:
            if not self.moveRight:   # i.e. move left
                if((self.rect.x - self.step) > 0):
                    self.rect.x -= self.step
            
            elif self.moveRight:
                if((self.rect.right + self.step) < self.scrWidth-1):
                    self.rect.x += self.step
            


    def hit(self, currTime):
        self.isHit = True
        self.timeHit = currTime
        self.health -= 10
        idx = random.randint(0, len(self.sounds)-1)
        self.sounds[idx].play()



    def draw(self, screen):

        if self.moveRight:
            if not self.isHit:
                screen.blit(self.rightImage, self.rect)
            else:
                screen.blit(self.rightImageHit, self.rect)
        else:
            if not self.isHit:
                screen.blit(self.leftImage, self.rect)
            else:
                screen.blit(self.leftImageHit, self.rect)


