import random

import pygame.image

from src.core.constrant import GAME_SPEED, GROUND_HEIGHT, PATH, WIDTH


class Obstacle:
    def __init__(self):
        self.__obstacles = [
            pygame.image.load(str(PATH) + "/asset/Image/cactus_1.png"),
            pygame.image.load(str(PATH) + "/asset/Image/cactus_2.png"),
            pygame.image.load(str(PATH) + "/asset/Image/cactus_3.png"),
        ]
        self.__obstacle = self.__obstacles[0]
        self.__spawn_x = WIDTH + 100
        self.reset()

    def reset(self):
        self.x = 0
        self.__obstacle = random.choice(self.__obstacles)

    def __randomize_if_offscreen(self):
        if self.__spawn_x - self.x < -self.__obstacle.get_width():
            self.__obstacle = random.choice(self.__obstacles)
            self.x = 0

    def update(self):
        self.x += GAME_SPEED
        self.__randomize_if_offscreen()

    @property
    def collision_rect(self):
        return pygame.Rect(
            self.__spawn_x - self.x,
            GROUND_HEIGHT - self.__obstacle.get_height() + 22,
            self.__obstacle.get_width(),
            self.__obstacle.get_height(),
        )

    def draw(self, screen):
        screen.blit(
            self.__obstacle,
            (self.__spawn_x - self.x, GROUND_HEIGHT - self.__obstacle.get_height() + 22),
        )
