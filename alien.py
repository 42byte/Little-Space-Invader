import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A Class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set itsstarting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Läd das Bild des Invasionschiffes und legt die rect attribute fest
        self.image = pygame.image.load("/home/mi/programming/Game_recent/images/alien.bmp")
        self.rect = self.image.get_rect()

        #Platziert jedes neue Invasionsschiff oben links auf dem Bildschirm
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Speichert die genaue Position desInvasionsschiffes
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at itscurrent location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right"""
        self.x += (self.ai_settings.alien_speed_factor *
                    self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
