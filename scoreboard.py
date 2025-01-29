import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring info
        self.text_color = (30,30,30)
        self.font_size = ai_game.settings.screen_width/20
        self.font = pygame.font.SysFont(None, int(self.font_size))
        self.vertical_offset = self.settings.screen_height / 60
        self.horizontal_offset = self.settings.screen_width / 80

        #Prep initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_enemies()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = str(f"Score: {score_str}")
        self.score_image = self.font.render(score_str, True, self.text_color)
        #self.score_image = pygame.transform.scale(self.score_image, (self.settings.screen_width / 5, self.settings.screen_height / 25))


        #Display the score in the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.horizontal_offset
        self.score_rect.top = self.vertical_offset

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        high_score_str = str(f"High Score: {high_score_str}")
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        #self.high_score_image = pygame.transform.scale(self.high_score_image, (self.settings.screen_width / 5, self.settings.screen_height / 25))


        #Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level number into a rendered image"""
        level_str = str(f"Level: {self.stats.level}")
        self.level_image = self.font.render(level_str, True, self.text_color)
        #self.level_image = pygame.transform.scale(self.level_image, (self.settings.screen_width / 5, self.settings.screen_height / 25))


        #Position the level no below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + (self.settings.screen_height / 40)

    def prep_ships(self):
        """Display remaning ships"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = self.horizontal_offset + ship_number * ship.rect.width
            ship.rect.y = self.vertical_offset
            self.ships.add(ship)

    def prep_enemies(self):
        """Display remianing enemeies"""
        enemies_str = str(f"Enemies: {self.stats.enemies_left}")
        self.enemy_image = self.font.render(enemies_str, True, self.text_color)
        #self.enemy_image = pygame.transform.scale(self.enemy_image, (self.settings.screen_width / 5, self.settings.screen_height / 25))


        """Position enemies left beneath the ships left"""
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.screen_rect.left + self.horizontal_offset #This needs an offset or is drawn against the border of the screen
        self.enemy_rect.top = self.score_rect.bottom + self.vertical_offset #Use score as a refrence for .y position to keep this in line with level text



    def show_score(self):
        """Draw score/level/ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.enemy_image, self.enemy_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()