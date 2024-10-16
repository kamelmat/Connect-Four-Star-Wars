import cv2
import pygame
import pygame_gui
import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'  # Use dummy audio driver
import glob
from .Board import Board  # Comment this out if not using
from .VictoryScreen import VictoryScreen
from .CustomBoard import CustomBoard  # Import the CustomBoard

class Game:
    def __init__(self):
        # Initialize Pygame
        print("Initializing Pygame...")
        pygame.init()
        
        # Set up the display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        print("Display set up.")

        # Load the font with increased size for victory message
        self.font = pygame.font.Font("/workspaces/Connect-Four-Star-Wars/assets/fonts/Starjedi.ttf", 48)  # Increased font size for victory message
        
        # Load the icons
        self.empire_icon = pygame.image.load("/workspaces/Connect-Four-Star-Wars/assets/font-awesome/icons/empire-icon.png").convert_alpha()  # Ensure this path is correct
        self.rebel_icon = pygame.image.load("/workspaces/Connect-Four-Star-Wars/assets/font-awesome/icons/rebel-icon.png").convert_alpha()  # Ensure this path is correct
        print("Icons loaded.")

        # Set the caption
        pygame.display.set_caption("Star Wars Connect 4")
        
        # Initialize the clock
        self.clock = pygame.time.Clock()
        
        # Initialize the custom board
        self.custom_board = CustomBoard(self)  # Ensure this is correctly initialized
        print("Custom board initialized.")
        
        # Initialize the running flag
        self.running = True

        # Initialize the game over flag
        self.game_over = False  # Initialize the game_over attribute
                
        # Initialize the mixer and load sounds
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound("/workspaces/Connect-Four-Star-Wars/assets/sounds/space_battle_music.mp3")
        self.background_music.set_volume(1)
        self.background_music.play(-1)
        print("Background music loaded and playing.")

        # Load wallpaper images
        self.wallpapers = self.load_wallpapers("assets/animations/*.jpg")  # Adjust the pattern if needed
        self.current_wallpaper_index = 0
        self.wallpaper_change_time = 4000  # Time in milliseconds for each wallpaper
        self.last_wallpaper_change = pygame.time.get_ticks()  # Get the current time
        print(f"Loaded {len(self.wallpapers)} wallpapers.")

        # Initialize Pygame GUI
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))  # No custom theme

        # Create the restart button centered on the screen
        button_width = 120  # Set a smaller width for the button
        button_height = 40  # Set a smaller height for the button
        padding = 20  # Set padding from the bottom of the screen
        self.restart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.width // 2 - button_width // 2, self.height - button_height - padding), (button_width, button_height)),
                                                           text='Restart',
                                                           manager=self.ui_manager)  # Set the button text and manager
        
        # Set button properties directly
        self.restart_button.set_text('Restart')  # Set the button text
        self.restart_button.set_image(pygame.Surface((button_width, button_height)))  # Create a surface for the button
        self.restart_button.image.fill((50, 50, 50))  # Fill the button with a dark gray color

    def load_wallpapers(self, pattern):
        # Load all wallpaper images matching the pattern
        images = []
        for filepath in glob.glob(pattern):
            image = pygame.image.load(filepath).convert()
            images.append(pygame.transform.scale(image, (self.width, self.height)))  # Scale to fit the screen
        return images

    def run(self):
        self.wallpapers = self.load_wallpapers("/workspaces/Connect-Four-Star-Wars/assets/animations/*.jpg")  # Usa el patrón relativo
        print("Starting the game loop...")
        while self.running:
            self.handle_events()
            self.draw_background()  # Draw the background wallpaper
            self.custom_board.draw()  # Draw the custom board
            self.ui_manager.update(self.clock.tick(60) / 1000.0)  # Update the UI manager
            self.ui_manager.draw_ui(self.screen)  # Draw the UI elements
            pygame.display.flip()     # Update the display

    def draw_background(self):

        # Check if it's time to change the wallpaper
        current_time = pygame.time.get_ticks()
        if current_time - self.last_wallpaper_change > self.wallpaper_change_time:
            self.current_wallpaper_index = (self.current_wallpaper_index + 1) % len(self.wallpapers)
            self.last_wallpaper_change = current_time

        # Draw the current wallpaper
        self.screen.blit(self.wallpapers[self.current_wallpaper_index], (0, 0))  # Draw the wallpaper

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.game_over:  # Check if the game is over
                        self.restart_game()  # Restart the game
                    else:
                        # Check if the restart button is clicked
                        if self.restart_button.rect.collidepoint(event.pos):
                            self.restart_game()  # Call the restart method
                        else:
                            # Calculate the column based on mouse position
                            column = (event.pos[0] - (self.width - (self.custom_board.columns * self.custom_board.cell_size)) // 2) // self.custom_board.cell_size
                            self.custom_board.drop_piece(column)  # Drop the piece in the selected column
            self.ui_manager.process_events(event)  # Process UI events

    def show_victory(self, winner):
        self.game_over = True  # Set game over state
        # Load the appropriate icon based on the winner
        icon = self.empire_icon if winner == 'Imperial' else self.rebel_icon
        
        # Get original dimensions
        original_width, original_height = icon.get_size()
        
        # Calculate new dimensions while maintaining aspect ratio
        new_height = self.height // 2
        aspect_ratio = original_width / original_height
        new_width = int(new_height * aspect_ratio)
        
        # Scale the icon
        icon = pygame.transform.scale(icon, (new_width, new_height))

        # Center the icon at the top of the screen
        icon_rect = icon.get_rect(center=(self.width // 2, self.height // 4))  # Position the icon at the top

        # Display the icon
        self.screen.blit(icon, icon_rect)

        # Display victory message
        victory_text = f"{winner} Wins!"
        text_color = (255, 0, 0) if winner == 'Imperial' else (0, 0, 255)  # Red for Imperial, Blue for Rebel
        victory_surface = self.font.render(victory_text, True, text_color)
        
        # Center the text below the icon
        text_rect = victory_surface.get_rect(center=(self.width // 2, self.height // 2 + icon_rect.height // 2))
        self.screen.blit(victory_surface, text_rect)  # Draw the victory text

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before returning to the main menu

    def __del__(self):
        # Remove the line that tries to release background_video if it's not defined
        pass

    def restart_game(self):
        # Reset the game state
        self.custom_board = CustomBoard(self)  # Reinitialize the custom board
        self.current_player = 'Imperial'  # Reset to the starting player
        self.game_over = False  # Reset game over state
