import pygame
from .Piece import Piece
import math

class CustomBoard:
    def __init__(self, game):
        self.game = game
        self.rows = 6
        self.columns = 7
        self.cell_size = 80  # Size of each cell
        self.board_texture = pygame.image.load("/workspaces/Connect-Four-Star-Wars/assets/textures/metal_texture.png").convert_alpha()  # Load metal texture
        self.border_color = (100, 100, 100)  # Dark gray for a metallic look
        self.border_thickness = 8  # Thickness of the border
        self.glow_color_rebel = (0, 0, 255)  # Blue glow for Rebel
        self.glow_color_imperial = (255, 0, 0)  # Red glow for Imperial
        self.glow_intensity = 0  # For animated glow effect
        self.glow_direction = 1  # For increasing/decreasing glow intensity

        # Load Star Wars font
        self.font = pygame.font.Font("/workspaces/Connect-Four-Star-Wars/assets/fonts/Starjedi.ttf", 24)  # Adjust the path as necessary

        # Initialize the grid for the pieces
        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = 'Imperial'  # Start with Imperial

        # Load Font Awesome icon images
        self.empire_icon = pygame.image.load("/workspaces/Connect-Four-Star-Wars/assets/font-awesome/icons/empire-icon.png").convert_alpha()
        self.rebel_icon = pygame.image.load("/workspaces/Connect-Four-Star-Wars/assets/font-awesome/icons/rebel-icon.png").convert_alpha()

    def draw(self):
        # Calculate the starting position to center the board
        start_x = (self.game.width - (self.columns * self.cell_size)) // 2
        start_y = (self.game.height - (self.rows * self.cell_size)) // 2

        # Draw the board structure
        self.draw_board_structure(start_x, start_y)

        for r in range(self.rows):
            for c in range(self.columns):
                # Draw the glow effect behind the square
                if self.grid[r][c] is not None:  # Only draw glow if there's a piece
                    glow_color = self.glow_color_imperial if self.grid[r][c].player == 'Imperial' else self.glow_color_rebel
                    self.draw_glow(start_x + c * self.cell_size, start_y + r * self.cell_size, glow_color)

                # Draw the cell with 70% transparency
                cell_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                cell_surface.fill((255, 255, 255, 180))  # Fill with white color and 70% transparency
                self.game.screen.blit(cell_surface, (start_x + c * self.cell_size, start_y + r * self.cell_size))

                # Draw the border with sharp edges
                self.draw_rounded_rect(start_x + c * self.cell_size, start_y + r * self.cell_size)

                # Draw the piece with shadow effect
                if self.grid[r][c] is not None:  # Access grid from CustomBoard
                    piece_image = self.grid[r][c].get_image()
                    piece_image = pygame.transform.scale(piece_image, (self.cell_size - 20, self.cell_size - 20))  # Scale the image to fit
                    self.game.screen.blit(piece_image, (start_x + c * self.cell_size + 10, start_y + r * self.cell_size + 10))  # Draw the piece

        # Draw integrated display
        self.draw_display(start_x, start_y)

        # Update glow intensity for animation
        self.update_glow()

    def draw_display(self, start_x, start_y):
        # Draw a single integrated display for the turn
        display_width = 200  # Increased width to fit "Imperial"
        display_height = 40
        display_rect = pygame.Rect(start_x + (self.columns * self.cell_size) // 2 - display_width // 2, start_y - 30, display_width, display_height)  # Centered display

        # Draw under-glow effect for the display
        glow_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA)  # Match display rectangle
        glow_alpha = int(128 * (1 + math.sin(self.glow_intensity)))  # Adjust alpha for glow effect
        glow_color = self.glow_color_imperial if self.current_player == 'Imperial' else self.glow_color_rebel
        pygame.draw.rect(glow_surface, (*glow_color[:3], glow_alpha), (0, 0, display_width, display_height))  # Semi-transparent glow
        self.game.screen.blit(glow_surface, (display_rect.x, display_rect.y - 5))  # Draw the glow behind the display

        # Draw display background
        pygame.draw.rect(self.game.screen, (50, 50, 50), display_rect)

        # Set text color based on the current player
        text_color = (255, 0, 0) if self.current_player == 'Imperial' else (0, 0, 255)  # Red for Imperial, Blue for Rebel

        # Render text for player turn
        display_text = self.font.render(f"{self.current_player}", True, text_color)

        # Calculate positions for text and icon
        text_x = display_rect.x + 40  # Adjust text position
        text_y = display_rect.y + (display_height - display_text.get_height()) // 2  # Center text vertically

        # Load the icon based on the current player
        icon = self.empire_icon if self.current_player == 'Imperial' else self.rebel_icon
        icon = pygame.transform.scale(icon, (30, 30))  # Scale the icon to fit

        # Draw the icon
        icon_x = display_rect.x + 10  # Adjust icon position
        icon_y = display_rect.y + (display_height - icon.get_height()) // 2  # Center icon vertically
        self.game.screen.blit(icon, (icon_x, icon_y))  # Draw the icon

        # Draw the text
        self.game.screen.blit(display_text, (text_x, text_y))  # Draw the text

    def draw_board_structure(self, start_x, start_y):
        # Draw the outer structure of the board
        # Draw pillars
        pillar_width = 30  # Increased thickness
        pillar_height = self.rows * self.cell_size + 40  # Extend above and below the grid
        pillar_surface = pygame.Surface((pillar_width, pillar_height), pygame.SRCALPHA)
        pillar_surface.blit(self.board_texture, (0, 0))
        self.game.screen.blit(pillar_surface, (start_x - pillar_width, start_y - 20))  # Left pillar
        self.game.screen.blit(pillar_surface, (start_x + self.columns * self.cell_size, start_y - 20))  # Right pillar

        # Draw the rounded top with metal texture
        top_rect = pygame.Rect(start_x - pillar_width, start_y - 40, (self.columns * self.cell_size) + (2 * pillar_width), 40)
        pygame.draw.rect(self.game.screen, self.border_color, top_rect)  # Top rectangle
        pygame.draw.arc(self.game.screen, self.border_color, 
                        (start_x - pillar_width, start_y - 40, 
                         (self.columns * self.cell_size) + (2 * pillar_width), 80), 
                        math.radians(0), math.radians(180), self.border_thickness)  # Top arc

        # Draw the metal texture on the arc
        arc_surface = pygame.Surface(((self.columns * self.cell_size) + (2 * pillar_width), 80), pygame.SRCALPHA)
        arc_surface.blit(self.board_texture, (0, 0))  # Apply the metal texture
        self.game.screen.blit(arc_surface, (start_x - pillar_width, start_y - 40))  # Draw the arc shape

        # Draw the feet with triangular design (R2-D2 style)
        foot_width = 60
        foot_height = 30
        left_foot_points = [
            (start_x - pillar_width - foot_width, start_y + pillar_height - 10),
            (start_x - pillar_width, start_y + pillar_height + foot_height),
            (start_x - pillar_width + foot_width, start_y + pillar_height - 10)
        ]
        right_foot_points = [
            (start_x + self.columns * self.cell_size + pillar_width, start_y + pillar_height - 10),
            (start_x + self.columns * self.cell_size, start_y + pillar_height + foot_height),
            (start_x + self.columns * self.cell_size - foot_width, start_y + pillar_height - 10)
        ]
        pygame.draw.polygon(self.game.screen, self.border_color, left_foot_points)  # Left foot
        pygame.draw.polygon(self.game.screen, self.border_color, right_foot_points)  # Right foot

        # Apply metal texture to feet
        foot_surface = pygame.Surface((foot_width * 2, foot_height), pygame.SRCALPHA)
        foot_surface.blit(self.board_texture, (0, 0))
        self.game.screen.blit(foot_surface, (start_x - pillar_width - foot_width, start_y + pillar_height - foot_height))  # Left foot
        self.game.screen.blit(foot_surface, (start_x + self.columns * self.cell_size - foot_width, start_y + pillar_height - foot_height))  # Right foot

    def draw_rounded_rect(self, x, y):
        # Draw a rounded rectangle for the cell border
        pygame.draw.rect(self.game.screen, self.border_color, 
                         (x, y, self.cell_size, self.cell_size), self.border_thickness, border_radius=10)  # Rounded corners

    def draw_glow(self, x, y, color):
        # Ensure the color has 4 elements (R, G, B, A)
        if len(color) == 3:
            color = (*color, 100)  # Add a default alpha value if not provided

        # Draw a glowing effect around the piece
        glow_surface = pygame.Surface((self.cell_size + 5, self.cell_size + 5), pygame.SRCALPHA)  # Smaller glow
        glow_alpha = int(128 * (1 + math.sin(self.glow_intensity)))  # Adjust alpha for glow effect
        pygame.draw.rect(glow_surface, (*color[:3], glow_alpha), (0, 0, self.cell_size + 5, self.cell_size + 5))  # Semi-transparent glow
        self.game.screen.blit(glow_surface, (x - 2.5, y - 2.5))  # Draw the glow behind the square

    def update_glow(self):
        # Update the glow intensity for animation
        self.glow_intensity += 0.1 * self.glow_direction
        if self.glow_intensity >= 1 or self.glow_intensity <= 0:
            self.glow_direction *= -1  # Reverse direction

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
