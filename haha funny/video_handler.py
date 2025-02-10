import subprocess
import os
import pygame
import api

def play_video(file_path):
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"  # Full VLC path
    file_path = fr'{'\\'.join(file_path.split('/'))}'
    if os.path.exists(file_path):
        print("Playing:", file_path)
        subprocess.run([vlc_path, file_path, "--no-osd"])
    else:
        print("File not found:", file_path)

def load_videos(VIDEO_DIR, is_online):
    if is_online:
        return api.get_posts()  # API fetch for online videos

    # Loading local offline videos
    video_list = []
    for video_folder in os.listdir(VIDEO_DIR):
        video_path = VIDEO_DIR + '/' +video_folder
        if os.path.isdir(video_path):
            info_path = os.path.join(video_path, "info.txt")
            if os.path.exists(info_path):
                with open(info_path, "r") as info_file:
                    info = [line.split('=')[-1].strip()[1:-1] for line in info_file.readlines()]
                    video_file = video_path + '/' + "video.mp4"
                    video_list.append({
                        "title": info[0],
                        "year released": info[1],
                        "studio": info[2],
                        "rating": info[3],
                        "pfolder": info[4],
                        "path": video_file,
                        "rect": pygame.Rect(0, 0, 200, 200)  # Initialize with a default rect
                    })
    return video_list