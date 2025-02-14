import requests
import pygame
import base64
import os

url = 'https://pytorrent.onrender.com'

def get_error(error_code: int) -> None:
    if error_code == 503:
        print("Database is down right now! Try again later plz!! (Error: 503)")
    else:
        print(f"Yikes got error code '{error_code}' you should probably report this to the devs")

def get_posts():
    try:
        response = requests.get(url)

        if response.status_code != 200:
            get_error(response.status_code)
            return None

        posts = response.json()

        for post in posts:
            post.update({"rect": pygame.Rect(0, 0, 200, 200)})
        return posts
    
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def download_directory(parent_folder_name: str):
    os.mkdir(f"files/{parent_folder_name}")
    folder_path = os.path.join(os.getcwd(), 'files', parent_folder_name)
    series = folder_path.split('\\')[-1]

    try:
        response = requests.get(url+f'/get/{series}')
        if response.status_code != 200:
            get_error(response.status_code)
            return None

        for post in response.json():
            with open(folder_path+'/video.mp4', 'wb') as videoFile:
                videoFile.write(base64.b64decode(post['binary']))
            
            with open(folder_path+'/info.txt', 'w') as infoFile:
                infoFile.write(f'title = "{post["title"]}"\ndate_released = "{post["year released"]}"\nstudio = "{post["studio"]}"\nrating = "{post["rating"]}"')

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
