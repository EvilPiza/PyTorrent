from flask import Flask, jsonify
import os
import base64

app = Flask(__name__) 

@app.route('/', methods=['GET'])
def main():
    data = []

    for folder in os.listdir(os.curdir):
        folder_path = os.path.join(os.curdir, folder)
        
        info_path = os.path.join(folder_path, 'info.txt')
        if os.path.isdir(folder_path) and os.path.isfile(info_path):
            video = parse_info_file(info_path)
            data.append(video)

    return jsonify(data)

def parse_info_file(info_path):
    with open(info_path, 'r') as info_file:
        info = [line.split('=')[-1].strip()[1:-1] for line in info_file.readlines()]
        return {
            "title": info[0],
            "year released": info[1],
            "studio": info[2],
            "rating": info[3],
            "pfolder": info[4]
        }

@app.route('/get/<series>', methods = ['GET'])
def get_download_info(series):
    folders = [os.path.basename(i) for i in os.listdir(os.curdir)]
    if not series in folders:
        return "Sorry, bubs. Couldn't find anything."

    folder_path = os.path.join(os.curdir, series)

    info_file = os.path.join(folder_path, 'info.txt')
    video_path = os.path.join(folder_path, 'video.mp4')
    data_dict = parse_info_file(info_file)
    with open(video_path, 'rb') as video_file:
        video_binary = base64.b64encode(video_file.read()).decode('utf-8')
        data_dict.update({'binary': video_binary})
    return jsonify([data_dict])

if __name__ == '__main__': 
    os.curdir = os.curdir+'\\backend'
    app.run(host='0.0.0.0',port=50000, debug = True) 
