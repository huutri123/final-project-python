import pygame

from src.core.constrant import BLACK, WIDTH
from src.managers.font import Font


class Hud:
    def __init__(self):
        self.__score = "00000"
        self.__highest_score = "00000"

    def reset_score(self):
        self.__score = "00000"

    def set_highest_score(self):
        if int(self.__score) > int(self.__highest_score):
            self.__highest_score = self.__score

    def update(self):
        score = str(int(self.__score) + 1)
        self.__score = "0" * (5 - len(score)) + score

    def draw(self, screen: pygame.Surface):
        font = Font(30).textFont
        score_display = font.render(str(self.__score), True, BLACK)
        highest_score_display = font.render("HI  " + str(self.__highest_score), True, BLACK)
        screen.blit(score_display, (WIDTH - 100, 10))
        screen.blit(highest_score_display, (WIDTH - 250, 10))
