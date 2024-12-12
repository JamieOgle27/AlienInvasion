class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games  settings."""
        # Screen settings
        self.screen_width = 500
        self.screen_height = 500
        self.bg_color = (255, 255, 255)
        self.fullscreen = False

        # Ship settings
        self.ship_speed = 220
        self.ship_limit = 2

        # Bullet settings
        self.bullet_speed = 0
        self.bullet_width = 0  
        self.bullet_height = 0
        self.bullet_color = (20,20,20)
        self.bullets_allowed = 3
        self.bullet_penetration = 2 #How many aliens a bullet can penetrate before being destroyed
        self.bullet_bounce = False

        # Alien settings
        self.alien_speed = 0
        self.fleet_drop_speed = 0
        #Fleet direction of 1 == right; -1 == left
        self.fleet_direction = 1
        self.speedup_scale = 1.1 #Increase in speed per level
        self.alien_points = 50
        self.score_scale = 1.2 #How quickly alien_points increases per level
        self.number_of_rows = 3

    def increase_speed(self):
        """Increase speed settings and alien points"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

