import pygame

from src.core.constrant import (
    FPS,
    GAME_OVER_FRAME,
    HEIGHT,
    PATH,
    RESTART_BUTTON_FRAME,
    WHITE,
    WIDTH,
)
from src.entities.dino import Dino
from src.entities.cloud import Cloud
from src.entities.ground import Ground
from src.entities.obstacle import Obstacle
from src.managers.collision import Collision
from src.ui.hud import Hud
from src.utils.helpers import ImageUtils


class Game:
    def __init__(self):
        # Note: Set up the window, clock, and main game state.
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__clock = pygame.Clock()
        pygame.display.set_caption("T-Rex Game")

        self.__running = True
        self.__game_started = False
        self.__game_over = False

        # Note: Create the main game objects.
        self.__cloud = Cloud()
        self.__ground = Ground()
        self.__dino = Dino()
        self.__obstacle = Obstacle()
        self.__hud = Hud()

        # Note: Cut the Game Over text from the shared sprite sheet.
        sheet = pygame.image.load(str(PATH) + "/asset/Image/sprite_sheet.png")
        self.__game_over_image = ImageUtils.get_image(sheet, GAME_OVER_FRAME)
        self.__restart_button_image = ImageUtils.get_image(sheet, RESTART_BUTTON_FRAME)
        self.__restart_button_rect = self.__restart_button_image.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 3 + self.__game_over_image.get_height() + 50,
            )
        )

    def __restart_game(self):
        """Start a fresh run from a mouse click."""
        # Note: Reset every object that changes during a run.
        self.__game_started = True
        self.__game_over = False
        self.__cloud.reset()
        self.__ground.reset()
        self.__dino.reset()
        self.__obstacle.reset()
        self.__hud.reset_score()

    def __handle_events(self):
        # Note: Handle quit, restart, and player input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.__game_over
                and self.__restart_button_rect.collidepoint(event.pos)
            ):
                self.__restart_game()

        keys = pygame.key.get_pressed()

        if not self.__game_started and not self.__game_over and keys[pygame.K_SPACE]:
            self.__game_started = True
            self.__dino.jump()

        self.__dino.duck(keys[pygame.K_DOWN] and self.__game_started and not self.__game_over)

        # Holding SPACE now keeps jumping. Dino.jump() itself only starts a jump
        # when Dino is on the ground, so this does not create mid-air double jumps.
        if self.__game_started and not self.__game_over and keys[pygame.K_SPACE] or  keys[pygame.K_UP]:
            self.__dino.jump()

    def __update(self):
        # Note: Stop game movement while the Game Over screen is visible.
        if not self.__game_started or self.__game_over:
            return

        # Note: Update moving objects and score while the game is running.
        self.__cloud.update()
        self.__dino.update()
        self.__ground.update()
        self.__obstacle.update()
        self.__hud.update()

        # Note: A collision ends the current run and saves the high score.
        if Collision.collision_check(self.__dino, self.__obstacle):
            self.__game_over = True
            self.__hud.set_highest_score()
            self.__dino.duck(False)

    def __draw(self):
        # Note: Draw the current frame from background to foreground.
        self.__screen.fill(WHITE)
        self.__cloud.draw(self.__screen)
        self.__ground.draw(self.__screen)
        self.__dino.draw(self.__screen)
        self.__obstacle.draw(self.__screen)
        self.__hud.draw(self.__screen)

        # Note: Show Game Over text and restart button only after losing.
        if self.__game_over:
            self.__screen.blit(
                self.__game_over_image,
                (
                    (WIDTH - self.__game_over_image.get_width()) // 2,
                    HEIGHT // 3,
                ),
            )
            self.__screen.blit(self.__restart_button_image, self.__restart_button_rect)

    def run(self):
        # Note: Main loop runs until the player closes the window.
        while self.__running:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock.tick(FPS)
            pygame.display.flip()
