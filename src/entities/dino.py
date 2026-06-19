import pygame.image

from src.core.constants import DINO_DUCK1, DINO_DUCK2, DINO_X, GRAVITY, GROUND_HEIGHT, JUMP_VELOCITY, PATH
from src.utils.helpers import ImageUtils


class Dino:
    def __init__(self):
        # Note: Load running frames from separate image files.
        self.__dino_run = [
            pygame.image.load(str(PATH) + "/asset/Image/dino_run1.png"),
            pygame.image.load(str(PATH) + "/asset/Image/dino_run2.png"),
        ]

        # Note: Load ducking frames by cutting them from the sprite sheet.
        self.__sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__dino_duck = [
            ImageUtils.get_image(self.__sheet, DINO_DUCK1),
            ImageUtils.get_image(self.__sheet, DINO_DUCK2),
        ]

        # Note: Masks make collision follow visible pixels instead of full rectangles.
        self.__collision_masks = {
            id(image): ImageUtils.create_visible_pixel_mask(image)
            for image in self.__dino_run + self.__dino_duck
        }
        self.__animation_speed = 0.2
        self.reset()

    def reset(self):
        # Note: Restore the dino to the starting movement state.
        self.__turn = 0
        self.__is_jumping = False
        self.__y_velocity = 0
        self.__elevation = 0
        self.__is_ducking = False

    def jump(self):
        # Note: Start a jump only when the dino is on the ground and not ducking.
        if not self.__is_jumping and not self.__is_ducking:
            self.__is_jumping = True
            self.__y_velocity = JUMP_VELOCITY
            return True
        return False

    def duck(self, is_ducking):
        # Note: Ducking is controlled by the game input handler.
        self.__is_ducking = is_ducking

    def update(self):
        # Note: Advance the running animation frame.
        self.__turn += self.__animation_speed
        if self.__turn >= 2:
            self.__turn = 0

        # Note: Apply jump physics until the dino lands back on the ground.
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
        # Note: Use ducking frames only while ducking on the ground.
        if self.__is_ducking and not self.__is_jumping:
            return self.__dino_duck[int(self.__turn)]
        return self.__dino_run[int(self.__turn)]

    @property
    def collision_rect(self):
        # Note: Rect position must match the image position drawn on screen.
        image = self.__current_image()
        return pygame.Rect(
            DINO_X,
            GROUND_HEIGHT - image.get_height() + 20 - self.__elevation,
            image.get_width(),
            image.get_height(),
        )

    @property
    def collision_mask(self):
        # Note: Return the mask for the current animation frame.
        return self.__collision_masks[id(self.__current_image())]

    @property
    def is_jumping(self):
        return self.__is_jumping

    @property
    def feet_position(self):
        rect = self.collision_rect
        return rect.centerx, rect.bottom

    @property
    def center_position(self):
        return self.collision_rect.center

    def draw(self, screen):
        # Note: Draw the current dino frame at its ground or jump position.
        image = self.__current_image()
        screen.blit(
            image,
            (DINO_X, GROUND_HEIGHT - image.get_height() + 20 - self.__elevation),
        )
