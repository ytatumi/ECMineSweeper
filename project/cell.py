import pygame
import random
import os


class Cell:
    """This file contains the cell class representing each square in the game"""

    def __init__(self, x, y, width, height, bomb_chance, bomb_image, flag_image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 64, 0)  # RGB color
        self.cell_thickness = 2
        self.neighbouring_bombs = 0
        self.selected = False
        self.flag = False

        self.cell_center = (
            self.x + self.width // 2,
            self.y + self.width // 2,
        )  # useful for drawing
        self.bomb = (
            random.random() < bomb_chance
        )  # each cell has a chance of being a bomb
        self.bomb_image = bomb_image
        self.flag_image = flag_image
        self.count_neighboring_bomb_font = pygame.font.SysFont("comicsans", 15)

    def draw_cell(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height),
            self.cell_thickness,
        )

    def draw_neighboring_bomb_counts(self, screen):
        neiboring_bomb_counter_text = self.count_neighboring_bomb_font.render(
            str(self.neighbouring_bombs), 1, ((255, 255, 255))
        )
        screen.blit(
            neiboring_bomb_counter_text,
            (
                self.cell_center[0] - (neiboring_bomb_counter_text.get_width() // 2),
                self.cell_center[1] - (neiboring_bomb_counter_text.get_height() // 2),
            ),
        )

    def draw_bomb(self, screen):
        screen.blit(self.bomb_image, (self.x, self.y))

    def draw_flag(self, screen):
        screen.blit(self.flag_image, (self.x, self.y))

    def draw(self, screen):
        """This method is called in the main.py files draw_cells function"""
        self.draw_cell(screen)
        if self.selected:
            if not self.bomb:
                self.draw_neighboring_bomb_counts(screen)
            else:
                self.draw_bomb(screen)

        if self.flag:
            self.draw_flag(screen)

    def draw_answer(self, screen):
        """This method is called in the main.py files draw_cells function"""
        self.draw_cell(screen)
        if self.bomb:
            self.draw_bomb(screen)
        else:
            self.draw_neighboring_bomb_counts(screen)
