from geopy.geocoders import Nominatim
from celery import Celery
from pandas import infer_freq
import redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
import csv
import os
from datetime import datetime 
import db
from db import  *
import infer
from sqlalchemy import *
import sqlalchemy as sqldb
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus as urlquote
from sqlalchemy.sql import table, column, select, update, insert
from infer import my_predict
import matplotlib.pyplot as plt
import cv2

app = Celery(
    # XXX The below 'myapp' is the name of this module, for generating
    # task names when executed as __main__.
    'myapp',
    broker='redis://localhost:6379',
    # ## add result backend here if needed.
    # backend='rpc'
)
bus = False
station_id = 2
bus_id = 2
app.conf.timezone = 'UTC'

@app.task
def route_a_bus(starting_station, bus_id):
    now = datetime.now().second
    #fetch all the routs at that specific starting station
    session = session_factory()
    mytable = configTable('route')
    query = session.query(mytable)\
    .filter(mytable.columns.starting_station==starting_station)
    result = session.execute(query)
    route = result.fetchall()
    most_crowded_route = -1
    max_crowd = 0
    for r in  route:
        #fetch all the all the statoins on each route
        mytable = configTable('route_station')
        query = session.query(mytable)\
        .filter(mytable.columns.route_id==r[0])
        result = session.execute(query)
        route_station = result.fetchall()
        sum_crowd = 0
        #sum the counts of each station on each route
        for r_s in route_station:
            sum_crowd += r_s[3]
        #compare the summed count from the current maximum count
        if sum_crowd > max_crowd:
            max_crowd = sum_crowd
            most_crowded_route = r
    return most_crowded_route[1]
    
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
    now = datetime.now() 
    # get current second
    sec = now.second - now.second % 5
    count=my_predict(f'img/bus/{bus_id}/image_{sec}.jpg')
    # sava this pridiction to db cont table Bus columns station , routes, currernt_count
    # use session_factory() to get a new Session
    session = session_factory()
    mytable = configTable('bus')
    session.query(mytable)\
    .filter(mytable.columns.id == bus_id)\
    .update({mytable.columns.current_cout:count})
    session.commit()
    
@app.task
def send_photo_from_station(sett):
    # -7 sec
    # -10 min
    # -13 houre
    # -16 dayly
    print('send-ph-f-s')

    pass

@app.task
def send_count_from_station(station_id):
    #  from database get all routes in that sation save it routes variable
    session = session_factory()
    mytable = configTable('route')
    query = session.query(mytable)\
    .filter(mytable.columns.starting_station==station_id)
    result = session.execute(query)
    routes = result.fetchall()
    print("here is the count")
    print(routes)
    now = datetime.now() 
    # get current second
    sec = now.second - now.second % 5
    sec = sec-5
    for r in  routes:
        img_path_now = f'img/croped/station/{station_id}/{r[1]}/000.jpg'
        print(img_path_now)
        if os.path.exists(img_path_now):
            mytable_station = configTable('route_station')
            count =my_predict(img_path_now)
            # sava this pridiction to db cont table Route_station columns station , routes, currernt_count
            session.query(mytable_station)\
            .filter(mytable_station.columns.station_id == station_id)\
            .update({mytable_station.columns.current_count:count})
            print(session.query(mytable_station).all())
            session.commit()
    
@app.task
def send_location_from_bus(bus_id):
    # call get location python api
 
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    getLoc = loc.geocode("Location")

    # save to db count table bus culumns latitude and logtiude 
    session = session_factory()
    mytable = configTable('bus')
    session.query(mytable)\
    .filter(mytable.columns.id == bus_id)\
    .update({mytable.columns.latitude:getLoc.latitude, mytable.columns.longtiude:getLoc.longitude})
    session.commit()



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    if bus == True:
        sender.add_periodic_task(4.0, send_photo_from_bus.s('bus_id'))
        sender.add_periodic_task(4.0, send_location_from_bus.s('bus_id'))
        sender.add_periodic_task(4.0, send_count_from_bus.s('bus_id'))
    else:
    #     sender.add_periodic_task(4.0, send_photo_from_station.s('station_id'))
        sender.add_periodic_task(4.60, send_count_from_station.s(station_id))
        sender.add_periodic_task(4.60, send_photo_from_station.s(station_id))
    #     # sender.add_periodic_task(4.0, infere.s(['hellosfa']), name='write 2')
    #     # See periodic tasks user guide for more examples:
    # # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html



if __name__ == '__main__':
    app.start()
