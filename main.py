import pygame
import sys
from scene.scene_instructions import SceneInstructions
from scene.scene_code import SceneCode
from utils.colors import *
from videoRenderer import VideoRenderer
import numpy as np

RECORD_VIDEO = False

# Pygame settings
WIDTH, HEIGHT = 1920, 1080
FRAMERATE = 60
BACKGROUND_COLOR = COLOR_BLACK

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Branchless Programming")
clock = pygame.time.Clock()

# Initialize scenes
scenes = [SceneCode(),SceneInstructions()]
scene_i = 0
tick = 0

running = True

# Create video renderer for the first scene

if RECORD_VIDEO:
    output_file = f"videos/{scenes[scene_i].__class__.__name__}.mp4"
    videoRenderer = VideoRenderer(FRAMERATE, WIDTH, HEIGHT, output_file)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if scene_i < len(scenes):
        scenes[scene_i].update(tick)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    if scene_i < len(scenes):
        scenes[scene_i].draw(screen)

    if scenes[scene_i].finish():

        if RECORD_VIDEO:
            videoRenderer.close()  # Ensure FFmpeg finishes the video before switching scenes
            if scene_i < len(scenes): 
                output_file = f"videos/{scenes[scene_i].__class__.__name__}.mp4"
                videoRenderer = VideoRenderer(FRAMERATE, WIDTH, HEIGHT, output_file)

        scene_i += 1  # Move to next scene

        if scene_i >= len(scenes):
            running = False  # No more scenes, exit loop

    # Update display
    pygame.display.flip()

    if RECORD_VIDEO:
        # Fix: Ensure frame format is correct before sending to FFmpeg (height, width, 3)
        videoRenderer.send_frame(np.moveaxis(pygame.surfarray.pixels3d(screen), 0, 1).tobytes())

    tick += 1
    clock.tick(FRAMERATE) 

if RECORD_VIDEO:
    videoRenderer.close()  # Ensure last video is properly saved

pygame.quit()
sys.exit()
