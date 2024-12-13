import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    """A class to represent a Meteor enemy"""

    def __init__(self, ai_game):
        """initialize the meteor and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        #Load the meteor image and set it's rect attribute
        self.image = pygame.image.load('images/alien.bmp') #Need to replace this image with a meteor
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width / 25, self.settings.screen_height / 20))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        #Strat the meteor at the top of the screen somewhere randomly
        self.y = float(self.rect.y)

    def update(self, dt):
        """Move the meteor to the bottom of the screen"""
        self.y += (self.settings.alien_speed * dt) #Todo: setup self.settings.meteor_speed
        self.rect.y = self.y