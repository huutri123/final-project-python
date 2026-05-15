import pygame.image
from src.core.constrant import *

class ImageUtils:
    """Xử lý ảnh chung"""

    @staticmethod
    def get_image(sheet,rect):
        """Get image from sheet"""
        image = pygame.Surface((rect[2],rect[3]),pygame.SRCALPHA)
        image.blit(sheet,(0,0),rect)
        return image
