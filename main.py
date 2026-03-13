import pygame
import sys
import time
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LINE_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def load_high_score():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                content = f.read().strip()
                if content:
                    return int(content)
        except (ValueError, IOError):
            pass
    return 0

def save_high_score(high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

def check_quit(game):
    for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                return

def check_end_conditions(player, asteroids, screen):
    end_font = pygame.font.SysFont("Arial", 64)
    for asteroid in asteroids:
        if player.collides_with(asteroid):
            asteroid.kill()
            player.lose_life()
            if player.get_lives() <= 0:
                return True
    return False

def print_final_score(score, high_score, screen):
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    end_font = pygame.font.SysFont("Arial", 64)
    end_text = end_font.render("Game Over!", True, "white")
    text_rect = end_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(end_text, text_rect)
    final_score_font = pygame.font.SysFont("Arial", 32)
    final_score_text = final_score_font.render(f"Final Score: {score}", True, "white")
    text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(final_score_text, text_rect)
    high_score_text = final_score_font.render(f"High Score: {high_score}", True, "white")
    text_rect = high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80))
    screen.blit(high_score_text, text_rect)
    pygame.display.flip()
    time.sleep(2)
    sys.exit()

def check_shot_collisions(shots, asteroids):
    increment_score = False
    for asteroid in asteroids:
        for shot in shots:
            if shot.collides_with(asteroid):
                increment_score = True
                log_event("asteroid_shot")
                asteroid.split()
                shot.kill()
    return increment_score

def check_asteroid_collisions(asteroids):
    for i, asteroid1 in enumerate(asteroids):
        for asteroid2 in list(asteroids)[i+1:]:
            if asteroid1.collides_with(asteroid2):
                # Elastic collision response
                normal = (asteroid2.position - asteroid1.position).normalize()

                # Masses proportional to radius
                mass1 = asteroid1.radius
                mass2 = asteroid2.radius

                # Velocity components along normal
                v1_n = asteroid1.velocity.dot(normal)
                v2_n = asteroid2.velocity.dot(normal)

                # Relative velocity along normal
                rel_vel_n = v2_n - v1_n

                # Do not resolve if velocities are separating
                if rel_vel_n > 0:
                    continue

                # Elastic collision formulas
                new_v1_n = (v1_n * (mass1 - mass2) + 2 * mass2 * v2_n) / (mass1 + mass2)
                new_v2_n = (v2_n * (mass2 - mass1) + 2 * mass1 * v1_n) / (mass1 + mass2)

                # Update velocities: tangential components stay the same
                asteroid1.velocity += (new_v1_n - v1_n) * normal
                asteroid2.velocity += (new_v2_n - v2_n) * normal

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # settings
    pygame.init()
    pygame.font.init()
    score_font = pygame.font.SysFont("Arial", 24)
    lives_font = pygame.font.SysFont("Arial", 24)
    high_score_font = pygame.font.SysFont("Arial", 24)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0 # delta time in seconds

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # set containers for each sprite class
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    score = 0
    high_score = load_high_score()
    asteroid_field = AsteroidField()
    # game loop
    while True:
        log_state()
        check_quit(pygame)
        screen.fill("black")
        updatable.update(dt)

        check_asteroid_collisions(asteroids)

        if check_end_conditions(player, asteroids, screen):
            print_final_score(score, high_score, screen)

        if check_shot_collisions(shots, asteroids): score += 1

        lives_text = lives_font.render(f"Lives: {player.get_lives()}", True, "white")
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
        score_text = score_font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        high_score_text = high_score_font.render(f"High Score: {high_score}", True, "white")
        screen.blit(high_score_text, (10, 40))
        for drawable_sprite in drawable:
            drawable_sprite.draw(screen, "white", drawable_sprite.radius, LINE_WIDTH)

        pygame.display.flip()
        clock.tick(60)
        dt = clock.get_time() / 1000.0


if __name__ == "__main__":
    main()
