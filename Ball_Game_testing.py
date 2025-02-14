import pygame
import sys


pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EEG Brainball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

clock = pygame.time.Clock()
FPS = 60
ball_radius = 20
ball_speed = 5

# Goal positions
LEFT_GOAL_X = ball_radius
RIGHT_GOAL_X = WIDTH - ball_radius

font = pygame.font.SysFont("Roboto Mono", 24)


class Ball:
    def __init__(self, x, y, color, goal_direction):
        self.x = x
        self.y = y
        self.color = color
        self.progress = 0
        self.rect = pygame.Rect(self.x - ball_radius, self.y - ball_radius, ball_radius * 2, ball_radius * 2)
        self.goal_direction = goal_direction
        self.start_x = x
        self.goal_x = RIGHT_GOAL_X if goal_direction == 1 else LEFT_GOAL_X

    def move_with_eeg(self):
        try:
            att = attention_value  # Use without ()
            med = meditation_value
            print(f"Attention: {att}, Meditation: {med}")  # Debugging print

            if att > 50 and self.x + ball_speed < WIDTH - ball_radius:
                self.x += ball_speed
            if med > 50 and self.x - ball_speed > ball_radius:
                self.x -= ball_speed

            self.update_rect()
            self.update_progress()
        except Exception as e:
            print(f"EEG read error: {e}")

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), ball_radius)

    def update_rect(self):
        self.rect.topleft = (self.x - ball_radius, self.y - ball_radius)

    def update_progress(self):
        if self.goal_direction == 1:
            self.progress = ((self.x - self.start_x) / (self.goal_x - self.start_x)) * 100
        else:
            self.progress = ((self.start_x - self.x) / (self.start_x - self.goal_x)) * 100
        self.progress = max(0, min(100, self.progress))


def draw_progress(surface, player):
    pygame.draw.rect(surface, GREEN, (50, 50, 200, 25))
    pygame.draw.rect(surface, RED, (50, 50, 2 * player.progress, 25))
    progress_text = font.render(f"Progress: {int(player.progress)}%", True, BLACK)
    surface.blit(progress_text, (50, 80))


# Initialize **one** player
player = Ball(WIDTH // 4, HEIGHT // 2, RED, goal_direction=1)

running = True
while running:
    clock.tick(FPS)
    print("Game loop running")  # Debugging print

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (LEFT_GOAL_X, 0), (LEFT_GOAL_X, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (RIGHT_GOAL_X, 0), (RIGHT_GOAL_X, HEIGHT), 5)

    player.move_with_eeg()
    player.draw(screen)
    draw_progress(screen, player)

    pygame.display.flip()

pygame.quit()
sys.exit()
