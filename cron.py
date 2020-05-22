from flask import Flask,json,render_template
import json,dateutil.parser,time
from apscheduler.schedulers.background import BackgroundScheduler
from auth import urllib

data_up = ""
data_now = ""
data_last = ""
live_status=[{"Kano":False,
            "Hitona":False,
            "Hareru":False,
            "Nonono":False},
            {"live_count":0}]

def curlup():
    global data_up
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/upcoming')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    if values is None:
        data_up = [{"message": "Look like no scheduled live stream for now","null": True}]
    else:
        data_up = values

def curlnow():
    global data_now
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/now')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    if values is None:
        data_now = [{"message": "Look like no live stream for now","null": True}]
    else:
        data_now = values

def curllast():
    global data_last
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/last')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    data_last = values

def boot():
    curlup()
    curlnow()
    curllast()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(curlup,'interval',minutes=35)
    sched.add_job(curlnow,'interval',minutes=10)
    sched.add_job(curllast,'interval',minutes=30)
    sched.start()

boot()

if data_now[0]["null"] == True:
    pass
else:
    for i in range(len(data_now)):
        if data_now[i]['Data']['ytChannelId'] == "UCfuz6xYbYFGsWWBi3SpJI1w" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Kano"] = True
            live_status[1]["live_count"] += 1
        elif data_now[i]['Data']['ytChannelId'] == "UCV2m2UifDGr3ebjSnDv5rUA" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Hitona"] = True
            live_status[1]["live_count"] += 1
        elif data_now[i]['Data']['ytChannelId'] == "UCyIcOCH-VWaRKH9IkR8hz7Q" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Hareru"] = True
            live_status[1]["live_count"] += 1
        elif data_now[i]['Data']['ytChannelId'] == "UCiexEBp7-D46FXUtQ-BpgWg" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Nonono"] = True
            live_status[1]["live_count"] += 1



