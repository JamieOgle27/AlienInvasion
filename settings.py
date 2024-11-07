class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        self.fullscreen = True

        # Ship settings
        self.ship_speed = 1.1
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.1
        self.bullet_width = 3 #Upgrade idea: Thick bullets (increase bullet width)
        self.bullet_height = 15
        self.bullet_color = (20,20,20)
        self.bullets_allowed = 4

        # Alien settings
        self.alien_speed = 1.1
        self.fleet_drop_speed = 14
        #Fleet direction of 1 == right; -1 == left
        self.fleet_direction = 1