import pygame

from constants import IMAGES_PATH, MUSIC_PATH, SOUNDS_PATH, VIDEOS_PATH

_cache = {}


def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


# ---------------------------------------------------------------- sorteio (sem a biblioteca random)
# Gerador de numeros pseudoaleatorios simples (congruencial linear).
_seed = [12345]


def seed_random(value):
    """Muda a semente do sorteio (usamos o tempo do pygame para cada partida ser diferente)."""
    _seed[0] = value % 2147483648


def random_float():
    """Numero entre 0 e 1."""
    _seed[0] = (_seed[0] * 1103515245 + 12345) % 2147483648
    return _seed[0] / 2147483648


def random_int(minimum, maximum):
    """Inteiro entre minimum e maximum (incluindo os dois)."""
    return minimum + int(random_float() * (maximum - minimum + 1))


def random_choice(options):
    """Escolhe um item da lista."""
    return options[random_int(0, len(options) - 1)]


def wave(time, period):
    """Onda que vai de -1 a 1 e volta, repetindo a cada `period` (substitui o seno)."""
    position = (time % period) / period
    return 4 * abs(position - 0.5) - 1


# ---------------------------------------------------------------- imagens e sons
def load_image(name):
    """Carrega uma imagem de assets/images (com cache). Ex: load_image("player_run1.png").
    Retorna None se o arquivo nao existir, e o objeto se desenha como retangulo."""
    if name not in _cache:
        try:
            _cache[name] = pygame.image.load(f"{IMAGES_PATH}/{name}").convert_alpha()
        except (FileNotFoundError, pygame.error):
            _cache[name] = None
    return _cache[name]


_sounds = {}


def play_sound(name):
    """Toca um som de assets/sounds (com cache). Se nao houver audio no PC, so ignora."""
    if name not in _sounds:
        try:
            _sounds[name] = pygame.mixer.Sound(f"{SOUNDS_PATH}/{name}")
        except (FileNotFoundError, pygame.error):
            _sounds[name] = None
    if _sounds[name]:
        _sounds[name].play()


def play_music(name, loops=-1, volume=0.7):
    """Toca uma musica de assets/music (por padrao em loop)."""
    try:
        pygame.mixer.music.load(f"{MUSIC_PATH}/{name}")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
    except (FileNotFoundError, pygame.error):
        pass


def stop_music():
    try:
        pygame.mixer.music.stop()
    except pygame.error:
        pass


def load_video_frames(name):
    """Carrega os quadros de um video: assets/videos/<name>/0001.jpg, 0002.jpg... ate acabar."""
    key = "video:" + name
    if key not in _cache:
        frames = []
        number = 1
        while True:
            try:
                frames.append(pygame.image.load(f"{VIDEOS_PATH}/{name}/{number:04d}.jpg").convert())
            except (FileNotFoundError, pygame.error):
                break
            number += 1
        _cache[key] = frames
    return _cache[key]
