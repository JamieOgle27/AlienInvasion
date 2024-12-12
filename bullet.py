import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, offset):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.rect.x += offset

        self.bullet_penetration = self.settings.bullet_penetration
        self.bullet_bounced = False

    def update(self, dt):
        """Move the bullet up the screen"""
        #Update the decimal position of the bullet
        if not self.bullet_bounced:
            self.y -= self.settings.bullet_speed * dt
        elif self.bullet_bounced:
            self.y += self.settings.bullet_speed * dt
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
