import os
import cv2
import threading

from camera.models import Image
from datetime import datetime
from django.http import StreamingHttpResponse
from django.shortcuts import render

directory = os.getcwd()
file_path = directory + "/camera/templates/imgaes"


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.grabbed, self.frame = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()

    def take_frame(self):
        now = datetime.now()
        file_name = file_path + now.strftime("%y%m%d_%H%M%S") + ".png"
        cv2.imwrite(file_name, self.frame)

        image = Image(name=now.strftime("%y%m%d_%H%M%S"))
        image.save()


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield (b"--frmae\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def stream(request):
    try:
        return StreamingHttpResponse(
            gen(()), content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except:
        pass


def live(request):
    if request.method == "POST":
        cam.take_frame()

    return render(request, "design/html/live.html")


def playback(request):
    image_list = Image.objects.all()
    return render(request, "design/html/playback.html", {"image_list": image_list})


def setting(request):
    return render(request, "design/html/setting.html")
