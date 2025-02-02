# main.py

import pygame
import sys
from scene.scene_code import SceneCode
from scene.scene_instructions import SceneInstructions
from utils.colors import *

# Initialize Pygame
pygame.init()

# Screen dimensions

WIDTH, HEIGHT = 1920, 1080
BACKGROUND_COLOR = COLOR_BLACK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Branchless Programming")

# Clock for controlling frame rate
clock = pygame.time.Clock()

NUM_SCENES = 2
scene_i = 0

# Add objcts
scenes = []

scene_code = SceneCode()
scenes.append(scene_code)

scene_instructions = SceneInstructions()
scenes.append(scene_instructions)


# Main game loop
tick = 0
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if scene_i < NUM_SCENES:
        scenes[scene_i].update(tick)

        if scenes[scene_i].finish():
            scene_i+=1

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    if scene_i < NUM_SCENES:
        scenes[scene_i].draw(screen)

    # Update the display
    pygame.display.flip()

    tick+=1
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
