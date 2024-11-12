import sys
import time

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
        self.settings_init()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.buttons_init()

        pygame.display.set_caption("Alien Invasion")

        self.prev_time = time.time()
        self.dt = 0

    def buttons_init(self):
        """Setup buttons and button behaviour"""
        self.mouse_button_up = True
        standard_button_height = self.settings.screen_height/9
        standard_button_width = self.settings.screen_width/4

        #Make the play Button
        self.play_button = Button(self, "Play", 1, 1, standard_button_width , standard_button_height)

        #Make the upgrade buttons
        self.upgrade_buttons = []

        self.upgrade_buttons.append(Button(self, "Shot Size", 0.5, 0.35, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Penetration", 0.5, 1, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Shield", 0.5, 1.65, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Double Shot", 1, 0.35, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Max Shots", 1, 1, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Extra Life", 1, 1.65, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Speed", 1.5, 0.35, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Bounce", 1.5, 1, standard_button_width , standard_button_height))
        self.upgrade_buttons.append(Button(self, "Bombs", 1.5, 1.65, standard_button_width , standard_button_height))
        self.next_button = Button(self, "Next", 1.9, 1.8, standard_button_width , standard_button_height)

        #Make the enemy buttons
        self.add_enemy_button = Button(self, "Add Enemy", 1.5, 1, standard_button_width , standard_button_height)
        self.next_level_button = Button(self, "Next Level", 1.9, 1.8, standard_button_width , standard_button_height)

    def settings_init(self):
        """Setup any inital settings, including screen size, speed of objects"""
        self.fullscreen = self.settings.fullscreen

        if self.fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        #Setup speed/scale of objects relevent to the screen size, so they're always consistent.
        self.settings.alien_speed = self.settings.screen_width / 20
        self.settings.fleet_drop_speed = self.settings.screen_height / 40
        self.settings.bullet_width = self.settings.screen_width /200
        self.settings.bullet_height = self.settings.screen_height / 100
        self.settings.bullet_speed = self.settings.screen_height

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
 
            if self.stats.game_active == 1: #1 - gameplay
                self.ship.update(self.dt)
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # Make the most recently drawn screen visible
            pygame.display.flip()

            self.delta_time()

    def delta_time(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def _check_events(self):
    # watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.mouse_button_up:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_up = True

    def _check_buttons(self, mouse_pos):
        if self.stats.game_active == 0: # 0 - main_menu
            self._check_play_button(mouse_pos)
            self.mouse_button_up = False
        elif self.stats.game_active == 1: # 1 - gameplay
            self.mouse_button_up = False
        elif self.stats.game_active == 2: # 2 - upagrade_screen
            self._check_upgrade_buttons(mouse_pos)
            self.mouse_button_up = False
        elif self.stats.game_active == 3: # 3 - enemy_screen
            self._check_enemy_buttons(mouse_pos)
            self.mouse_button_up = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the play button"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked:
            self._start_game()

    def _check_upgrade_buttons(self, mouse_pos):
        for value in range(len(self.upgrade_buttons)):
            upgrade_button_clicked = self.upgrade_buttons[value].rect.collidepoint(mouse_pos)
            if upgrade_button_clicked:
                #Todo: upgrade system
                if value == 0:
                    self.settings.bullet_width *= 1.2
                    self.settings.bullet_height *= 1.1
                if value == 1:
                    self.settings.bullet_penetration += 1
                if value == 2:
                    print("Shield")
                if value == 3:
                    print("Double Bullets")
                if value == 4:
                    self.settings.bullets_allowed += 1
                if value == 5:
                    self.ships_left += 1
                if value == 6:
                    self.settings.ship_speed += 0.2
                if value == 7:
                    self.settings.bullet_bounce = True
                if value == 8:
                    print("Bombs")


        next_button_clicked = self.next_button.rect.collidepoint(mouse_pos)
        if next_button_clicked:
            self.enemy_screen()

    def _check_enemy_buttons(self, mouse_pos):
        add_enemy_button_clicked = self.add_enemy_button.rect.collidepoint(mouse_pos)
        if add_enemy_button_clicked:
            print("Add Enemy Button Clicked") #Todo: Extra Enemies system
        next_level_button_clicked = self.next_level_button.rect.collidepoint(mouse_pos)
        if next_level_button_clicked:
            self.next_level()

    def _start_game(self):
         #Reset game stats
        self.stats.reset_stats()
        self.stats.game_active = 1 # 1 - gameplay
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        time.sleep(0.2)

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
        elif event.key == pygame.K_p and self.stats.game_active == 0: #0 - main_menu
            self._start_game()


    def _check_keyup_events(self, event):
        """respons to key relseases"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_bullets(self):
        self.bullets.update(self.dt)

        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                if self.settings.bullet_bounce == True:
                    bullet.bullet_bounced = True
                else:
                    self.bullets.remove(bullet)
            if bullet.rect.top >= self.settings.screen_height:
                    self.bullets.remove(bullet)

                #print(len(self.bullets))   #Debug: Check bullet count (bullets should be added when fired and removed once offscreen)

        self._check_bullet_alien_collisons()



    def _check_bullet_alien_collisons(self):        
        #Check for any bullets that have hit aliens
        #If so alien + bullet need to be removed
        collisionsAlt = pygame.sprite.groupcollide(self.aliens, self.bullets, False, False) #Need to grab bullets that are colliding to handle bullet penetration
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True) #need to grab aliens colliding to handle damage / score generation
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if collisionsAlt:
            for bullets in collisionsAlt.values():
                i = 0
                remove = []
                j = 0
                while j < len(bullets):
                    if bullets[j].bullet_penetration == 0:
                        if bullets[j] is not remove:
                            remove.append(bullets[j])
                    elif bullets[j].bullet_penetration > 0:
                        bullets[j].bullet_penetration -= 1
                    j += 1
                for bullet in remove:
                    self.bullets.remove(bullet)
                remove = []


        if not self.aliens:
            #Destroy existing bullets
            self.bullets.empty()
            self.upgrade_screen()

    def upgrade_screen(self):
        """Upgrade Alien Craft screen"""
        self.stats.game_active = 2 # 2 = upgrade_screen
        pygame.mouse.set_visible(True)

    def enemy_screen(self):
        """Enemy Screen - for adding more enemies to the next level"""
        self.stats.game_active = 3 # 3 = enemy_screen
        pygame.mouse.set_visible(True)


    def next_level(self):
        self.stats.game_active = 1 # 1 - gameplay
        pygame.mouse.set_visible(False)

        #create new fleet
        self._create_fleet()
        self.settings.increase_speed()

        #increase level
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """Update pos of aliens"""
        self._check_fleet_edges()
        self.aliens.update(self.dt)
        self._check_alien_ship_collisons()
        self._check_aliens_bottom()

        #Update enemies left UI
        self.stats.enemies_left = len(self.aliens)
        self.sb.prep_enemies()

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
            time.sleep(0.5)
        else:
            self.stats.game_active = 0 #main_menu
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
        available_space_x = self.settings.screen_width - (5 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        #Determine how many rows of aliens fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

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

        #Draw play button if game_state is main_menu
        if self.stats.game_active == 0: # 0 - main_menu
            self.play_button.draw_button()

        #Draw upgrade screen if game_state is upgrade_screen
        if self.stats.game_active == 2: # 2 - upgrade_screen
            for value in range(len(self.upgrade_buttons)):
                self.upgrade_buttons[value].draw_button() #Draw this for now, but it shouldn't work
            self.next_button.draw_button() #Draw this for now, but it shouldn't work


        #Draw the enemy screen if game_state is enemy_screen
        if self.stats.game_active == 3: # 3 - enemy_screen
            self.add_enemy_button.draw_button() #Draw this for now, but it shouldn't work
            self.next_level_button.draw_button() #Draw this for now, but it shouldn't work

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