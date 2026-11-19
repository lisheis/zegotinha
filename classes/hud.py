import pygame

from constants import MAX_LIVES, SCREEN_WIDTH
from classes.text import Text
from utils.helpers import load_image

HUD_HEIGHT = 50


class Hud:
    """Barra do topo: vida, vacinas e tempo (igual a imagem de referencia)."""

    def __init__(self):
        self.text = Text(0, 0, size=26, bold=True)

    def draw(self, screen, player, time_left):
        # faixa azul com degrade
        for y in range(HUD_HEIGHT):
            t = y / HUD_HEIGHT
            color = (int(40 + 30 * t), int(110 + 40 * t), int(200 + 30 * t))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
        pygame.draw.line(screen, (20, 50, 110), (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT), 2)

        self.text.y = 10
        self.text.x = 18
        self.text.display(screen, f"LIFE: {player.lives}", shadow=True)
        full, empty = load_image("heart_full.png"), load_image("heart_empty.png")
        for i in range(MAX_LIVES):
            if full and empty:
                screen.blit(full if i < player.lives else empty, (128 + i * 28, 14))
            else:
                color = (220, 50, 50) if i < player.lives else (90, 60, 60)
                pygame.draw.circle(screen, color, (140 + i * 28, 26), 10)

        self.text.x = 330
        self.text.display(screen, f"VACCINES: {player.ammo}", shadow=True)
        icon = load_image("item_syringe.png")
        if icon:
            for i in range(min(player.ammo, 6)):
                screen.blit(icon, (530 + i * 22, 12))

        self.text.x = SCREEN_WIDTH - 160
        self.text.display(screen, f"TIME: {max(0, int(time_left))}", shadow=True)
