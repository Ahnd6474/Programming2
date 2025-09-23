
# Barrel.py

import random, pygame
from pygame.locals import *


class Barrel(pygame.sprite.Sprite):

    SLOTS = [(4, 103), (82, 27), (157, 104), (234, 27), 
             (310, 104), (388, 27), (463, 104), (539, 27), 
             (615, 104), (691, 27), (768, 104), (845, 27), 
             (920, 104)]


    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/Barrel.png").convert_alpha()
        self.rect = self.image.get_rect()

        idx = random.randint(0, len(Barrel.SLOTS)-1)
        self.rect.x = Barrel.SLOTS[idx][0]
        self.rect.y = Barrel.SLOTS[idx][1] + 24

        self.brokenImage = pygame.image.load("assets/Barrel_break.png").convert_alpha()
        self.isBroken = False
        self.step = 10


    def split(self):
        self.isBroken = True
        self.image = self.brokenImage
        x = self.rect.x; y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x - 10; self.rect.y = y


    def move(self):
        self.rect.y += self.step



    def draw(self, screen):
        screen.blit(self.image, self.rect)


