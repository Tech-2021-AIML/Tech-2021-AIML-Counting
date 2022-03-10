import yaml
import cv2 

if isinstance('config/station_cam.yaml', str):  # *.yaml file
    with open('config/station_cam.yaml') as f:
        cam_conf = yaml.load(f, Loader=yaml.SafeLoader)  # model dict



def crop_img(station_id , now ,sec):
    print('ok')
    for i ,r in enumerate(cam_conf['cams'][station_id]['route']):
        img = cv2.imread(f'img/station/{station_id}/image_{station_id}_{str(now)[0:-12]}_{str(sec)}.jpg')
        croped_img = img[0:100, 0:200]
        cv2.imwrite(f'img/croped/station/{station_id}/{r}/{str(now)[0:-12]}_{str(sec)}.jpg', croped_img)

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


# {route:['R1'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R1'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R2'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R2'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R2'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R3'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R3'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R3'],  crop_conf:[(0,0),(110,110)]},
#     {route:['R1','1R','R3'}
