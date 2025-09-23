
import pygame
from pygame.locals import *
from pygame.font import *

import pickle, os
from operator import itemgetter


# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)



class HighScores:

  def __init__(self, scrWidth, scrHeight):
    self.fnm = "highscores.pkl"
    self.scrWidth = scrWidth
    self.scrHeight = scrHeight
    self.font = pygame.font.Font(None,30)
    self.scores = []


    if os.path.isfile(self.fnm):
        with open(self.fnm, "rb") as f:
            self.scores = pickle.load(f)
    else:
        self.scores = [("John", 15536), ("Andrew", 10000)]
  

  def add(self, name, score):
      self.scores.append((name, score))
      self.scores = sorted(self.scores, 
                                key=itemgetter(1), reverse=True)[:10]
      with open(self.fnm, 'wb') as f:
          pickle.dump(self.scores, f)


  def draw(self, screen):
      self.printText(screen, "High Scores", 40, 150)
      idx = 1
      for name, score in self.scores:
          self.printText(screen, "%d) %s %d"%(idx, name, score), 40, 175+25*idx)
          idx += 1
    


  def printText(self, screen, text, x, y):
      label = self.font.render(str(text)+'  ', True, WHITE)
      textRect = label.get_rect()
      textRect.x = x 
      textRect.y = y
      screen.blit(label, textRect)
        

  def printScores(self):
      print("Data in", self.fnm,":")
      idx = 1
      for name, score in self.scores:
          print("%d) %s %d" % (idx,name,score))
          idx += 1

