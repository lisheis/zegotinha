import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from classes.text import Text
from utils.helpers import wave 

# adicionar a biblioteca no constants.py
LEVEL_INTRO = {"title": "Fase 1: Coronavírus", "lines" : ["        Cuidado com o Coronavírus! Desvie ou arremesse 1 vacina para elimina-lo, mas lembre de chegar com a máxima quantidade na UPA", "ESPAÇO: Pular", "X: Arremessa vacina"], "image": "",
               
"title": "Fase 2: Zika e Coronavírus  ", "lines" : ["Agora o Zika vírus também apareceu! Desvie ou arremesse 2 vacinas para elimina-lo", "ESPAÇO: Pular", "X: Arremessa vacina" ], "image": "",

"title": "Fase 3: Dengue, Zika e Coronavírus ", "lines" : ["Última fase! Cuidado o Aedes aegypti!"], "image": ""}


class levelintro:

    """página de aprensentação do nível para explicar ao usuario as teclas que serão utilizadas por eles e o(s) enemy(s) da fase e como derrota-lo(s)"""

    FADE_FRAMES = 30
    BLINK_FRAMES = 30

    def __init__(self, data):
        self.title = data["title"]
        self.line = data["lines"]
        self.image = pygame.image.load(data["image"]).convert_alpha()
        self.ticks = 0
        self.button = pygame.Rect(SCREEN_WIDTH // 2 - 230, 455, 460, 66 )

    def handle_event(self, event):

        pressed_enter = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                pressed_enter = True

        return pressed_enter


    def draw(self, screen):
        pass




