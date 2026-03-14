import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.hitbox_radius = SHOT_RADIUS * 0.9  # slightly smaller hitbox

    def draw(self, screen, color, radius, width):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        other_radius = getattr(other, 'hitbox_radius', other.radius)
        distance = self.position.distance_to(other.position)
        return distance < (self.hitbox_radius + other_radius)
