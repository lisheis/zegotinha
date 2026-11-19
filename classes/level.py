import pygame

from constants import (BLOCK_SIZE, ENEMY_KINDS, ITEM_KINDS, GROUND_Y, ITEM_SIZE, LEVEL_TIME, LEVELS, PLAYER_X,
                       PLATFORM_Y, QUESTION_CHANCE, SCREEN_HEIGHT, SCREEN_WIDTH, SPEED_GAIN)
from classes.coin import Item
from classes.enemy import Enemy
from classes.goal import Goal
from classes.obstacle import Obstacle
from classes.platform import Platform
from classes.popup import Popup
from classes.projectile import Projectile
from classes.player import Player
from utils.collision import check_collision
from utils.helpers import load_image, random_choice, random_float, random_int, seed_random

ITEM_CHOICES = ["vaccine", "syringe", "drop"]


class Level:
    """Uma fase: gera blocos, obstaculos, virus e itens, e controla tempo e UPA."""

    def __init__(self, number):
        self.number = number
        seed_random(pygame.time.get_ticks() + number * 7919)  # cada partida sai diferente
        self.config = LEVELS[number]
        self.speed = self.config["speed"]
        self.distance = 0.0  # total percorrido, usado no scroll do cenario

        self.player = Player()
        self.obstacles = []
        self.platforms = []
        self.enemies = []
        self.items = []
        self.projectiles = []
        self.popups = []
        self.goal = None

        self.frames = 0
        self.distance_since_spawn = 0
        self.next_gap = 300
        self.won = False

    # ---- estado ----
    @property
    def time_left(self):
        return LEVEL_TIME - self.frames / 60

    @property
    def lost(self):
        return self.player.lives <= 0

    @property
    def vaccines(self):
        """Vacinas que o Ze esta levando. Ao chegar na UPA, elas viram pontos."""
        return self.player.ammo

    # ---- entrada ----
    def jump(self):
        self.player.jump()

    def throw(self):
        if self.player.ammo > 0:
            self.player.ammo -= 1
            p = self.player
            self.projectiles.append(Projectile(p.x + p.width, p.y + p.height // 2))

    # ---- spawn ----
    def ground_viruses(self):
        kinds = [k for k in self.config["viruses"] if not ENEMY_KINDS[k]["flying"]]
        return kinds or ["corona"]

    def spawn_platform_row(self, x):
        """Fileira de blocos no alto, com itens em cima e virus andando por baixo."""
        count = random_int(3, 7)
        for i in range(count):
            question = random_float() < QUESTION_CHANCE
            self.platforms.append(Platform(x + i * BLOCK_SIZE, PLATFORM_Y, question))

        # 1 ou 2 itens em blocos diferentes
        first = random_int(0, count - 1)
        spots = [first]
        if random_float() < 0.5:
            spots.append((first + random_int(1, count - 1)) % count)
        for i in spots:
            item_x = x + i * BLOCK_SIZE + (BLOCK_SIZE - ITEM_SIZE) // 2
            self.items.append(Item(item_x, PLATFORM_Y - ITEM_SIZE - 8, random_choice(ITEM_CHOICES)))

        used_width = count * BLOCK_SIZE
        if random_float() < self.config["virus_chance"]:
            # o virus nasce mais atras e passa por baixo dos blocos bem quando o Ze chega neles
            kind = random_choice(self.ground_viruses())
            extra = ENEMY_KINDS[kind]["extra_speed"]
            frames_to_reach = (x + used_width / 2 - PLAYER_X) / self.speed
            virus_x = PLAYER_X + (self.speed + extra) * frames_to_reach
            self.enemies.append(Enemy(virus_x, kind))
            used_width = max(used_width, int(virus_x - x) + 60)
        return used_width

    def spawn_obstacle(self, x):
        """Bloco no chao para pular, as vezes com um item no alto."""
        width = random_choice([BLOCK_SIZE, 2 * BLOCK_SIZE])
        height = random_choice([BLOCK_SIZE, 2 * BLOCK_SIZE])
        self.obstacles.append(Obstacle(x, width, height))
        if random_float() < 0.6:
            item_y = GROUND_Y - height - 70
            self.items.append(Item(x + width // 2 - ITEM_SIZE // 2, item_y, random_choice(ITEM_CHOICES)))
        return width

    def spawn_virus(self, x):
        """Virus solto (o aedes vem voando), com um item flutuando de vez em quando."""
        self.enemies.append(Enemy(x, random_choice(self.config["viruses"])))
        if random_float() < 0.4:
            self.items.append(Item(x + 140, GROUND_Y - 140, random_choice(ITEM_CHOICES)))
            return 180
        return 60

    def spawn(self):
        x = SCREEN_WIDTH + 40
        roll = random_float()
        if roll < 0.5:
            return self.spawn_platform_row(x)
        if roll < 0.5 + 0.5 * (1 - self.config["virus_chance"]):
            return self.spawn_obstacle(x)
        return self.spawn_virus(x)

    # ---- loop ----
    def update(self):
        self.frames += 1
        progress = min(1.0, self.frames / 60 / LEVEL_TIME)
        self.speed = self.config["speed"] * (1 + (SPEED_GAIN - 1) * progress)
        self.distance += self.speed

        player = self.player
        bumped = player.update(self.obstacles, self.platforms)
        if bumped and bumped.hit_from_below():
            # a vacina do bloco "?" vai direto para o Ze
            amount = ITEM_KINDS["vaccine"]["ammo"]
            player.ammo += amount
            self.popups.append(Popup(bumped.x + (BLOCK_SIZE - ITEM_SIZE) // 2, bumped.y - ITEM_SIZE, amount))

        for popup in self.popups[:]:
            popup.update(self.speed)
            if popup.is_done():
                self.popups.remove(popup)

        # a UPA entra quando o tempo acaba; antes disso continua gerando coisas
        if self.goal is None:
            self.distance_since_spawn += self.speed
            if self.time_left <= 0:
                self.goal = Goal(SCREEN_WIDTH + 100)
            elif self.distance_since_spawn >= self.next_gap:
                used_width = self.spawn()
                self.distance_since_spawn = 0
                self.next_gap = used_width + random_int(*self.config["gap"])
        else:
            self.goal.update(self.speed)
            if self.goal.x <= player.x + player.width:
                self.won = True

        for group in (self.obstacles, self.platforms, self.items):
            for obj in group[:]:
                obj.update(self.speed)
                if obj.is_offscreen():
                    group.remove(obj)

        for enemy in self.enemies[:]:
            enemy.update(self.speed)
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
            elif check_collision(player, enemy):
                player.take_hit()
                self.enemies.remove(enemy)

        for item in self.items[:]:
            if check_collision(player, item):
                player.collect(item)
                self.items.remove(item)

        for proj in self.projectiles[:]:
            proj.update()
            hit = False
            for enemy in self.enemies[:]:
                if check_collision(proj, enemy):
                    hit = True
                    if enemy.hit():
                        self.enemies.remove(enemy)
                    break
            if hit or proj.is_offscreen():
                self.projectiles.remove(proj)

    def draw_background(self, screen):
        theme = self.config["theme"]
        # cada camada anda numa velocidade: quanto mais longe, mais devagar (parallax)
        for layer, factor in (("sky", 0), ("clouds", 0.05), ("far", 0.2), ("near", 0.6)):
            image = load_image(f"backgrounds/{theme}_{layer}.png")
            if image is None:
                continue
            offset = int(self.distance * factor) % SCREEN_WIDTH
            screen.blit(image, (-offset, 0))
            screen.blit(image, (SCREEN_WIDTH - offset, 0))

        ground = load_image(f"ground_{theme}.png")
        if ground is None:
            pygame.draw.rect(screen, (90, 60, 40), (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
            return
        offset = int(self.distance) % ground.get_width()
        for x in range(-offset, SCREEN_WIDTH, ground.get_width()):
            screen.blit(ground, (x, GROUND_Y))

    def draw(self, screen):
        self.draw_background(screen)
        if self.goal:
            self.goal.draw(screen)
        for group in (self.obstacles, self.platforms, self.items, self.enemies, self.projectiles, self.popups):
            for obj in group:
                obj.draw(screen)
        self.player.draw(screen)
