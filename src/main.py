import pygame
from components.Game import Game

def main():
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
