import pygame

from constants import ENEMY_KINDS, GROUND_Y
from classes.game_object import GameObject
from utils.helpers import load_image, wave


class Enemy(GameObject):
    """Virus. O tipo ('corona', 'zika', 'aedes') define cor, vida e velocidade."""

    def __init__(self, x, kind):
        data = ENEMY_KINDS[kind]
        size = data["size"]
        self.kind = kind
        self.hp = data["hp"]
        self.extra_speed = data["extra_speed"]
        self.flying = data["flying"]
        self.age = 0

        self.base_y = GROUND_Y - 110 if self.flying else GROUND_Y - size
        super().__init__(x, self.base_y, size, size, data["color"])

    def update(self, scroll_speed):
        self.age += 1
        self.x -= scroll_speed + self.extra_speed
        if self.flying:
            self.y = self.base_y + wave(self.age, 80) * 30

    def hit(self):
        self.hp -= 1
        return self.hp <= 0

    def is_offscreen(self):
        return self.x + self.width < 0

    def draw(self, screen):
        image = load_image(f"enemy_{self.kind}.png")
        if image:
            screen.blit(image, (self.x, self.y))
            return

        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)
        radius = self.width // 2
        pygame.draw.circle(screen, self.color, (cx, cy), radius)
        pygame.draw.circle(screen, WHITE_EYE, (cx - 7, cy - 4), 5)
        pygame.draw.circle(screen, WHITE_EYE, (cx + 7, cy - 4), 5)
        pygame.draw.circle(screen, (0, 0, 0), (cx - 7, cy - 4), 2)
        pygame.draw.circle(screen, (0, 0, 0), (cx + 7, cy - 4), 2)


WHITE_EYE = (255, 255, 255)
