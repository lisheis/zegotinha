SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

WINDOW_TITLE = "Ze Gotinha - A Caminho da UPA"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 255)
RED = (220, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (60, 200, 90)

IMAGES_PATH = "assets/images"
SOUNDS_PATH = "assets/sounds"
MUSIC_PATH = "assets/music"

# Audio que toca sempre que a tela inicial aparece
MENU_VOICE = "cade_ze_gotinha.ogg"
# Videos do Ze dancando que aparecem ao chegar na UPA (um por fase).
# Cada um e uma pasta de imagens em assets/videos/<nome>/ + o audio assets/music/<nome>.ogg
VIDEOS_PATH = "assets/videos"
VICTORY_VIDEOS = ["danca1", "danca2", "danca3"]
VIDEO_FPS = 15

# Chao e fisica
GROUND_Y = 440
GRAVITY = 0.8
JUMP_FORCE = -15

# Jogador (Ze Gotinha)
PLAYER_X = 150
PLAYER_WIDTH = 44
PLAYER_HEIGHT = 64
PLAYER_COLOR = WHITE
MAX_LIVES = 5
START_AMMO = 3
INVULNERABLE_FRAMES = 90

# Vacina arremessada
PROJECTILE_WIDTH = 22
PROJECTILE_HEIGHT = 10
PROJECTILE_SPEED = 12

# Obstaculos, blocos e itens
OBSTACLE_COLOR = (170, 120, 60)
ITEM_SIZE = 26
BLOCK_SIZE = 40
# Altura das fileiras de blocos suspensos (o Ze passa por baixo e os virus tambem)
PLATFORM_Y = GROUND_Y - 110
QUESTION_CHANCE = 0.25  # chance de um bloco ser "?" (solta vacina na cabecada)

# Virus: cor, tamanho, vida, velocidade extra, se voa
ENEMY_KINDS = {
    "corona": {"color": (150, 60, 170), "size": 44, "hp": 1, "extra_speed": 1.5, "flying": False},
    "zika":   {"color": (60, 170, 90),  "size": 44, "hp": 2, "extra_speed": 3, "flying": False},
    "aedes":  {"color": (90, 60, 40),   "size": 36, "hp": 1, "extra_speed": 1, "flying": True},
}

# Itens: cor e municao que dao (vida nao se recupera)
ITEM_KINDS = {
    "vaccine": {"color": (80, 230, 120), "ammo": 2},
    "syringe": {"color": (150, 200, 255), "ammo": 1},
    "drop":    {"color": (60, 140, 255), "ammo": 1},
}

# Tempo da fase em segundos. Quando acaba, a UPA aparece no fim do caminho.
LEVEL_TIME = 65

# A fase vai acelerando: no fim do tempo a velocidade e SPEED_GAIN vezes a inicial
SPEED_GAIN = 1.5

# Fases em ordem: entardecer (principal, sempre a primeira), noite, dia. Mais virus conforme avanca.
# gap = distancia (px) entre um elemento e outro; virus_chance = chance de ser virus
LEVELS = [
    {"name": "Entardecer", "theme": "entardecer", "speed": 5, "gap": (220, 420), "virus_chance": 0.4,
     "viruses": ["corona"]},
    {"name": "Noite", "theme": "noite", "speed": 6, "gap": (200, 380), "virus_chance": 0.5,
     "viruses": ["corona", "zika"]},
    {"name": "Dia", "theme": "dia", "speed": 7, "gap": (180, 340), "virus_chance": 0.6,
     "viruses": ["corona", "zika", "aedes"]},
]

# Ranking (podio): arquivo onde os recordes ficam salvos
RANKING_FILE = "ranking.txt"
RANKING_SHOW = 5      # quantos aparecem na tela inicial
NAME_MAX_LENGTH = 12

FONT_STYLE = "Arial"
FONT_SIZE = 22
