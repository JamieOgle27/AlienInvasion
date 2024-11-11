class GameStats:
    """Tracks stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start game in active state
        self.game_active = 0
        #0 - main_menu
        #1 - gameplay
        #2 - upgrade_screen
        #3 - enemy_screen

        self.high_score = 0 #Only initilize this once then it should never be reset!
        self.enemies_left = 0 #Doesn't need reset as it's setup when the fleet is created

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
