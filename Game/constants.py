# constants.py
import pygame

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 25
BALL_SPEED = 5

# EEG Constants
SF = 512             # Sampling frequency of EEG
BUFFER_SEC = 4       # EEG buffer in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pygame Initialization
pygame.init()
