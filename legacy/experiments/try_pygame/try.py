import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square with Circular Hole")

# Define colors
GREEN = (0, 255, 0)
TRANSPARENT = (0, 0, 0, 0)

# Define constants
SQUARE_SIZE = 200
CIRCLE_RADIUS = 80

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the green square
    square_rect = pygame.Rect((WIDTH - SQUARE_SIZE) // 2, (HEIGHT - SQUARE_SIZE) // 2, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, GREEN, square_rect)

    # Create a surface for the circle
    circle_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    
    # Draw the transparent circle
    pygame.draw.circle(circle_surface, TRANSPARENT, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), CIRCLE_RADIUS)

    # Blit the circle onto the square with the mask
    screen.blit(circle_surface, square_rect.topleft)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
