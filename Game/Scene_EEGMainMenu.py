import pygame
import sys
import serial.tools.list_ports
from Game import Game  # Import the Brainball game
from SceneManager import SceneManager

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER = (150, 255, 150)
DROPDOWN_COLOR = (200, 200, 200)
SELECTED_COLOR = (180, 180, 180)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brainball Game Menu")

# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)


class GameMenu:
    def __init__(self,scene_manager):
        self.scene_manager = scene_manager  # Store SceneManager reference
        self.running = True
        self.com_ports = self.get_com_ports()  # Fetch available COM ports
        self.selected_port = None
        self.dropdown_open = False

    def get_com_ports(self):
        """Get available COM ports"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def draw_button(self, text, x, y, width, height, hover):
        """Draw a button"""
        color = BUTTON_HOVER if hover else BUTTON_COLOR
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 10, y + 10))

    def draw_dropdown(self, x, y, width, height):
        """Draw the COM port selection dropdown"""
        pygame.draw.rect(screen, DROPDOWN_COLOR, (x, y, width, height))

        # Show selected COM port or default text
        text_surface = small_font.render(
            self.selected_port if self.selected_port else "Select COM Port", True, BLACK)
        screen.blit(text_surface, (x + 10, y + 10))

        # Draw dropdown options if open
        if self.dropdown_open:
            for i, port in enumerate(self.com_ports):
                option_rect = pygame.Rect(x, y + (i + 1) * height, width, height)
                pygame.draw.rect(screen, SELECTED_COLOR if port == self.selected_port else DROPDOWN_COLOR, option_rect)
                text_surface = small_font.render(port, True, BLACK)
                screen.blit(text_surface, (x + 10, y + (i + 1) * height + 10))

    def run_game(self):
        """Launch the Brainball game"""
        if self.selected_port:
            #print(f"Starting game with {self.selected_port}...")
            

            self.scene_manager.get_scene("Game").ConnectEEGDEVICE(self.selected_port)
            self.scene_manager.switch_scene("Game")

    def run(self):
        """Main menu loop"""
        #while self.running:
        screen.fill(WHITE)
        # Title
        title = font.render("Brainball Collision Game", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - 150, 50))
        # Buttons
        start_button_y = 200
        exit_button_y = 270  # Adjusted to keep space between buttons
        dropdown_y = exit_button_y + 70  # **Placed BELOW Exit Button**
        start_hover = start_button_y <= pygame.mouse.get_pos()[1] <= start_button_y + 50
        exit_hover = exit_button_y <= pygame.mouse.get_pos()[1] <= exit_button_y + 50
        # Enable start button only if COM port is selected
        if self.selected_port:
            self.draw_button("Start Game", 300, start_button_y, 200, 50, start_hover)
        else:
            pygame.draw.rect(screen, (150, 150, 150), (300, start_button_y, 200, 50))
            text_surface = font.render("Start Game", True, BLACK)
            screen.blit(text_surface, (310, start_button_y + 10))
        self.draw_button("Exit", 300, exit_button_y, 200, 50, exit_hover)
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Toggle dropdown
                if 300 <= x <= 500 and dropdown_y <= y <= dropdown_y + 40:
                    self.dropdown_open = not self.dropdown_open
                # Select COM port from dropdown
                if self.dropdown_open:
                    for i, port in enumerate(self.com_ports):
                        option_rect = pygame.Rect(300, dropdown_y + (i + 1) * 40, 200, 40)
                        if option_rect.collidepoint(x, y):
                            self.selected_port = port
                            self.dropdown_open = False
                # Start button
                if 300 <= x <= 500 and start_button_y <= y <= start_button_y + 50 and self.selected_port:
                    self.run_game()
                    
                # Exit button
                if 300 <= x <= 500 and exit_button_y <= y <= exit_button_y + 50:
                    self.scene_manager.ForceExit()
        # Draw dropdown **LAST** so it appears on top
        self.draw_dropdown(300, dropdown_y, 200, 40)
        pygame.display.flip()

        #pygame.quit()
        #sys.exit()