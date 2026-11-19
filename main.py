import pygame

from constants import FPS, LEVELS, SCREEN_HEIGHT, SCREEN_WIDTH, VICTORY_VIDEOS, WINDOW_TITLE
from classes.hud import Hud
from classes.level import Level
from classes.menu import Menu
from classes.text import Text
from classes.victory import Victory
from utils.ranking import save_score


def draw_message(screen, title, lines):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    Text(SCREEN_WIDTH // 2, 200, size=52, bold=True).display(screen, title, center=True, shadow=True)
    for i, line in enumerate(lines):
        Text(SCREEN_WIDTH // 2, 270 + i * 36, size=26).display(screen, line, center=True, shadow=True)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    hud = Hud()
    menu = Menu()
    level_number = 0
    level = Level(level_number)

    # menu | playing | level_won | game_over | finished
    state = "menu"
    player_name = ""
    total_score = 0       # vacinas entregues nas UPAs nesta partida
    last_delivered = 0
    ranking_position = None
    victory = None        # tela do Ze dancando ao chegar na UPA

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == "menu":
                if menu.handle_event(event):
                    player_name = menu.name
                    total_score = 0
                    level_number = 0
                    level = Level(level_number)
                    state = "playing"

            elif state in ("level_won", "finished"):
                if victory.handle_event(event):
                    if state == "level_won":
                        level_number += 1
                        level = Level(level_number)
                        state = "playing"
                    else:
                        menu = Menu(player_name)
                        level = Level(0)
                        state = "menu"

            elif event.type == pygame.KEYDOWN:
                if state == "playing":
                    if event.key == pygame.K_SPACE:
                        level.jump()
                    elif event.key == pygame.K_x:
                        level.throw()
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):  # game over
                    menu = Menu(player_name)
                    level = Level(0)
                    state = "menu"

        if state == "menu":
            level.distance += 1.5  # cenario andando devagar atras do menu
        elif state == "playing":
            level.update()
            if level.lost:
                state = "game_over"
                ranking_position = save_score(player_name, total_score)
            elif level.won:
                last_delivered = level.vaccines
                total_score += last_delivered
                video = VICTORY_VIDEOS[level_number % len(VICTORY_VIDEOS)]
                if level_number == len(LEVELS) - 1:
                    state = "finished"
                    ranking_position = save_score(player_name, total_score)
                    victory = Victory(f"Parabéns, {player_name}!", [
                        "Bairro vacinado!", f"{total_score} vacinas",
                        f"{ranking_position}º lugar", "no ranking"], "VOLTAR AO INÍCIO", video)
                else:
                    state = "level_won"
                    victory = Victory("Chegou na UPA!", [
                        "Entregou", "Total",
                        f"{last_delivered} vacinas", f"{total_score} vacinas"], "IR PARA A PRÓXIMA FASE", video)

        if state == "menu":
            level.draw_background(screen)
            menu.draw(screen)
        else:
            level.draw(screen)
            hud.draw(screen, level.player, level.time_left)

        if state in ("level_won", "finished"):
            victory.draw(screen)
        elif state == "game_over":
            draw_message(screen, "Game Over", [
                f"Total: {total_score} vacinas  -  {ranking_position}º lugar no ranking",
                "ENTER: voltar ao início"])

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
