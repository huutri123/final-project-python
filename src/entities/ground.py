import pygame.image

from src.core.constants import GAME_SPEED, GROUND_HEIGHT, PATH


class Ground:
    def __init__(self):
        # Note: Load one ground image and draw it twice for endless scrolling.
        self.__ground = pygame.image.load(str(PATH) + "/asset/Image/ground.png")
        self.reset()

    def reset(self):
        # Note: Place the two ground images side by side.
        self.__x1 = 0
        self.__x2 = self.__ground.get_width()

    def update(self, speed=GAME_SPEED):
        # Note: Move both ground images left every frame.
        self.__x1 -= speed
        self.__x2 -= speed

        # Note: When one image leaves the screen, place it after the other one.
        if self.__x1 <= -self.__ground.get_width():
            self.__x1 = self.__x2 + self.__ground.get_width()
        if self.__x2 <= -self.__ground.get_width():
            self.__x2 = self.__x1 + self.__ground.get_width()

    def draw(self, screen):
        # Note: Draw both ground images to hide the looping edge.
        screen.blit(self.__ground, (self.__x1, GROUND_HEIGHT))
        screen.blit(self.__ground, (self.__x2, GROUND_HEIGHT))
