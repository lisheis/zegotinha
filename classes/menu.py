import pygame

from constants import MENU_VOICE, NAME_MAX_LENGTH, RANKING_SHOW, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from classes.text import Text
from utils.helpers import play_sound
from utils.ranking import load_ranking

GOLD = (245, 195, 50)
SILVER = (195, 200, 215)
BRONZE = (205, 130, 70)


class Menu:
    """Tela inicial: digitar o nome, botao grande de JOGAR e o podio dos recordes."""

    def __init__(self, name=""):
        self.name = name
        self.ranking = load_ranking()
        self.button = pygame.Rect(70, 300, 380, 110)
        self.input_box = pygame.Rect(70, 200, 380, 58)
        self.warning = 0  # pisca o campo quando tenta jogar sem nome
        self.frames = 0
        play_sound(MENU_VOICE)  # "Cade o Ze Gotinha?"

    def handle_event(self, event):
        """Retorna True quando o jogador pede para comecar."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button.collidepoint(event.pos):
                return self.try_start()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.try_start()
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.name) < NAME_MAX_LENGTH:
                self.name += event.unicode
        return False

    def try_start(self):
        if self.name.strip():
            self.name = self.name.strip()
            return True
        self.warning = 60
        return False

    def draw(self, screen):
        self.frames += 1
        if self.warning > 0:
            self.warning -= 1

        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((10, 20, 50, 120))
        screen.blit(shade, (0, 0))

        Text(SCREEN_WIDTH // 2, 70, size=56, color=WHITE, bold=True).display(
            screen, "ZÉ GOTINHA", center=True, shadow=True)
        Text(SCREEN_WIDTH // 2, 120, size=26, color=(255, 230, 140), bold=True).display(
            screen, "A caminho da UPA", center=True, shadow=True)

        self.draw_name_input(screen)
        self.draw_button(screen)
        Text(260, 440, size=20).display(screen, "ESPAÇO: pular     X: jogar vacina", center=True, shadow=True)
        Text(260, 470, size=18, color=(255, 230, 140)).display(
            screen, "Chegue na UPA com o máximo de vacinas!", center=True, shadow=True)

        self.draw_podium(screen)

    def draw_name_input(self, screen):
        Text(self.input_box.x, self.input_box.y - 32, size=22, bold=True).display(
            screen, "Digite seu nome:", shadow=True)
        border = (240, 70, 70) if self.warning > 0 and (self.warning // 8) % 2 == 0 else (30, 60, 130)
        pygame.draw.rect(screen, (250, 250, 255), self.input_box, border_radius=10)
        pygame.draw.rect(screen, border, self.input_box, 4, border_radius=10)

        cursor = "|" if (self.frames // 30) % 2 == 0 else ""
        content = self.name + cursor if self.name else cursor
        Text(self.input_box.x + 16, self.input_box.y + 12, size=28, color=(30, 40, 80), bold=True).display(
            screen, content)

    def draw_button(self, screen):
        hover = self.button.collidepoint(pygame.mouse.get_pos())
        body = (70, 200, 90) if hover else (55, 180, 75)
        shadow = self.button.move(0, 8)
        pygame.draw.rect(screen, (25, 90, 40), shadow, border_radius=18)
        pygame.draw.rect(screen, body, self.button, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), self.button, 4, border_radius=18)
        Text(self.button.centerx, self.button.centery, size=56, bold=True).display(
            screen, "JOGAR", center=True, shadow=True)

    def draw_podium(self, screen):
        Text(720, 185, size=30, color=(255, 230, 140), bold=True).display(
            screen, "PÓDIO", center=True, shadow=True)

        base = 400
        # (posicao no ranking, x, altura, cor)
        places = [(1, 540, 140, SILVER), (0, 660, 180, GOLD), (2, 780, 105, BRONZE)]
        for index, x, height, color in places:
            block = pygame.Rect(x, base - height + 60, 120, height - 60)
            pygame.draw.rect(screen, color, block, border_radius=6)
            pygame.draw.rect(screen, (60, 50, 30), block, 3, border_radius=6)
            Text(block.centerx, block.y + 22, size=30, color=(60, 45, 20), bold=True).display(
                screen, f"{index + 1}º", center=True)
            if index < len(self.ranking):
                entry = self.ranking[index]
                Text(block.centerx, block.y - 44, size=20, bold=True).display(
                    screen, entry["name"], center=True, shadow=True)
                Text(block.centerx, block.y - 20, size=18, color=(190, 255, 190)).display(
                    screen, f"{entry['score']} vacinas", center=True, shadow=True)

        for i in range(3, RANKING_SHOW):
            if i < len(self.ranking):
                entry = self.ranking[i]
                Text(720, base + 22 + (i - 3) * 26, size=19).display(
                    screen, f"{i + 1}º  {entry['name']}  -  {entry['score']} vacinas", center=True, shadow=True)

        if not self.ranking:
            Text(720, base + 30, size=18).display(screen, "Ainda não há recordes. Seja o primeiro!",
                                                   center=True, shadow=True)
