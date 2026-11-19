import pygame

from constants import GROUND_Y, OBSTACLE_COLOR
from classes.game_object import GameObject
from utils.helpers import load_image


class Obstacle(GameObject):
    """Bloco no chao. Da pra pular por cima dele; bater de lado tira vida."""

    def __init__(self, x, width=50, height=50):
        super().__init__(x, GROUND_Y - height, width, height, OBSTACLE_COLOR)

    def update(self, scroll_speed):
        self.x -= scroll_speed

    def is_offscreen(self):
        return self.x + self.width < 0

    def draw(self, screen):
        tile = load_image("block_brick.png")
        if not tile:
            pygame.draw.rect(screen, self.color, self.get_rect())
            return

        # repete o bloco de 40x40 ate preencher o obstaculo, alinhado por baixo
        area = pygame.Rect(self.get_rect())
        screen.set_clip(area)
        size = tile.get_width()
        for tx in range(area.left, area.right, size):
            for ty in range(area.bottom - size, area.top - size, -size):
                screen.blit(tile, (tx, ty))
        screen.set_clip(None)
