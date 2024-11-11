import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """initilize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.fullscreen = self.settings.fullscreen

        if self.fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play Button
        self.play_button = Button(self, "Play")

        pygame.display.set_caption("Alien Invasion")


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
 
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # Make the most recently drawn screen visible
            pygame.display.flip()

    def _check_events(self):
    # watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
         #Reset game stats
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        sleep(0.2)

        #Get rid of aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        #Create a new fleet and center ship
        self._create_fleet()
        self.ship.center_ship()

        #Hide the mouse cursor.
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respons to key presses."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """respons to key relseases"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_bullets(self):
        self.bullets.update()

        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
                #print(len(self.bullets))   #Debug: Check bullet count (bullets should be added when fired and removed once offscreen)

        self._check_bullet_alien_collisons()



    def _check_bullet_alien_collisons(self):        
        #Check for any bullets that have hit aliens
        #If so alien + bullet need to be removed
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) #Upgrade idea: Powerful bullets: set arg 3 to False and bullets don't get destroyed when they hit an alien
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Update pos of aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_alien_ship_collisons()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have hit the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                #print("An alien has reached the bottom of the screen, the ship has been hit") #Debug: Check for ship being hit
                break

    def _check_alien_ship_collisons(self):
        #Check if the aliens have hit the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            #print("Ship has been hit by an alien!") #Debug: Check for ship being hit

    def _ship_hit(self):
        # Decrease ships left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any aliens + bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """Respon to a alien hitting the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Create a fleet of aliens"""
        #Make a alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        #Determine how many rows of aliens fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2* alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_screen(self):
        """Redraw the screen during each pass through the loop."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #Draw the scoreboard
        self.sb.show_score()


        #Draw play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Creates a new bullet and adds it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



if __name__ =='__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()