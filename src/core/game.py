import pygame

from src.core.constrant import FPS, HEIGHT, WHITE, WIDTH
from src.entities.dino import Dino
from src.entities.ground import Ground
from src.entities.obstacle import Obstacle
from src.managers.collision import Collision
from src.ui.hud import Hud


class Game:
    def __init__(self):
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__clock = pygame.Clock()
        pygame.display.set_caption("T-Rex Game")

        self.__running = True
        self.__game_over = True
        self.__can_restart_with_space = True

        self.__ground = Ground()
        self.__dino = Dino()
        self.__obstacle = Obstacle()
        self.__hud = Hud()

    def __restart_game(self):
        """Start a fresh run only from a new SPACE press."""
        self.__game_over = False
        self.__can_restart_with_space = False
        self.__ground.reset()
        self.__dino.reset()
        self.__obstacle.reset()
        self.__hud.reset_score()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                # The player must release SPACE after dying before SPACE can restart.
                # This prevents auto-restart when the collision happens while SPACE is held.
                self.__can_restart_with_space = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.__game_over and self.__can_restart_with_space:
                    self.__restart_game()

        keys = pygame.key.get_pressed()
        self.__dino.duck(keys[pygame.K_DOWN] and not self.__game_over)

        # Holding SPACE now keeps jumping. Dino.jump() itself only starts a jump
        # when Dino is on the ground, so this does not create mid-air double jumps.
        if not self.__game_over and keys[pygame.K_SPACE]:
            self.__dino.jump()

    def __update(self):
        if self.__game_over:
            return

        self.__dino.update()
        self.__ground.update()
        self.__obstacle.update()
        self.__hud.update()

        if Collision.collision_check(self.__dino, self.__obstacle):
            self.__game_over = True
            self.__can_restart_with_space = not pygame.key.get_pressed()[pygame.K_SPACE]
            self.__hud.set_highest_score()
            self.__dino.duck(False)

    def __draw(self):
        self.__screen.fill(WHITE)
        self.__ground.draw(self.__screen)
        self.__dino.draw(self.__screen)
        self.__obstacle.draw(self.__screen)
        self.__hud.draw(self.__screen)

    def run(self):
        while self.__running:
            self.__handle_events()
            self.__update()
            self.__draw()
            self.__clock.tick(FPS)
            pygame.display.flip()
