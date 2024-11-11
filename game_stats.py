class GameStats:
    """Tracks stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start game in active state
        self.game_active = False 
        self.high_score = 0 #Only initilize this once then it should never be reset!


    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.enemies_left = 0