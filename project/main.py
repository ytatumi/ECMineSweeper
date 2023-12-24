import pygame
import os
import sys
from cell import Cell

""" This is the main file you work on for the project"""

pygame.init()

displayInfo = pygame.display.Info()
SCREEN_MIN_SIZE = round(min(displayInfo.current_w, displayInfo.current_h) * 0.8)
amount_of_cells = 16  # The amount of cells is equal in rows and columns, 16x16 (LOCKED)
bomb_chance = 0.25  # Change to prefered value or use default 0.25
total_score = 0
selected_cells_count = 0
total_bomb_count = 0

CELL_SIZE = SCREEN_MIN_SIZE // amount_of_cells  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * amount_of_cells
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE
SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MineSweeper")

BOMB_IMAGE = pygame.image.load(os.path.join("images", "bomb.png"))
BOMB_IMAGE = pygame.transform.scale(BOMB_IMAGE, (CELL_WIDTH, CELL_HEIGHT))
FLAG_IMAGE = pygame.image.load(os.path.join("images", "flag.png"))
FLAG_IMAGE = pygame.transform.scale(FLAG_IMAGE, (CELL_WIDTH, CELL_HEIGHT))

SCORE_FONT = pygame.font.SysFont("comicsans", 15)
GAMEEND_FONT = pygame.font.SysFont("comicsans", 35)
GAMEEND_FONT2 = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 20)

WHITE = (255, 255, 255)
RED = (255, 0, 0)


GAMEEND = False
ANSWER = False
WIN = False

cells = []


def create_cells():
    """This function is meant to initialy generate all the cells and create the boundaries"""
    y = 0
    for _ in range(amount_of_cells):
        row = []
        x = 0
        for _ in range(amount_of_cells):
            row.append(
                Cell(x, y, CELL_WIDTH, CELL_HEIGHT, bomb_chance, BOMB_IMAGE, FLAG_IMAGE)
            )
            x += CELL_WIDTH
        cells.append(row)
        y += CELL_HEIGHT


def draw_cells():
    """In this function we want to draw each cell, i.e call upon each cells .draw() method!"""
    global ANSWER
    for row in cells:
        for cell in row:
            if not ANSWER:
                cell.draw(screen)
            else:
                cell.draw_answer(screen)


def get_cell_number(x, y):
    return x // CELL_WIDTH, y // CELL_HEIGHT


def count_neighboring_bomb(row_num, col_num):
    if row_num > 0 and cells[row_num - 1][col_num].bomb == True:
        cells[row_num][col_num].neighbouring_bombs += 1
    if row_num < amount_of_cells - 1 and cells[row_num + 1][col_num].bomb == True:
        cells[row_num][col_num].neighbouring_bombs += 1
    if row_num > 0 and col_num > 0 and cells[row_num - 1][col_num - 1].bomb == True:
        cells[row_num][col_num].neighbouring_bombs += 1
    if col_num > 0 and cells[row_num][col_num - 1].bomb == True:
        cells[row_num][col_num].neighbouring_bombs += 1
    if (
        col_num > 0
        and row_num < amount_of_cells - 1
        and cells[row_num + 1][col_num - 1].bomb == True
    ):
        cells[row_num][col_num].neighbouring_bombs += 1
    if (
        col_num < amount_of_cells - 1
        and row_num > 0
        and cells[row_num - 1][col_num + 1].bomb == True
    ):
        cells[row_num][col_num].neighbouring_bombs += 1
    if col_num < amount_of_cells - 1 and cells[row_num][col_num + 1].bomb == True:
        cells[row_num][col_num].neighbouring_bombs += 1
    if (
        row_num < amount_of_cells - 1
        and col_num < amount_of_cells - 1
        and cells[row_num + 1][col_num + 1].bomb == True
    ):
        cells[row_num][col_num].neighbouring_bombs += 1


def draw_score():
    score_text = SCORE_FONT.render(f"SCORE: {selected_cells_count}", 1, WHITE)
    screen.blit(score_text, (READJUSTED_SIZE - (score_text.get_width() + 20), 0))


def draw_gameend_text(text):
    gameover_text = GAMEEND_FONT.render(text, 1, RED)
    screen.blit(
        gameover_text,
        (
            (READJUSTED_SIZE - gameover_text.get_width()) / 2,
            (READJUSTED_SIZE - gameover_text.get_height()) // 2,
        ),
    )
    restart_text = GAMEEND_FONT2.render("** Press key A to see the answer! **", 1, RED)
    screen.blit(
        restart_text,
        (
            (READJUSTED_SIZE - gameover_text.get_width()) / 2,
            (READJUSTED_SIZE - gameover_text.get_height()) // 2 + 40,
        ),
    )
    restart_text = GAMEEND_FONT2.render("** Press key S to Restart! **", 1, RED)
    screen.blit(
        restart_text,
        (
            (READJUSTED_SIZE - gameover_text.get_width()) / 2,
            (READJUSTED_SIZE - gameover_text.get_height()) // 2 + 80,
        ),
    )


def draw():
    """This function handles all the drawings to the screen, such as drawing rectangles, objects etc"""
    draw_cells()
    draw_score()

    if GAMEEND == True:
        if WIN:
            draw_gameend_text("YOU WON!! Congratulations!")
        else:
            draw_gameend_text("YOU BLEW UP!! GAME OVER!")


def event_handler(event):
    """This function handles all events in the program"""
    global selected_cells_count, ANSWER, GAMEEND, WIN

    if event.type == pygame.QUIT:
        # running = False
        terminate_program()
    if event.type == pygame.MOUSEBUTTONDOWN and not GAMEEND:
        x, y = pygame.mouse.get_pos()
        col_num, row_num = get_cell_number(x, y)
        if event.button == 1:  # Left click
            if not cells[row_num][col_num].selected:
                if cells[row_num][col_num].flag:
                    cells[row_num][col_num].flag = False
                cells[row_num][col_num].selected = True
                selected_cells_count += 1
                if cells[row_num][col_num].bomb:  # Game End : Lose
                    GAMEEND = True
                elif total_bomb_count == (amount_of_cells**2 - selected_cells_count):
                    GAMEEND, WIN = True
        elif event.button == 3:  # Right click
            if not cells[row_num][col_num].flag:
                cells[row_num][col_num].flag = True
            else:
                cells[row_num][col_num].flag = False

    if event.type == pygame.KEYDOWN and GAMEEND:
        if event.key == pygame.K_a:
            ANSWER = True
        elif event.key == pygame.K_s:
            game_reset()
            run_setup()


def run_setup():
    """This function is meant to run all code that is neccesary to setup the app, happends only once"""
    global total_bomb_count
    create_cells()
    for row_num in range(amount_of_cells):
        for col_num in range(amount_of_cells):
            count_neighboring_bomb(row_num, col_num)
            total_bomb_count += cells[row_num][col_num].bomb


def terminate_program():
    """Functionality to call on whenever you want to terminate the program"""
    pygame.quit()
    sys.exit()


def game_reset():
    global GAMEEND, ANSWER, cells, total_score, selected_cells_count, total_bomb_count
    cells = []
    total_score = 0
    selected_cells_count = 0
    total_bomb_count = 0
    GAMEEND = False
    ANSWER = False


def main():
    run_setup()

    clock = pygame.time.Clock()
    FPS = 60

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            event_handler(event)

        draw()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
