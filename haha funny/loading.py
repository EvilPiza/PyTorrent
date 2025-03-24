import pygame
import api

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_loading():
    screen.fill((0, 0, 0))
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    
    # Draw text
    font = pygame.font.Font(None, 36)
    text = font.render("Loading...", True, (255, 255, 255))
    screen.blit(text, (center_x - text.get_width() // 2, center_y + 50))
    
    pygame.display.flip()

def run_loading_screen(long_function):
    def wrapper():
        pygame.display.set_caption(f'pytorrent - Connecting to: "{api.url}"')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            draw_loading()
            data = long_function()
            running = False
        return data
    return wrapper

