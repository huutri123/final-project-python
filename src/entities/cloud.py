import random

import pygame.image

from src.core.constants import (
    CLOUD_COUNT,
    CLOUD_FRAME,
    CLOUD_MAX_Y,
    CLOUD_MIN_Y,
    CLOUD_SPEED,
    PATH,
    WIDTH,
)
from src.utils.helpers import ImageUtils


class Cloud:
    def __init__(self):
        # Note: Cut the cloud sprite from the shared sprite sheet.
        sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__cloud = ImageUtils.get_image(sheet, CLOUD_FRAME)
        self.reset()

    def reset(self):
        # Note: Spread clouds across the screen so the background starts populated.
        gap = WIDTH // CLOUD_COUNT
        self.__clouds = [
            {
                "x": i * gap + random.randint(0, gap // 2),
                "y": random.randint(CLOUD_MIN_Y, CLOUD_MAX_Y),
            }
            for i in range(CLOUD_COUNT)
        ]

    def update(self):
        # Note: Move clouds slower than obstacles to create background depth.
        for cloud in self.__clouds:
            cloud["x"] -= CLOUD_SPEED
            if cloud["x"] < -self.__cloud.get_width():
                cloud["x"] = WIDTH + random.randint(0, WIDTH // 3)
                cloud["y"] = random.randint(CLOUD_MIN_Y, CLOUD_MAX_Y)

    def draw(self, screen):
        # Note: Clouds are background elements and do not affect collision.
        for cloud in self.__clouds:
            screen.blit(self.__cloud, (cloud["x"], cloud["y"]))
