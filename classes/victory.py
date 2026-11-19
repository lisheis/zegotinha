import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, VIDEO_FPS
from classes.text import Text
from utils.helpers import load_video_frames, play_music, random_choice, random_float, random_int, stop_music, wave

CONFETTI_COLORS = [(255, 90, 90), (255, 220, 70), (90, 200, 255), (120, 230, 120), (255, 255, 255)]


class Victory:
    """Tela de quando o Ze chega na UPA: passa o video do Ze dancando o funk da vacina."""

    def __init__(self, title, lines, button_label, video_name):
        self.title = title
        self.lines = lines
        self.button_label = button_label
        self.frames = load_video_frames(video_name)
        self.start_time = pygame.time.get_ticks()
        self.ticks = 0
        self.button = pygame.Rect(SCREEN_WIDTH // 2 - 230, 455, 460, 66)
        self.confetti = [self.new_confetti(random_int(-SCREEN_HEIGHT, 0)) for _ in range(60)]
        play_music(f"{video_name}.ogg", loops=0, volume=0.9)

    def new_confetti(self, y):
        return [random_int(0, SCREEN_WIDTH), y, 1.5 + random_float() * 2, random_choice(CONFETTI_COLORS)]

    def handle_event(self, event):
        """Retorna True quando o jogador quer continuar (ENTER ou clique no botao)."""
        pressed_enter = event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
        clicked = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                   and self.button.collidepoint(event.pos))
        if pressed_enter or clicked:
            stop_music()
            return True
        return False

    def current_frame(self):
        """Quadro do video de acordo com o tempo (fica no ultimo quando acaba)."""
        if not self.frames:
            return None
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        index = min(int(elapsed * VIDEO_FPS), len(self.frames) - 1)
        return self.frames[index]

    def draw(self, screen):
        self.ticks += 1

        panel = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel.fill((15, 100, 120, 225))
        screen.blit(panel, (0, 0))

        for c in self.confetti:
            c[1] += c[2]
            if c[1] > SCREEN_HEIGHT:
                c[:] = self.new_confetti(-10)
            pygame.draw.rect(screen, c[3], (c[0], c[1], 6, 10))

        frame = self.current_frame()
        if frame:
            rect = frame.get_rect(midtop=(SCREEN_WIDTH // 2, 62))
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(10, 10), border_radius=8)
            screen.blit(frame, rect)
            text_left = rect.left // 2
            text_right = (rect.right + SCREEN_WIDTH) // 2
        else:
            text_left, text_right = 200, SCREEN_WIDTH - 200

        Text(SCREEN_WIDTH // 2, 32, size=40, bold=True).display(screen, self.title, center=True, shadow=True)
        for i, line in enumerate(self.lines):
            side_x = text_left if i % 2 == 0 else text_right
            Text(side_x, 230 + (i // 2) * 40, size=24, bold=True, color=(255, 240, 160)).display(
                screen, line, center=True, shadow=True)

        hover = self.button.collidepoint(pygame.mouse.get_pos())
        pulse = int(abs(wave(self.ticks, 60)) * 30)
        body = (90, 215, 100) if hover else (60 + pulse, 190, 80)
        pygame.draw.rect(screen, (25, 90, 40), self.button.move(0, 6), border_radius=16)
        pygame.draw.rect(screen, body, self.button, border_radius=16)
        pygame.draw.rect(screen, (255, 255, 255), self.button, 3, border_radius=16)
        Text(self.button.centerx, self.button.centery - 8, size=28, bold=True).display(
            screen, self.button_label, center=True, shadow=True)
        Text(self.button.centerx, self.button.centery + 19, size=15).display(
            screen, "(aperte ENTER)", center=True)
