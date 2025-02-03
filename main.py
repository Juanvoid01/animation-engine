import pygame
import sys
from scene.scene_instructions import SceneInstructions
from utils.colors import *
from videoRenderer import VideoRenderer
import numpy as np

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
scenes = [SceneInstructions()]
scene_i = 0
tick = 0
running = True

# ✅ Create video renderer for the first scene
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

    # ✅ Check if scene is finished
    if scenes[scene_i].finish():
        videoRenderer.close()  # ✅ Ensure FFmpeg finishes the video before switching scenes
        scene_i += 1  # Move to next scene

        if scene_i < len(scenes):  # ✅ Only create a new renderer if scenes remain
            output_file = f"videos/{scenes[scene_i].__class__.__name__}.mp4"
            videoRenderer = VideoRenderer(FRAMERATE, WIDTH, HEIGHT, output_file)
        else:
            running = False  # No more scenes, exit loop

    # Update display
    pygame.display.flip()

    # ✅ Fix: Ensure frame format is correct before sending to FFmpeg
    frame = pygame.surfarray.pixels3d(screen)  # (width, height, 3)
    frame = np.swapaxes(frame, 0, 1)  # Convert to (height, width, 3)
    frame_bytes = frame.tobytes()

    # Send frame to FFmpeg
    videoRenderer.send_frame(frame_bytes)

    tick += 1
    clock.tick(FRAMERATE)  # Maintain FPS

# Cleanup
videoRenderer.close()  # Ensure last video is properly saved

pygame.quit()
sys.exit()
