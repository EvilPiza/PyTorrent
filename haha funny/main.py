import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pytorrent go brrr")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Clock object to control frame rate
clock = pygame.time.Clock()

# Directory containing video files
VIDEO_DIR = "files"

# Function to load video data
def load_videos():
    videos = []
    for video_folder in os.listdir(VIDEO_DIR):
        video_path = os.path.join(VIDEO_DIR, video_folder)
        if os.path.isdir(video_path):
            # Attempt to read 'info.txt' from the video folder
            info_path = os.path.join(video_path, "info.txt")
            if os.path.exists(info_path):
                with open(info_path, "r") as info_file:
                    title = info_file.readline().strip()  # First line as title
                    video_file = os.path.join(video_path, "video.mp4")  # Assume the video file is named 'video.mp4'
                    if os.path.exists(video_file):
                        videos.append({"title": title, "path": video_file})
    return videos

# Load videos from the directory
videos = load_videos()

# Function to draw the boxes
def draw_boxes():
    for video in videos:
        video["rect"] = pygame.Rect(50, 50 + videos.index(video) * 250, 200, 200)  # Stagger boxes vertically
        pygame.draw.rect(screen, GREY, video["rect"])
        font = pygame.font.Font(None, 36)
        text = font.render(video["title"], True, BLACK)
        text_rect = text.get_rect(center=video["rect"].center)
        screen.blit(text, text_rect)

# Function to open video with VLC
def open_video(file_path):
    subprocess.run(["vlc", file_path])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                mouse_x, mouse_y = event.pos
                for video in videos:
                    if video["rect"].collidepoint(mouse_x, mouse_y):
                        print(f"Opening {video['title']}")
                        open_video(video["path"])

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the video boxes
    draw_boxes()

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
