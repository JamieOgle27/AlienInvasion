import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """initialize the alien and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the alien image and set it's rect attribute
        self.image = pygame.image.load('images/alien_purple.bmp')
        self.image = pygame.transform.scale(self.image, (self.settings.screen_width / 25, self.settings.screen_height / 20))
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's horizontal pos
        self.x = float(self.rect.x)

    def update(self, dt):
        """Move the aliens to the right."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction * dt)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien as at the edge of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right and self.settings.fleet_direction > 0:
            return True
        if self.rect.left <= 0 and self.settings.fleet_direction < 0:
            return True

    def check_bottom(self):
        """Returns True if alien hits the bottom of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.bottom >= screen_rect.bottom:
            return True

