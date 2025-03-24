import subprocess
import os
import pygame
import api

def play_video(file_path: str):
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"  # Full VLC path
    file_path = '\\'.join(file_path.split('/'))
    command = [vlc_path, "--fullscreen", file_path, "--no-osd"]     # Auto fullscreen
    #command.remove("--fullscreen")    # Uncomment this line for not-auto-fullscreen
    
    if not os.path.exists(vlc_path):
        print("PyTorrent requires VLC to run! plz download it!! If you did and still get this error then report this to the devs plz!!")
        
    if os.path.exists(file_path):
        print("Playing:", file_path)
        subprocess.run(command)
    else:
        print("File not found:", file_path)

def load_videos(VIDEO_DIR: str, is_online: bool):
    if is_online:
        return api.get_posts()  # API fetch for online videos

    if not os.path.exists(VIDEO_DIR):
        os.mkdir(os.path.dirname(os.path.abspath(__file__))+'/files')

    # Loading local offline videos
    video_list = []
    for video_folder in os.listdir(VIDEO_DIR):
        video_path = VIDEO_DIR + '/' +video_folder
        if os.path.isdir(video_path):
            info_path = os.path.join(video_path, f"{video_folder}_info.txt")
            if os.path.exists(info_path):
                with open(info_path, "r") as info_file:
                    info = [line.split('=')[-1].strip()[1:-1] for line in info_file.readlines()]
                    videos = [file for file in os.listdir(video_path) if file.endswith('.mp4')]
                    video_list.append({
                        "title": info[0],
                        "year released": info[1],
                        "studio": info[2],
                        "rating": info[3],
                        "pfolder": info[4],
                        "path": video_path,
                        "episodes": videos,
                        "episode buttons": [],
                        "rect": pygame.Rect(0, 0, 200, 200)  # initialize with a default rect
                    })
    return video_list
