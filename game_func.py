import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown(event, ai_settings, screen, stats, ship, aliens, bullets):
    """Check keydown events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)


def check_keyup(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens,
    bullets):
    """check user input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, stats, ship, aliens,
                bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship,
    aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, ship, aliens, bullets):
    #Blendet den Mauszeiger aus
    pygame.mouse.set_visible(False)

    #Setzt die Spielstatistik zurück
    stats.reset_stats()
    stats.game_active = True

    #Leert die Liste der Aliens und Geschosses
    aliens.empty()
    bullets.empty()

    #Erstellt eine neue Flotte und zentriert das eigene Schiff
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, bullets, aliens,
        play_button):
    """Updates the screen"""
    screen.fill(ai_settings.bg_color)

    #Zeichnet alle Geschosse hintet dem Schiff und den Außerirdischen neues
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #Zeichnet die Play Schaltfläche bei inaktivem Spiel
    if not stats.game_active:
        play_button.draw_button()

    #update frame
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update Position of the bullet and get rid of old bullets"""
    #aktualisiert die Position
    bullets.update()
    #entfernt die verschwundenen Geschosse
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
    """Responds to bullet-alien collision"""
    #Prüft ob irgendwelche Geschosse ein Schiff getroffen haben
    #Wenn ja, werden beide Objekte entfernt
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        #Zerstört alle vorhandenen Geschosse und erstellt eine neue Flotte
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bulletif limit is not reached yet"""
    #Erstellt ein neues Geschoss und fügt es zur Gruppe Bullets hinzu
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_heigth -
                        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an Alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    #Erstellt ein Invasionschiff und ermittelt die Anzahl der Invassionsschiffe
    #pro Reihe. Die Abstände zwischen den Invasionschiffen entsprechen
    #jeweils einer Schiffsbreite
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)

    #Erstellt die erste Reihe von aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Erstellt ein Invasionschiff und platziert es in der Reihe
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge, and then
    Update the position of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)

    #Prüft auf Kollisionen zwischen eigenem Shiff und den Aliens
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    aliens.update()
    #Prüft auf Invasionsschiffe, die das untere Ende des Bildschirms erreichen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens,bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond approprately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to a ship being hit"""

    if stats.ships_left > 0:
        #Verringert die Anzahl der verbliebenden Leben
        stats.ships_left -= 1

        #Leert die Liste der Invasoren und Geschosse
        aliens.empty()
        bullets.empty()

        #Erstellt eine neue Flotte und zentriert das eigene Schiff
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #gleiche reaktion wie bei einer Kollision mit einem Schiff
            ship_hit(ai_settings, stats, screen,ship, aliens, bullets)
            break
