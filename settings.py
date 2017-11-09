class Settings():
    """A class to store all settings attributes"""

    def __init__(self):
        """Initialize the settings"""
        self.screen_width = 1200
        self.screen_heigth = 600
        self.bg_color = (230, 230, 230)

        #Schiffseinstellungen
        self.ship_speed_factor = 1.5
        self.ship_limit = 1

        #bullets
        self.bullet_speed_factor = 2.5
        self.bullet_width = 300
        self.bullet_heigth = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #Invasionschiffe Einstellungen
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 50
        #Der Wert 1 für fleet_direction bedeutet "nach rechts", -1 "nach links"
        self.fleet_direction = 1
