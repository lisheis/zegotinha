import pygame

from constants import FONT_SIZE, FONT_STYLE, WHITE

_fonts = {}


class Text:
    def __init__(self, x, y, size=FONT_SIZE, color=WHITE, bold=False):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.style = FONT_STYLE
        self.bold = bold

    def get_font(self):
        key = (self.style, self.size, self.bold)
        if key not in _fonts:
            _fonts[key] = pygame.font.SysFont(self.style, self.size, bold=self.bold)
        return _fonts[key]

    def display(self, screen, content, center=False, shadow=False):
        """Escreve o texto em (x, y). Com center=True, (x, y) e o centro do texto."""
        font = self.get_font()
        text_surface = font.render(content, True, self.color)
        pos = (self.x, self.y)
        if center:
            pos = text_surface.get_rect(center=(self.x, self.y)).topleft
        if shadow:
            shadow_surface = font.render(content, True, (20, 20, 40))
            screen.blit(shadow_surface, (pos[0] + 2, pos[1] + 2))
        screen.blit(text_surface, pos)
