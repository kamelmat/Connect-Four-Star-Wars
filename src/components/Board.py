import pygame
from .Piece import Piece

class Board:
    def __init__(self, game):
        self.game = game
        self.rows = 6
        self.columns = 7
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'Imperial'  # or 'Rebel'
        self.cell_size = 100  # Size of each cell

    def draw(self):
        # Calculate the starting position to center the board
        start_x = (self.game.width - (self.columns * self.cell_size)) // 2
        start_y = (self.game.height - (self.rows * self.cell_size)) // 2

        for c in range(self.columns):
            for r in range(self.rows):
                if self.grid[r][c] is None:
                    # Create a semi-transparent circle
                    circle_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 255, 255, 128), (self.cell_size // 2, self.cell_size // 2), 40)  # White circle with 50% transparency
                    self.game.screen.blit(circle_surface, (start_x + c * self.cell_size, start_y + r * self.cell_size))  # Draw the circle
                else:
                    piece_image = self.grid[r][c].get_image()
                    piece_image = pygame.transform.scale(piece_image, (80, 80))  # Scale the image to fit
                    self.game.screen.blit(piece_image, (start_x + c * self.cell_size + 10, start_y + r * self.cell_size + 10))  # Draw the piece

    def drop_piece(self, column):
        for r in range(self.rows - 1, -1, -1):  # Start from the bottom row
            if self.grid[r][column] is None:  # Check if the cell is empty
                self.grid[r][column] = Piece(self.current_player)  # Create a new Piece instance
                self.play_sound()
                # Check for a winner after placing the piece
                if self.check_winner(self.current_player):  # Pass the current player to check for a win
                    self.game.show_victory(self.current_player)
                self.current_player = 'Rebel' if self.current_player == 'Imperial' else 'Imperial'
                break

    def play_sound(self):
        sound_file = "assets/sounds/tie_fighter.mp3" if self.current_player == 'Imperial' else "assets/sounds/x_wing.mp3"
        print(f"Playing sound: {sound_file}")  # Debug print
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

    def check_winner(self, color):
        """Check if there is a winner with four in a row."""
        return (self.check_rows(color) or
                self.check_columns(color) or
                self.check_right_diagonal(color) or
                self.check_left_diagonal(color))

    def check_rows(self, color):
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if (self.grid[r][c] is not None and
                    self.grid[r][c].player == color and
                    self.grid[r][c + 1] is not None and
                    self.grid[r][c + 1].player == color and
                    self.grid[r][c + 2] is not None and
                    self.grid[r][c + 2].player == color and
                    self.grid[r][c + 3] is not None and
                    self.grid[r][c + 3].player == color):
                    return True
        return False

    def check_columns(self, color):
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if (self.grid[r][c] is not None and
                    self.grid[r][c].player == color and
                    self.grid[r + 1][c] is not None and
                    self.grid[r + 1][c].player == color and
                    self.grid[r + 2][c] is not None and
                    self.grid[r + 2][c].player == color and
                    self.grid[r + 3][c] is not None and
                    self.grid[r + 3][c].player == color):
                    return True
        return False

    def check_right_diagonal(self, color):
        for c in range(self.columns - 3):
            for r in range(self.rows - 1, 2, -1):
                if (self.grid[r][c] is not None and
                    self.grid[r][c].player == color and
                    self.grid[r - 1][c + 1] is not None and
                    self.grid[r - 1][c + 1].player == color and
                    self.grid[r - 2][c + 2] is not None and
                    self.grid[r - 2][c + 2].player == color and
                    self.grid[r - 3][c + 3] is not None and
                    self.grid[r - 3][c + 3].player == color):
                    return True
        return False

    def check_left_diagonal(self, color):
        for c in range(self.columns - 1, 2, -1):
            for r in range(self.rows - 1, 2, -1):
                if (self.grid[r][c] is not None and
                    self.grid[r][c].player == color and
                    self.grid[r - 1][c - 1] is not None and
                    self.grid[r - 1][c - 1].player == color and
                    self.grid[r - 2][c - 2] is not None and
                    self.grid[r - 2][c - 2].player == color and
                    self.grid[r - 3][c - 3] is not None and
                    self.grid[r - 3][c - 3].player == color):
                    return True
        return False
