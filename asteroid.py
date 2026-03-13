import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

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