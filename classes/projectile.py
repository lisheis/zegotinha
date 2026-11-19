import pygame

from constants import PROJECTILE_HEIGHT, PROJECTILE_SPEED, PROJECTILE_WIDTH, SCREEN_WIDTH
from classes.game_object import GameObject
from utils.helpers import load_image


class Projectile(GameObject):
    """Vacina arremessada pelo Ze Gotinha."""

    def __init__(self, x, y):
        super().__init__(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT, (150, 200, 255))

    def update(self):
        self.x += PROJECTILE_SPEED

    def is_offscreen(self):
        return self.x > SCREEN_WIDTH

    def draw(self, screen):
        image = load_image("projectile.png")
        if image:
            screen.blit(image, (self.x, self.y))
            return
        pygame.draw.rect(screen, self.color, self.get_rect(), border_radius=4)
