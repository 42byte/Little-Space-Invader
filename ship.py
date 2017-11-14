import pygame

class Ship():
    """Create ships properties"""

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        #load picture
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Ship placement in the bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        #moving flag
        self.moving_right = False
        self.moving_left = False

    def update_self(self):
        """Update Ships Position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #aktualisiert self rect centerx
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx
