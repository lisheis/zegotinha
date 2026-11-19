import pygame

from constants import GROUND_Y
from classes.game_object import GameObject
from classes.text import Text
from utils.helpers import load_image


class Goal(GameObject):
    """UPA 24h: chegar nela termina a fase."""

    def __init__(self, x):
        width, height = 260, 170
        super().__init__(x, GROUND_Y - height, width, height, (70, 110, 190))
        self.label = Text(0, 0)

    def update(self, scroll_speed):
        self.x -= scroll_speed

    def draw(self, screen):
        flag = load_image("flag.png")
        if flag:
            screen.blit(flag, (self.x - 50, self.y + self.height - flag.get_height()))
        image = load_image("upa.png")
        if image:
            screen.blit(image, (self.x, self.y))
            return
        pygame.draw.rect(screen, self.color, self.get_rect())
        pygame.draw.rect(screen, (240, 240, 240), (self.x + 30, self.y + 30, 200, 40))
        pygame.draw.rect(screen, (255, 220, 100), (self.x + 100, self.y + 100, 60, 70))
        self.label.x = self.x + 60
        self.label.y = self.y + 36
        self.label.color = (30, 90, 40)
        self.label.display(screen, "UPA 24h +")
