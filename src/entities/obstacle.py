import random

import pygame.image

from src.core.constants import (
    BIRD_FRAME_1,
    BIRD_FRAME_2,
    BIRD_HIGH_Y,
    BIRD_LOW_Y,
    GAME_SPEED,
    GROUND_HEIGHT,
    PATH,
    WIDTH,
)
from src.utils.helpers import ImageUtils


class Obstacle:
    def __init__(self):
        # Note: Load all cactus variants and choose one during reset.
        self.__obstacles = [
            pygame.image.load(str(PATH) + "/asset/Image/cactus_1.png"),
            pygame.image.load(str(PATH) + "/asset/Image/cactus_2.png"),
            pygame.image.load(str(PATH) + "/asset/Image/cactus_3.png"),
        ]
        sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__bird_frames = [
            ImageUtils.get_image(sheet, BIRD_FRAME_1),
            ImageUtils.get_image(sheet, BIRD_FRAME_2),
        ]

        # Note: Each image gets a pixel mask for accurate collision.
        all_obstacles = self.__obstacles + self.__bird_frames
        self.__collision_masks = {
            id(image): ImageUtils.create_visible_pixel_mask(image)
            for image in all_obstacles
        }
        self.__obstacle = self.__obstacles[0]
        self.__is_bird = False
        self.__bird_y = BIRD_HIGH_Y
        self.__bird_turn = 0
        self.__bird_animation_speed = 0.15
        self.__spawn_x = WIDTH + 100
        self.reset()

    def reset(self):
        # Note: Move the obstacle back to the spawn point and randomize its image.
        self.x = 0
        self.__is_bird = random.choice([False, False, False, True])
        self.__bird_y = random.choice([BIRD_LOW_Y, BIRD_HIGH_Y])
        self.__bird_turn = 0
        self.__obstacle = self.__bird_frames[0] if self.__is_bird else random.choice(self.__obstacles)

    def __randomize_if_offscreen(self):
        # Note: Reuse the same obstacle object after it leaves the screen.
        if self.__spawn_x - self.x < -self.__obstacle.get_width():
            self.reset()

    def update(self, speed=GAME_SPEED):
        # Note: Increasing x makes the obstacle appear to move left.
        self.x += speed
        if self.__is_bird:
            self.__bird_turn += self.__bird_animation_speed
            if self.__bird_turn >= len(self.__bird_frames):
                self.__bird_turn = 0
            self.__obstacle = self.__bird_frames[int(self.__bird_turn)]
        self.__randomize_if_offscreen()

    def __y_position(self):
        # Note: Cactus stays on the ground, bird uses one of two flight heights.
        if self.__is_bird:
            return self.__bird_y
        return GROUND_HEIGHT - self.__obstacle.get_height() + 22

    @property
    def collision_rect(self):
        # Note: Rect position follows the same coordinates used by draw().
        return pygame.Rect(
            self.__spawn_x - self.x,
            self.__y_position(),
            self.__obstacle.get_width(),
            self.__obstacle.get_height(),
        )

    @property
    def collision_mask(self):
        # Note: Return the mask that belongs to the current obstacle image.
        return self.__collision_masks[id(self.__obstacle)]

    def draw(self, screen):
        # Note: Draw the obstacle on top of the ground line.
        screen.blit(
            self.__obstacle,
            (self.__spawn_x - self.x, self.__y_position()),
        )
