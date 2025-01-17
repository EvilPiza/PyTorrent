import os

video_prefixes = ['mp4', 'wav']

def load_videos():
    for index in range(len(os.listdir("files"))):
        prefix = os.path.abspath(os.path.curdir)
        cfile = os.listdir(prefix + "\\files\\")[index]  
        info_path = os.path.abspath('/'.join((prefix + "\\files\\" + cfile + "\\info.txt").split('\\')))
        videos: dict[str, str | None] = {'foler_path': None, 'video_path': None}
        with open(info_path, "r") as info:
            for line in info:
                variable, value = line.split('=')
                variable, value = (variable.strip(), value.strip())
                videos[variable] = value
            videos['folder_path'] = info_path[:-8]
            info.close()
        for nested_file in os.listdir(f"files/{cfile}"):
            if nested_file[-3:] in video_prefixes:
                videos['video_path'] = os.path.abspath(nested_file)
    return videos
load_videos()