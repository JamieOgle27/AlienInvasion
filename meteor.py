import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    """A class to represent a Meteor enemy"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the meteor image and set it's rect attribute
        self.image = pygame.image.load('images/alien.bmp') #Need to replace this image with a meteor
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width / 25, self.settings.screen_height / 20))
        self.rect = self.image.get_rect()