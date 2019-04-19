import requests
import time
import subprocess
import os.path
import pathlib
import base64
from API import ApiComunicacion

class Camera():

    def __init__(self,recording):
        self.recording = recording
        self.api = ApiComunicacion()

    def record_video(self):
        print('Recording')
        url = 'http://127.0.0.1:8080/stream/video.mjpeg'
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)

        filename = time.strftime("%Y%m%d-%H%M%S")+'.mp4'
        save_path = '/home/pi/Downloads/tesis/video'
        completed_video= os.path.join(save_path, filename)

        i=0
        with open(completed_video, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    i = i + 1
                    #f.flush() commented by recommendation from J.F.Sebastian
                    if(self.recording == False or i==10000):
                        print('Sending')
                        f.close()
                        with open(completed_video,'rb') as f:
                            video = f.read()
                            encode_video = base64.encodebytes(video)

                            json = {'ip_address': '10.10.10.110',
                                    'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                                    'video': encode_video}

                            r = self.api.post(json,'createvideo')
                            a = r.json()
                            print(a)
                            path = pathlib.Path(completed_video)
                            path.unlink()
                            f.close()
                            break
        return local_filename

    def recording(self):
        self.recording = not self.recording

camera = Camera(True)

camera.record_video()