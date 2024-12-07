import pygame
import time
import sys
from random import randint

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1920
screen_height = 1080

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Text Screensaver")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Font settings
font_size = 14
font = pygame.font.SysFont("arial", font_size)

# Text to display
text = "All work and no play makes Jack a dull boy. "
char_index = 0  # Index of the current character to display
text_position = [0, 0]  # Start at the top left
line_height = font_size + 4  # Space between lines

# Color interpolation settings
color_change_speed = 0.005  # Speed of color change
color_value = 0  # Initial color value
color_direction = 1  # Initial color change direction (1 for increasing, -1 for decreasing)

last_mouse_position = pygame.mouse.get_pos()

pygame.mouse.set_visible(False)

def interpolate_color(start_color, end_color, factor):
    #Interpolate between two colors with a given factor (0 to 1).
    return tuple(int(start + (end - start) * factor) for start, end in zip(start_color, end_color))

def screensaver():
    global char_index, text_position, last_mouse_position, color_value, color_direction

    running = True
    displayed_text = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        # Check for mouse movement
        current_mouse_position = pygame.mouse.get_pos()
        if current_mouse_position != last_mouse_position:
            running = False
        last_mouse_position = current_mouse_position

        if char_index < len(text):
            displayed_text += text[char_index]
            char_index += 1
        else:
            displayed_text += text[char_index % len(text)]
            char_index += 1

        screen.fill(black)  # Clear the screen

        words = displayed_text.split(' ')
        x, y = 0, 0

        # Update color value
        color_value += color_direction * color_change_speed
        if color_value >= 1:
            color_value = 1
            color_direction = -1
        elif color_value <= 0:
            color_value = 0
            color_direction = 1

        current_color = interpolate_color(white, red, color_value)

        for word in words:
            word_surface = font.render(word + ' ', True, current_color)
            word_width, word_height = word_surface.get_size()

            # Check if the word fits in the current line
            if x + word_width > screen_width:
                # Move to the next line
                x = 0
                y += line_height

            # Check if the text reaches the bottom of the screen
            if y + line_height > screen_height:
                # Scroll the screen up
                screen.scroll(0, -line_height)
                y -= line_height
                # Fill the newly exposed area with black
                pygame.draw.rect(screen, black, pygame.Rect(0, screen_height - line_height, screen_width, line_height))

            screen.blit(word_surface, (x, y))
            x += word_width

        pygame.display.update()
        time.sleep(randint(5, 10) / 100)
        #time.sleep(0.01)

    pygame.quit()
    sys.exit()

# Run the screensaver
screensaver()