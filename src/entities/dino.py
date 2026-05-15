import pygame.image

from src.core.constrant import DINO_DUCK1, DINO_DUCK2, DINO_X, GRAVITY, GROUND_HEIGHT, JUMP_VELOCITY, PATH
from src.utils.helpers import ImageUtils


class Dino:
    def __init__(self):
        self.__dino_run = [
            pygame.image.load(str(PATH) + "/asset/Image/dino_run1.png"),
            pygame.image.load(str(PATH) + "/asset/Image/dino_run2.png"),
        ]
        self.__sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__dino_duck = [
            ImageUtils.get_image(self.__sheet, DINO_DUCK1),
            ImageUtils.get_image(self.__sheet, DINO_DUCK2),
        ]
        self.__animation_speed = 0.2
        self.reset()

    def reset(self):
        self.__turn = 0
        self.__is_jumping = False
        self.__y_velocity = 0
        self.__elevation = 0
        self.__is_ducking = False

    def jump(self):
        if not self.__is_jumping and not self.__is_ducking:
            self.__is_jumping = True
            self.__y_velocity = JUMP_VELOCITY

    def duck(self, is_ducking):
        self.__is_ducking = is_ducking

    def update(self):
        self.__turn += self.__animation_speed
        if self.__turn >= 2:
            self.__turn = 0

        if self.__is_jumping:
            self.__turn = 0
            self.__elevation += self.__y_velocity
            self.__y_velocity -= GRAVITY
            if self.__is_ducking:
                self.__y_velocity -= 5

            if self.__elevation + self.__y_velocity < 0:
                self.__elevation = 0
                self.__is_jumping = False
                self.__y_velocity = 0

    def __current_image(self):
        if self.__is_ducking and not self.__is_jumping:
            return self.__dino_duck[int(self.__turn)]
        return self.__dino_run[int(self.__turn)]

    @property
    def collision_rect(self):
        image = self.__current_image()
        return pygame.Rect(
            DINO_X,
            GROUND_HEIGHT - image.get_height() + 20 - self.__elevation,
            image.get_width(),
            image.get_height(),
        )

    def draw(self, screen):
        image = self.__current_image()
        screen.blit(
            image,
            (DINO_X, GROUND_HEIGHT - image.get_height() + 20 - self.__elevation),
        )
