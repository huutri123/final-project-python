import sys
from src.core.game import Game
import pygame

def main():
    pygame.init()
    game = Game()
    game.run()
    sys.exit()

if __name__=="__main__":
    main()