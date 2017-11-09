import pygame
from pygame.sprite import Group
import game_func as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button

def run_game():
    #initialize
    pygame.init()
    ai_settings = Settings()

    #screen
    screen = pygame.display.set_mode((ai_settings.screen_width,
                ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invasion")

    #Erstellt die PlaySchaltfläche
    play_button = Button(ai_settings, screen, "Play")

    #Erstellt eine Instanz zur Speicherung von Statistiken
    stats = GameStats(ai_settings)

    #ship
    ship = Ship(ai_settings, screen)
    #bullets
    bullets = Group()
    #Aliens
    aliens = Group()

    #Erstellt die Invasionflotte
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Hauptschleife
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens,
            bullets)
        if stats.game_active == True:
            ship.update_self()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens,
            play_button)

run_game()
