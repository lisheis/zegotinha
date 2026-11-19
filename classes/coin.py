import pygame

from constants import ITEM_KINDS, ITEM_SIZE
from classes.game_object import GameObject
from utils.helpers import load_image


class Item(GameObject):
    """Coletavel: vacina e seringa dao municao, gotinha da vida."""

    def __init__(self, x, y, kind):
        data = ITEM_KINDS[kind]
        super().__init__(x, y, ITEM_SIZE, ITEM_SIZE, data["color"])
        self.kind = kind
        self.ammo = data.get("ammo", 0)
        self.life = data.get("life", 0)

    def update(self, scroll_speed):
        self.x -= scroll_speed

    def is_offscreen(self):
        return self.x + self.width < 0

    def draw(self, screen):
        image = load_image(f"item_{self.kind}.png")
        if image:
            screen.blit(image, (self.x, self.y))
            return
        pygame.draw.rect(screen, self.color, self.get_rect(), border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), self.get_rect(), 2, border_radius=6)
