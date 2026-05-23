import pygame
from src.core.constrant import PATH


class Font:
    def __init__(self,fontSize):
        # Note: Load the arcade font at the requested size.
        self.textFont = pygame.font.Font(str(PATH) + '/asset/font/arcadeclassic.regular.ttf',fontSize)
