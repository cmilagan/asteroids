from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_IMAGE,
    )
from shot import Shot
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.rotation = 0
        self.cooldown = 0
        self.__lives = 3
        self.trail = []  # (pos, life)

    def get_lives(self):
        return self.__lives

    def lose_life(self):
        self.__lives -= 1

    def gain_life(self):
        self.__lives += 1

    def draw(self, screen, color, points, width):
        # draw the purple trail
        for pos, life in self.trail:
            alpha = max(0, min(255, int(255 * (life / 0.3))))
            trail_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (180, 0, 180, alpha), (4, 4), 4)
            screen.blit(trail_surf, (pos.x - 4, pos.y - 4))

        # Flip the image vertically so it starts upside down
        flipped_image = pygame.transform.flip(self.image, False, True)
        rotated_image = pygame.transform.rotate(flipped_image, -self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown = max(0, self.cooldown - dt)

        moving_forward = keys[pygame.K_w]

        if keys[pygame.K_w]:
            self.move(dt)
            self._add_trail()
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        for i in range(len(self.trail) - 1, -1, -1):
            pos, life = self.trail[i]
            life -= dt
            if life <= 0:
                self.trail.pop(i)
            else:
                self.trail[i] = (pos, life)

    def _add_trail(self):
        back_dir = pygame.Vector2(0, 1).rotate(self.rotation) * -1
        trail_pos = self.position + back_dir * (PLAYER_RADIUS + 4)
        self.trail.append((trail_pos, 0.3))

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.cooldown > 0:
            return
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
