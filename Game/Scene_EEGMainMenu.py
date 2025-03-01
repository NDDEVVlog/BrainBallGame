import pygame
import sys
import serial.tools.list_ports
from Scene_Game import Scene_Game  # Import the Brainball game
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
DISABLED_COLOR = (150, 150, 150)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brainball Game Menu")

# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)


class GameMenu:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager  # Store SceneManager reference
        self.running = True
        self.com_ports = self.get_com_ports()  # Fetch available COM ports
        self.selected_port = None
        self.selected_port_2 = None
        self.dropdown_open = False
        self.dropdown_open_2 = False  # Second dropdown state

    def get_com_ports(self):
        """Get available COM ports"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def draw_button(self, text, x, y, width, height, hover, enabled=True):
        """Draw a button"""
        color = BUTTON_HOVER if hover else (BUTTON_COLOR if enabled else DISABLED_COLOR)
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (x + 10, y + 10))

    def draw_dropdown(self, x, y, width, height, selected_port, dropdown_open, dropdown_id):
        """Draw the COM port selection dropdown"""
        pygame.draw.rect(screen, DROPDOWN_COLOR, (x, y, width, height))

        # Show selected COM port or default text
        text_surface = small_font.render(
            selected_port if selected_port else f"Select COM {dropdown_id}", True, BLACK
        )
        screen.blit(text_surface, (x + 10, y + 10))

        # Draw dropdown options if open
        if dropdown_open:
            for i, port in enumerate(self.com_ports):
                # Ensure the same port is not selected twice
                is_disabled = (dropdown_id == 1 and port == self.selected_port_2) or \
                              (dropdown_id == 2 and port == self.selected_port)
                
                option_rect = pygame.Rect(x, y + (i + 1) * height, width, height)
                color = SELECTED_COLOR if port == selected_port else (DISABLED_COLOR if is_disabled else DROPDOWN_COLOR)
                
                pygame.draw.rect(screen, color, option_rect)
                text_surface = small_font.render(port, True, BLACK)
                screen.blit(text_surface, (x + 10, y + (i + 1) * height + 10))

    def run_game(self):
        """Launch the Brainball game"""
        if self.selected_port and self.selected_port_2:
            self.scene_manager.get_scene("Game").ConnectEEGDEVICE(self.selected_port, self.selected_port_2)
            self.scene_manager.switch_scene("Game")

    def run(self):
        """Main menu loop"""
        screen.fill(WHITE)
        
        # Title
        title = font.render("Brainball Collision Game", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - 150, 50))
        
        # Buttons
        start_button_y = 200
        exit_button_y = 270
        dropdown_y = exit_button_y + 70
        dropdown_x_2 = 520  # Position for second dropdown
        
        start_hover = start_button_y <= pygame.mouse.get_pos()[1] <= start_button_y + 50
        exit_hover = exit_button_y <= pygame.mouse.get_pos()[1] <= exit_button_y + 50
        
        # Enable start button only if both COM ports are selected
        start_enabled = self.selected_port and self.selected_port_2
        self.draw_button("Start Game", 300, start_button_y, 200, 50, start_hover, start_enabled)

        self.draw_button("Exit", 300, exit_button_y, 200, 50, exit_hover)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Toggle first dropdown
                if 300 <= x <= 500 and dropdown_y <= y <= dropdown_y + 40:
                    self.dropdown_open = not self.dropdown_open
                    self.dropdown_open_2 = False  # Close second dropdown when first is opened

                # Toggle second dropdown
                if dropdown_x_2 <= x <= dropdown_x_2 + 200 and dropdown_y <= y <= dropdown_y + 40:
                    self.dropdown_open_2 = not self.dropdown_open_2
                    self.dropdown_open = False  # Close first dropdown when second is opened

                # Select COM port from first dropdown
                if self.dropdown_open:
                    for i, port in enumerate(self.com_ports):
                        option_rect = pygame.Rect(300, dropdown_y + (i + 1) * 40, 200, 40)
                        if option_rect.collidepoint(x, y) and port != self.selected_port_2:
                            self.selected_port = port
                            self.dropdown_open = False

                # Select COM port from second dropdown
                if self.dropdown_open_2:
                    for i, port in enumerate(self.com_ports):
                        option_rect = pygame.Rect(dropdown_x_2, dropdown_y + (i + 1) * 40, 200, 40)
                        if option_rect.collidepoint(x, y) and port != self.selected_port:
                            self.selected_port_2 = port
                            self.dropdown_open_2 = False

                # Start button
                if 300 <= x <= 500 and start_button_y <= y <= start_button_y + 50 and start_enabled:
                    self.run_game()
                    
                # Exit button
                if 300 <= x <= 500 and exit_button_y <= y <= exit_button_y + 50:
                    self.scene_manager.ForceExit()

        # Draw both dropdowns
        self.draw_dropdown(300, dropdown_y, 200, 40, self.selected_port, self.dropdown_open, 1)
        self.draw_dropdown(dropdown_x_2, dropdown_y, 200, 40, self.selected_port_2, self.dropdown_open_2, 2)

        pygame.display.flip()
