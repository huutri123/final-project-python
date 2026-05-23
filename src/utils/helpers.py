import json

import pygame
from src.core.constrant import PATH


class ImageUtils:
    """Shared image helpers."""

    @staticmethod
    def get_image(sheet, rect):
        """Cut one image from a sprite sheet."""
        # Note: Create a transparent surface with the requested sprite size.
        image = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), rect)
        return image

    @staticmethod
    def create_visible_pixel_mask(surface: pygame.Surface) -> pygame.mask.Mask:
        """Create a collision mask from visible, non-white pixels only.

        The source sprites use a white background. A normal rect collision sees that
        whole rectangle as solid, so the game can end before the dino visually touches
        a cactus. This mask keeps only the dark sprite pixels as the hit area.
        """
        # Note: Build a mask manually so white sprite backgrounds are ignored.
        mask = pygame.mask.Mask(surface.get_size())

        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                red, green, blue, alpha = surface.get_at((x, y))
                is_visible = alpha > 0
                is_background = red > 245 and green > 245 and blue > 245

                if is_visible and not is_background:
                    mask.set_at((x, y), 1)

        return mask

class Data:
    @staticmethod
    def GetData():
        # Note: Read high score data from the JSON file.
        try:
            file = open(str(PATH) + "/data/highscore.json")
        except FileNotFoundError:
            print(FileNotFoundError)
        else:
            data = json.load(file)
            file.close()
            return data

    @staticmethod
    def SaveData(data):
        # Note: Save high score data back to the JSON file.
        try:
            file = open(str(PATH) + "/data/highscore.json")
        except FileNotFoundError:
            print(FileNotFoundError)
        else:
            json.dump(file,data)
            file.close()
