import pygame.image

from src.core.constrant import GAME_SPEED, GROUND_HEIGHT, PATH


class Ground:
    def __init__(self):
        self.__ground = pygame.image.load(str(PATH) + "/asset/Image/ground.png")
        self.__speed = GAME_SPEED
        self.reset()

    def reset(self):
        self.__x1 = 0
        self.__x2 = self.__ground.get_width()

    def update(self):
        self.__x1 -= self.__speed
        self.__x2 -= self.__speed

        if self.__x1 <= -self.__ground.get_width():
            self.__x1 = self.__x2 + self.__ground.get_width()
        if self.__x2 <= -self.__ground.get_width():
            self.__x2 = self.__x1 + self.__ground.get_width()

    def draw(self, screen):
        screen.blit(self.__ground, (self.__x1, GROUND_HEIGHT))
        screen.blit(self.__ground, (self.__x2, GROUND_HEIGHT))
