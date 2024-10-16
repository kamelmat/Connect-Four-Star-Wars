import pygame
import random  # Import the random module

class Piece:
    def __init__(self, player):
        self.player = player
        self.image = self.load_image()

    def load_image(self):
        if self.player == 'Imperial':
            imperial_ships = [
                "assets/images/imperial_tie_fighter.png",
                "assets/images/imperial_tie_interceptor.png",
                "assets/images/imperial_tie_bomber.png",
                "assets/images/imperial_tie_defender.png"
            ]
            selected_ship = random.choice(imperial_ships)  # Randomly select a ship
            print(f"Loading image for Imperial: {selected_ship}")  # Debug print
            return pygame.image.load(selected_ship)  # Load the selected image
        else:
            rebel_ships = [
                "assets/images/rebel_x_wing.png",
                "assets/images/rebel_a_wing.png",
                "assets/images/rebel_y_wing.png",
                "assets/images/rebel_b_wing.png"
            ]
            selected_ship = random.choice(rebel_ships)  # Randomly select a ship
            print(f"Loading image for Rebel: {selected_ship}")  # Debug print
            return pygame.image.load(selected_ship)  # Load the selected image

    def get_image(self):
        return self.image
