from flask import Flask,json,render_template
import json,dateutil.parser,time
from apscheduler.schedulers.background import BackgroundScheduler
from auth import *

data_up = ""
data_now = ""
data_last = ""
live_status=[{"Kano":False,"Hitona":False,"Hareru":False,"Nonono":False},{"live_count":0}]


def curlup():
    global data_up
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/upcoming')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    if values is None:
        data_up = "null"
    else:
        data_up = values

def curlnow():
    global data_now
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/now')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    if values is None:
        data_now = "null"
    else:
        data_now = values

def curllast():
    global data_last
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/last')
    response = urllib.request.urlopen(req)
    values = json.loads(response.read())
    if values is None:
        data_last = "null"
    else:
        data_last = values

def boot():
    curlup()
    curlnow()
    curllast()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(curlup,'interval',hours=1)
    sched.add_job(curlnow,'interval',minutes=30)
    sched.add_job(curllast,'interval',hours=1)
    sched.start()
boot()


data_null = [{"Data":{"description":"foo","durationSecs":"None","embeddable":'true',"lateSecs":0,"liveChat":"foo","liveEnd":"bar","liveSchedule":"foo","liveStart":"bar","liveViewers":"foo","publishedAt":"foo","status":"bar","thumbnail":"foo","title":"foo","ytChannelId":"bar","ytVideoId":"foo"}}]
