import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_SMALL_IMAGE, ASTEROID_LARGE_IMAGE
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        if self.radius == ASTEROID_MIN_RADIUS:
            self.image = pygame.image.load(ASTEROID_SMALL_IMAGE).convert_alpha()
        elif self.radius == ASTEROID_MAX_RADIUS:
            self.image = pygame.image.load(ASTEROID_LARGE_IMAGE).convert_alpha()
        else:
            self.image = pygame.image.load(ASTEROID_LARGE_IMAGE).convert_alpha()

    def draw(self, screen, color, radius, width):
        if self.radius == 20:
            scale = 60
        elif self.radius == 40:
            scale = 100
        elif self.radius == 60:
            scale = 130
        else:
            scale = int(2 * self.radius)  # fallback
        scaled_image = pygame.transform.scale(self.image, (scale, scale))
        rect = scaled_image.get_rect(center=self.position)
        screen.blit(scaled_image, rect)

    def update(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        if isinstance(other, Asteroid):
            return super().collides_with(other)
        return False

    def split(self):
        self.kill()
        new_radius = None
        if self.radius <= 20:
            return
        elif self.radius == 40:
            new_radius = ASTEROID_MIN_RADIUS
        elif self.radius == 60:
            new_radius = 2 * ASTEROID_MIN_RADIUS

        new_velocity1 = self.velocity.rotate(random.uniform(20, 50))
        new_velocity2 = self.velocity.rotate(random.uniform(-20, 50))
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = new_velocity1
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = new_velocity2
        log_event("asteroid_split")
        return [asteroid1, asteroid2]