import requests
import pygame
import base64
import os
import loading

url = 'http://127.0.0.1:50000'#'https://pytorrent.onrender.com'

def get_error(error_code: int) -> None:
    if error_code == 503:
        print("Database is down right now! Try again later plz!! (Error: 503)")
    else:
        print(f"Yikes got error code '{error_code}' you should probably report this to the devs")

@loading.run_loading_screen
def get_posts():
    try:
        response = requests.get(url, timeout=30)

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
    try:
        os.mkdir(f"files/{parent_folder_name}")
    except FileExistsError:
        pass
    folder_path = os.path.join(os.getcwd(), 'files', parent_folder_name)
    series = folder_path.split('\\')[-1]

    try:
        response = requests.get(url+f'/get/{series}')
        if response.status_code != 200:
            get_error(response.status_code)
            return None

        for index, post in enumerate(response.json()):
            for binary in post['binary']:
                with open(folder_path+f'/{series}_{index+1}.mp4', 'wb') as videoFile:
                    videoFile.write(base64.b64decode(base64.b64encode(str.encode(binary))))
            
            with open(folder_path+f'/{series}_info.txt', 'w') as infoFile:
                infoFile.write(f'title = "{post["title"]}"\ndate_released = "{post["year released"]}"\nstudio = "{post["studio"]}"\nrating = "{post["rating"]}"\npfolder = "{post["pfolder"]}"')

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
