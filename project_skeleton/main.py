import pygame
import sys
from cell import Cell
from calcs import measure_distance

""" This is the main file you work on for the project"""

pygame.init()

SCREEN_MIN_SIZE = 750  # Can be made to autoadjust after % of ur screen
amount_of_cells = 16  # The amount of cells is equal in rows and columns, 16x16
bomb_chance = 0.25

CELL_SIZE = SCREEN_MIN_SIZE // amount_of_cells  # how large can each cell be?
READJUSTED_SIZE = CELL_SIZE * amount_of_cells
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE

SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("MineSweeper")

cells = []


def create_cells():
    """This function is meant to initialy generate all the cells and create the boundaries"""
    # This is a good base to go from (think about it thoroughly before you code!! We want to create 16x16 list with each object being a cell):
    # for a_row in range(amount_of_cells):
    #     row = []
    #     for a_column in range(amount_of_cells):
    #         pass

    pass


def draw_cells():
    """In this function we want to draw each cell, i.e call upon each cells .draw() method!"""
    # Hint: take inspiration from the forloop in create_cells to loop over all the cells
    pass


def draw():
    """This function handles all the drawings to the screen, such as drawing rectangles, objects etc"""
    draw_cells()


def event_handler(event):
    """This function handles all events in the program"""
    if event.type == pygame.QUIT:
        terminate_program()


def run_setup():
    """This function is meant to run all code that is neccesary to setup the app, happends only once"""
    create_cells()


def terminate_program():
    """Functionality to call on whenever you want to terminate the program"""
    pygame.quit()
    sys.exit()


def main():
    run_setup()

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            event_handler(event)

        draw()
        pygame.display.update()

    terminate_program()


if __name__ == "__main__":
    main()
