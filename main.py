import sys

import pygame


from src.core.game import Game


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    # Note: Initialize pygame before creating any game window or assets.
    pygame.init()

    try:
        # Note: Create and start the main game loop.
        game = Game()
        game.run()
    finally:
        # Note: Release pygame resources cleanly when the window is closed.
        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.quit()
        pygame.quit()

    # Note: Exit the program after the game window is closed.
    return 0


if __name__=="__main__":
    # Note: Run the game only when this file is executed directly.
    sys.exit(main())
