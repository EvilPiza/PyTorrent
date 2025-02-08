import pygame
import sys
import video_handler
import save_data

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pytorrent go brrr")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

clock = pygame.time.Clock()

MAIN_DIR = save_data.get_main_directory()
VIDEO_DIR = MAIN_DIR + "/files"
SCROLL_SPEED = 50

running = True
in_video_menu = False
selected_video = None
scroll_offset = 0

is_online = False
button_rect = pygame.Rect(50, 500, 200, 50)

videos = video_handler.load_videos(VIDEO_DIR, is_online)


def wrap_text(text, font, box_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + ' ' + word
        if font.size(test_line)[0] <= box_width:
            current_line = test_line 
        else:
            lines.append(current_line) 
            current_line = word

    lines.append(current_line)
    return lines

def draw_video_boxes(scroll_offset):
    columns = 2
    box_width = 200
    box_height = 200
    margin = 50
    start_y_pos = 100
    border_radius = 20
    font = pygame.font.Font(None, 24)

    for index, video in enumerate(videos):
        
        col = index % columns
        row = index // columns
        x_pos = margin + col * (box_width + margin)
        y_pos = start_y_pos + row * (box_height + margin) - scroll_offset

        if y_pos + box_height > 0 and y_pos < SCREEN_HEIGHT:
            video["rect"] = pygame.Rect(x_pos, y_pos, box_width, box_height)
            pygame.draw.rect(screen, GREY, video["rect"], border_radius=border_radius)

            title_lines = wrap_text(video["title"], font, box_width - 20)

            for i, line in enumerate(title_lines):
                text = font.render(line, True, BLACK)
                text_rect = text.get_rect(center=(video["rect"].centerx, video["rect"].top + 20 + i * 30))
                screen.blit(text, text_rect)

def draw_scrollbar(scroll_offset):
    scrollbar_width = 20
    total_height = len(videos) * 250
    visible_area = SCREEN_HEIGHT
    scrollbar_ratio = visible_area / total_height

    if total_height <= visible_area:
        scrollbar_height = visible_area
    else:
        scrollbar_height = max(visible_area * scrollbar_ratio, 40)

    scrollbar_position = (scroll_offset / (total_height - visible_area)) * (visible_area - scrollbar_height)

    pygame.draw.rect(screen, GREY, pygame.Rect(SCREEN_WIDTH - scrollbar_width, 0, scrollbar_width, visible_area))
    pygame.draw.rect(screen, BLACK, pygame.Rect(SCREEN_WIDTH - scrollbar_width, scrollbar_position, scrollbar_width, scrollbar_height))

def draw_video_details(video):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    title_text = font.render(f"Title: {video['title']}", True, BLACK)
    screen.blit(title_text, (50, 50))

    year_text = font.render(f"Year Released: {video['year released']}", True, BLACK)
    screen.blit(year_text, (50, 100))

    studio_text = font.render(f"Studio: {video['studio']}", True, BLACK)
    screen.blit(studio_text, (50, 150))

    rating_text = font.render(f"Rating: {video['rating']}", True, BLACK)
    screen.blit(rating_text, (50, 200))

    play_button = pygame.Rect(50, 250, 200, 50)
    pygame.draw.rect(screen, GREY, play_button, border_radius=10)
    play_text = font.render("Play", True, BLACK)
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

    back_button = pygame.Rect(50, 350, 200, 50)
    pygame.draw.rect(screen, GREY, back_button, border_radius=10)
    back_text = font.render("Go Back", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    back_instructions = pygame.font.Font(None, 24).render("Press 'B' to go back", True, BLACK)
    screen.blit(back_instructions, (50, 410))

    return play_button, back_button

def online_button():
    button_color = GREY if not is_online else (0, 255, 0)
    button_text = "Online" if is_online else "Offline"
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    button_font = pygame.font.Font(None, 36)
    button_label = button_font.render(button_text, True, BLACK)
    button_label_rect = button_label.get_rect(center=button_rect.center)
    screen.blit(button_label, button_label_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if in_video_menu and selected_video:
                    play_button, back_button = draw_video_details(selected_video)
                    if play_button.collidepoint(mouse_x, mouse_y):
                        try:
                            video_handler.play_video(selected_video["path"])
                        except Exception as e:
                            print(e)
                    elif back_button.collidepoint(mouse_x, mouse_y):
                        in_video_menu = False
                        selected_video = None
                else:
                    for video in videos:
                        if video["rect"].collidepoint(mouse_x, mouse_y):
                            selected_video = video
                            in_video_menu = True
                if button_rect.collidepoint(mouse_x, mouse_y):
                    is_online = not is_online
                    videos = video_handler.load_videos(VIDEO_DIR, is_online)
                    in_video_menu = False
                    selected_video = None
            elif event.button == 4: 
                scroll_offset -= SCROLL_SPEED
                if scroll_offset < 0:
                    scroll_offset = 0
            elif event.button == 5: 
                scroll_offset += SCROLL_SPEED
                if scroll_offset > len(videos) * 250 - SCREEN_HEIGHT:
                    scroll_offset = len(videos) * 250 - SCREEN_HEIGHT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                in_video_menu = False
                selected_video = None
            elif event.key == pygame.K_DOWN:
                scroll_offset += SCROLL_SPEED
                if scroll_offset > len(videos) * 250 - SCREEN_HEIGHT:
                    scroll_offset = len(videos) * 250 - SCREEN_HEIGHT
            elif event.key == pygame.K_UP:
                scroll_offset -= SCROLL_SPEED
                if scroll_offset < 0:
                    scroll_offset = 0

    screen.fill(WHITE)

    if in_video_menu and selected_video:
        draw_video_details(selected_video)
    else:
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Available Videos", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50 - scroll_offset))
        screen.blit(title_text, title_rect)

        draw_video_boxes(scroll_offset)
        draw_scrollbar(scroll_offset)

    online_button()
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
