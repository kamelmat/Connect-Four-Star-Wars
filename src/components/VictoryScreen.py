import pygame

class VictoryScreen:
    def __init__(self, winner):
        self.winner = winner
        self.logo_image = self.load_logo()

    def load_logo(self):
        if self.winner == 'Imperial':
            return pygame.image.load("assets/images/imperial_logo.png")  # Path to Imperial logo
        else:
            return pygame.image.load("assets/images/rebel_logo.png")  # Path to Rebel logo

    def display(self, screen):
        # Scale the logo to fit the entire screen
        logo = pygame.transform.scale(self.logo_image, (screen.get_width(), screen.get_height()))
        screen.blit(logo, (0, 0))  # Draw the logo

        # Display the winning message
        font = pygame.font.Font(None, 74)
        text = font.render(f"{self.winner} Wins!", True, (255, 255, 255))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing
