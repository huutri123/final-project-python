import pygame

from src.core.constants import WIDTH
from src.managers.font import Font
from src.utils.helpers import Data


HUD_TEXT = (255, 247, 203)
HUD_MUTED = (131, 218, 234)
HUD_PANEL = (17, 30, 53, 150)


class Hud:
    def __init__(self):
        # Note: Score values are kept as fixed-width strings for display.
        self.__score = "00000"
        data = Data.GetData() or {}
        self.__highest_score = str(data.get("highscore", "00000")).zfill(5)
        self.__score_timer = 0

    def reset_score(self):
        # Note: Restart only clears the current score, not the high score.
        self.__score = "00000"

    def set_highest_score(self):
        # Note: Save the score if the finished run beats the current high score.
        if int(self.__score) > int(self.__highest_score):
            self.__highest_score = self.__score
            Data.SaveData({"highscore": self.__highest_score})

    def update(self):
        # Note: Increase score by one point every frame while the game runs.
        self.__score_timer += 1

        if self.__score_timer < 6:
            return
        self.__score_timer = 0

        score = str(int(self.__score) + 1)
        self.__score = "0" * (5 - len(score)) + score

    @property
    def score(self):
        return self.__score

    @property
    def highest_score(self):
        return self.__highest_score

    def draw(self, screen: pygame.Surface):
        # Note: Draw score and high score in the top-right corner.
        font = Font(28).textFont
        panel = pygame.Surface((268, 52), pygame.SRCALPHA)
        pygame.draw.rect(panel, HUD_PANEL, panel.get_rect(), border_radius=14)
        pygame.draw.rect(panel, (255, 247, 203, 70), panel.get_rect(), 2, border_radius=14)
        high_label = font.render("HI", True, HUD_MUTED)
        high_value = font.render(str(self.__highest_score), True, HUD_TEXT)
        score_display = font.render(str(self.__score), True, HUD_TEXT)
        panel.blit(high_label, (18, 13))
        panel.blit(high_value, (58, 13))
        panel.blit(score_display, (168, 13))
        screen.blit(panel, (WIDTH - panel.get_width() - 24, 20))
