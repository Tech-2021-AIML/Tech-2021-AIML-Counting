from pickle import NONE
import yaml
import cv2 

if isinstance('config/station_cam.yaml', str):  # *.yaml file
    with open('config/station_cam.yaml') as f:
        cam_conf = yaml.load(f, Loader=yaml.SafeLoader)  # model dict


def crop_img(station_id, now, sec):
    print('ok')
    for i, r in enumerate(cam_conf['cams'][station_id]['route']):
        img_path = f'img/station/{station_id}/image_{station_id}_{str(now)[0:-12]}_{str(sec)}.jpg'
        img = cv2.imread(img_path)
        if os.path.exists(img_path):
            crop_axis = cam_conf['cams'][station_id]['crop_conf'][i]
            border_pixle = cam_conf['cams'][station_id]['border_conf'][i]
            croped_img = img[crop_axis[0]:crop_axis[2],
                             crop_axis[1]:crop_axis[3]]

            c = cv2.copyMakeBorder(
                croped_img, border_pixle[0], border_pixle[1], border_pixle[2], border_pixle[3], cv2.BORDER_CONSTANT
                ,value=(0, 0, 0))
            cv2.imwrite(
                f'img/croped/station/{station_id}/{r}/{str(now)[0:-12]}_{str(sec)}.jpg', croped_img)
            cv2.imwrite(
                f'img/croped/station/{station_id}/{r}/{str(now)[0:-12]}_{str(sec)}_boader.jpg', c)

import os
def no_file(Bus , bus_id,station_id,sec,now):
    if Bus:
        if os.path.exists(f'img/bus/{bus_id}/img_{bus_id}_{str(now)[0:-12]}_{str(sec)}.jpg'):
            return False
        return True        
    else:    
        if os.path.exists(f'img/station/{station_id}/image_{station_id}_{str(now)[0:-12]}_{str(sec)}.jpg'):
            return False
        return True


