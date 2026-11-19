import pygame

from constants import BLOCK_SIZE, OBSTACLE_COLOR
from classes.game_object import GameObject
from utils.helpers import load_image


class Platform(GameObject):
    """Bloco suspenso. Da pra subir em cima e bater a cabeca por baixo.
    O bloco '?' solta uma vacina na primeira cabecada."""

    def __init__(self, x, y, question=False):
        super().__init__(x, y, BLOCK_SIZE, BLOCK_SIZE, OBSTACLE_COLOR)
        self.question = question
        self.used = False
        self.bump = 0  # frames da animacao de "pulinho" do bloco

    def update(self, scroll_speed):
        self.x -= scroll_speed
        if self.bump > 0:
            self.bump -= 1

    def hit_from_below(self):
        """Retorna True se o bloco soltou um item."""
        self.bump = 8
        if self.question and not self.used:
            self.used = True
            return True
        return False

    def is_offscreen(self):
        return self.x + self.width < 0

    def draw(self, screen):
        if self.used:
            name = "block_used.png"
        elif self.question:
            name = "block_question.png"
        else:
            name = "block_brick.png"
        image = load_image(name)
        dy = -(6 * (4 - abs(self.bump - 4)) // 4) if self.bump > 0 else 0  # sobe e desce
        if image:
            screen.blit(image, (self.x, self.y + dy))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y + dy, self.width, self.height))
