'''get_every_T_sec function caputre image from camera every given second T using opencv ,datetime and cv2'''
from matplotlib.pyplot import get
import cv2
from util import crop_img, no_file
import datetime


# params
Bus = False
bus_id = 1
station_id = 10


def get_every_T_sec(cam, T):
    '''get_every_T_sec function caputre image from camera every given second T using opencv ,datetime and cv2'''
    while True:
        # get current time
        now = datetime.datetime.now()
        # get current second
        sec = now.second
        # if current second is divisible by T
        if sec % T == 0 and no_file(Bus , bus_id, station_id, sec, now):
            # capture image
            ret, frame = cam.read()
            # save image
            if not Bus:
                cv2.imwrite(
                    f'img/station/{station_id}/image_{station_id}_{str(now)[0:-12]}_{str(sec)}.jpg', frame)
                crop_img(station_id, now ,sec)
            # display image
            else:
                cv2.imwrite(
                    f'img/bus/{bus_id}/img_{bus_id}_{str(now)[0:-12]}_{str(sec)}.jpg', frame)
            cv2.imshow('frame', frame)
            # wait for 1ms
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # release camera
    cam.release()
    # close all windows
    cv2.destroyAllWindows()


get_every_T_sec(cv2.VideoCapture(0), 5)
