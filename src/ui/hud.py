import pygame

from src.core.constrant import BLACK, WIDTH
from src.managers.font import Font


class Hud:
    def __init__(self):
        # Note: Score values are kept as fixed-width strings for display.
        self.__score = "00000"
        self.__highest_score = "00000"

    def reset_score(self):
        # Note: Restart only clears the current score, not the high score.
        self.__score = "00000"

    def set_highest_score(self):
        # Note: Save the score if the finished run beats the current high score.
        if int(self.__score) > int(self.__highest_score):
            self.__highest_score = self.__score

    def update(self):
        # Note: Increase score by one point every frame while the game runs.
        score = str(int(self.__score) + 1)
        self.__score = "0" * (5 - len(score)) + score

    def draw(self, screen: pygame.Surface):
        # Note: Draw score and high score in the top-right corner.
        font = Font(30).textFont
        score_display = font.render(str(self.__score), True, BLACK)
        highest_score_display = font.render("HI  " + str(self.__highest_score), True, BLACK)
        screen.blit(score_display, (WIDTH - 100, 10))
        screen.blit(highest_score_display, (WIDTH - 250, 10))
