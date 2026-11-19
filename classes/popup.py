from classes.text import Text
from utils.helpers import load_image


class Popup:
    """Vacina que sobe do bloco '?' e some, mostrando quanto o Ze ganhou (ex: +2)."""

    DURATION = 40

    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount
        self.timer = self.DURATION
        self.text = Text(0, 0, size=22, color=(180, 255, 180), bold=True)

    def update(self, scroll_speed):
        self.timer -= 1
        self.y -= 2
        self.x -= scroll_speed

    def is_done(self):
        return self.timer <= 0

    def draw(self, screen):
        image = load_image("item_vaccine.png")
        if image:
            screen.blit(image, (self.x, self.y))
        self.text.x, self.text.y = self.x + 30, self.y
        self.text.display(screen, f"+{self.amount}", shadow=True)
