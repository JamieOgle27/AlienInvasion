import pygame
from random import uniform as randfloat
from random import randrange
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
        self.image = pygame.image.load('images/meteor.bmp') #Need to replace this image with a meteor
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width / 25, self.settings.screen_height / 20))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

        #Start the meteor at the top of the screen, at a random position
        self.x = randrange(0, self.settings.screen_width)
        self.rect.x = self.x
        self.y = self.screen_rect.top - self.image.get_size()[1]
        self.rect.y = self.y
        self.x_direction = randfloat(-0.6, 0.6)

    def update(self, dt):
        """Update meteor position every frame"""

        #Loop the meteor if it's gone off screen, otherwise update it's position as normal
        if not self.loop_meteor():
            self.y += (self.settings.alien_speed * dt) #Todo: setup self.settings.meteor_speed
            self.x += (self.settings.alien_speed * self.x_direction * dt)

        self.rect.y = self.y
        self.rect.x = self.x

    def loop_meteor(self):
        """move the meteor to the top of the screen if it's at the bottom"""
        if self.check_bottom():
            self.y = self.screen_rect.top - self.image.get_size()[1]
            return True

    def check_bottom(self):
        """Returns True if alien hits the bottom of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.bottom - self.image.get_size()[1] >= screen_rect.bottom:
            print("bottom")
            return True