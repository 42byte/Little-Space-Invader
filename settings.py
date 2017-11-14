class Settings():
    """A class to store all settings attributes"""

    def __init__(self):
        """Initialize the games static settings"""
        self.screen_width = 1200
        self.screen_heigth = 600
        self.bg_color = (230, 230, 230)

        #Schiffseinstellungen
        self.ship_limit = 1

        #bullets

        self.bullet_width = 300
        self.bullet_heigth = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #Invasionschiffe Einstellungen
        self.fleet_drop_speed = 20

        #Stärke der Beschleunigung des Spiels
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #Der Wert 1 für fleet_direction bedeutet "nach rechts", -1 "nach links"
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the games speed"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale