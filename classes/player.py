import pygame

from constants import (GRAVITY, GROUND_Y, INVULNERABLE_FRAMES, JUMP_FORCE, MAX_LIVES,
                       PLAYER_COLOR, PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_X, START_AMMO)
from classes.game_object import GameObject
from utils.helpers import load_image


class Player(GameObject):
    """Ze Gotinha: fica parado no eixo X, so pula. O cenario e que corre."""

    def __init__(self):
        super().__init__(PLAYER_X, GROUND_Y - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_COLOR)
        self.vy = 0
        self.on_ground = True
        self.lives = MAX_LIVES
        self.ammo = START_AMMO
        self.invulnerable = 0
        self.frames = 0

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

    def take_hit(self):
        if self.invulnerable == 0:
            self.lives -= 1
            self.invulnerable = INVULNERABLE_FRAMES

    def collect(self, item):
        self.ammo += item.ammo

    def update(self, obstacles, platforms):
        """Aplica gravidade e pousa no chao, em obstaculos ou em plataformas.
        Bater de lado em um obstaculo do chao tira vida e o remove.
        Retorna a plataforma em que o Ze bateu a cabeca (ou None)."""
        self.frames += 1
        if self.invulnerable > 0:
            self.invulnerable -= 1

        prev_top = self.y
        prev_bottom = self.y + self.height
        self.vy += GRAVITY
        self.y += self.vy
        bottom = self.y + self.height

        # cabecada por baixo de um bloco
        bumped = None
        if self.vy < 0:
            for pl in platforms:
                overlaps_x = self.x + 8 < pl.x + pl.width and self.x + self.width - 8 > pl.x
                if overlaps_x and prev_top >= pl.y + pl.height - 6 and self.y < pl.y + pl.height:
                    self.y = pl.y + pl.height
                    self.vy = 0
                    bumped = pl
                    break
            bottom = self.y + self.height

        support = GROUND_Y
        for ob in obstacles + platforms:
            overlaps_x = self.x + self.width > ob.x + 4 and self.x < ob.x + ob.width - 4
            if overlaps_x and self.vy >= 0 and prev_bottom <= ob.y + 8 and bottom >= ob.y:
                support = min(support, ob.y)

        if bottom >= support:
            self.y = support - self.height
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        player_rect = pygame.Rect(self.get_rect())
        for pl in platforms:
            pl_rect = pygame.Rect(pl.get_rect())
            if player_rect.colliderect(pl_rect):
                if player_rect.bottom > pl_rect.top + 8 and player_rect.top < pl_rect.bottom - 8:
                    if self.vy < 0:
                        self.vy = 0

        for ob in obstacles[:]:
            ob_rect = pygame.Rect(ob.get_rect())
            if player_rect.colliderect(ob_rect) and player_rect.bottom > ob_rect.top + 8:
                self.take_hit()
                obstacles.remove(ob)

        return bumped

    def draw(self, screen):
        # pisca enquanto esta invulneravel
        if self.invulnerable > 0 and (self.invulnerable // 5) % 2 == 0:
            return
        if not self.on_ground:
            image = load_image("player_jump.png")
        else:
            image = load_image("player_run1.png" if (self.frames // 8) % 2 == 0 else "player_run2.png")

        if image:
            screen.blit(image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, self.get_rect(), border_radius=10)
