import sys
from src.core.game import Game
import pygame

def main():
    # Note: Initialize pygame before creating any game window or assets.
    pygame.init()

    # Note: Create and start the main game loop.
    game = Game()
    game.run()

    # Note: Exit the program after the game window is closed.
    sys.exit()

if __name__=="__main__":
    # Note: Run the game only when this file is executed directly.
    main()
