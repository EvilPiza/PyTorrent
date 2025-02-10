import requests
import pygame
import base64
import os

url = 'http://192.168.1.14:50000'


def get_posts():
    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()

            for post in posts:
                post.update({"rect": pygame.Rect(0, 0, 200, 200)})
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def download_directory(parent_folder_name):
    os.mkdir(f"files/{parent_folder_name}")
    folder_path = os.path.join(os.getcwd(), 'files', parent_folder_name)
    series = folder_path.split('\\')[-1]
    try:
        responses = requests.get(url+f'/get/{series}')
        if responses.status_code == 200:
            for response in responses.json():
                with open(folder_path+'/video.mp4', 'wb') as videoFile:
                    videoFile.write(base64.b64decode(response['binary']))
                
                with open(folder_path+'/info.txt', 'w') as infoFile:
                    infoFile.write(f'title = "{response['title']}"\ndate_released = "{response['year released']}"\nstudio = "{response['studio']}"\nrating = "{response['rating']}"')

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None