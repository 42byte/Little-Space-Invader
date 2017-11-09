import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class that manages bullets"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ships current position"""
        super().__init__()
        self.screen = screen

        #Erstellt ein Geschossrechteck bei (0,0) und legt dann die richtige
        #Position fest
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_heigth)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #Speichert die Position des Geschosses als float
        self.y = float(self.rect.y)
        #Färbt das Gweschoss ein
        self.color = ai_settings.bullet_color
        #Setzt die Geschwindigkeit des Geschosses
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        #Aktualisierung der float
        self.y -= self.speed_factor
        #aktualisiert the rect
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
