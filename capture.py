
from celery import Celery
from pandas import infer_freq
import redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
import csv
import datetime
from db import  session_factory
# import infer
app = Celery(
    # XXX The below 'myapp' is the name of this module, for generating
    # task names when executed as __main__.
    'myapp',
    broker='redis://localhost:6379',
    # ## add result backend here if needed.
    # backend='rpc'
)
bus = False
station_id = ''
bus_id = ''

import cv2
app.conf.timezone = 'UTC'
import matplotlib.pyplot as plt

from infer import my_predict

route_tuple = ((),('R1'),('R1'),('R1'),('R2'),('R2'),('R2'),('R3'),('R3'),('R3'),('R1','R2','R3'))

# from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://black:tikur@localhost/count', echo=True, future=True)
# conn = engine.connect()





'''infere model using infer predict method celery task'''
# app.task
# def infere(image):
#     ans,img,hmap = infer.predict('test_images/myimg/' + image)
#     print("Predict Count:",ans)
#     #Print count, image, heat map
#     plt.imshow(img.reshape(img.shape[1],img.shape[2],img.shape[3]))
#     plt.show()
#     plt.imshow(hmap.reshape(hmap.shape[1],hmap.shape[2]) , cmap = c.jet )
#     plt.show()
#     return ans


@app.task
def write_csv_hourly(sett):
    # -7 sec
    # -10 min
    # -13 houre
    # -16 dayly
    print('l')
    pass

@app.task
def send_photo_from_bus(sett):
    # -7 sec
    # -10 min
    # -13 houre
    # -16 dayly
    print('send-ph-f-b')
    pass
@app.task
def send_count_from_bus(bus_id):
    now = datetime.datetime.now() 
    # get current second
    sec = now.second - now.second % 5
    count =my_predict(f'test_images/capture/image_{str(sec)}.jpg')
    # sava this pridiction to db cont table Bus columns station , routes, currernt_count

    

    pass

@app.task
def send_photo_from_station(sett):
    # -7 sec
    # -10 min
    # -13 houre
    # -16 dayly
    print('send-ph-f-s')

    pass

from datetime import datetime
@app.task
def send_count_from_station(station_id):
    #  from database get all routes in that sation save it routes variable

    routes = []
    now = datetime.datetime.now() 
    # get current second
    sec = now.second - now.second % 5
    for r in  route_tuple[station_id]:
        count =my_predict(f'test_images/c/{station_id}/{r}/image_{str(sec)}.jpg')
        # sava this pridiction to db cont table Route_station columns station , routes, currernt_count

    print('send-c-f-s')

    pass
@app.task
def send_location_from_bus():
    # call get location python api
    # save to db count table bus culumns latitude and logtiude 

    pass


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    if bus == True:
        sender.add_periodic_task(4.0, send_photo_from_bus.s('bus_id'))
        sender.add_periodic_task(4.0, send_location_from_bus.s('bus_id'))
        sender.add_periodic_task(4.0, send_count_from_bus.s('bus_id'))
    else:
    #     sender.add_periodic_task(4.0, send_photo_from_station.s('station_id'))
        sender.add_periodic_task(4.0, send_count_from_station.s('station_id'))
        sender.add_periodic_task(4.0, send_photo_from_station.s('station_id'))
    #     # sender.add_periodic_task(4.0, infere.s(['hellosfa']), name='write 2')
    #     # See periodic tasks user guide for more examples:
    # # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html


if __name__ == '__main__':
    app.start()
