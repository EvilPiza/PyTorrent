import requests
import pygame
import base64
import os

url = 'https://pytorrent.onrender.com'

def get_posts():
    try:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Yikes got error code '{response.status_code}' you should probably report this to the devs")
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
        responses = requests.get(url+f'/get/{series}')
        if responses.status_code != 200:
            print(f"Yikes got error code '{responses.status_code}' you should probably report this to the devs")
            return None

        for response in responses.json():
            with open(folder_path+'/video.mp4', 'wb') as videoFile:
                videoFile.write(base64.b64decode(response['binary']))
            
            with open(folder_path+'/info.txt', 'w') as infoFile:
                infoFile.write(f'title = "{response["title"]}"\ndate_released = "{response["year released"]}"\nstudio = "{response["studio"]}"\nrating = "{response["rating"]}"')

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
