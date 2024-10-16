import pygame
from components.Game import Game
import os

def main():
    print("Current Working Directory:", os.getcwd())
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
