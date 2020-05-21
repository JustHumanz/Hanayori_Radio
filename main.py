from flask import Flask,json,render_template
import urllib,json,pytz,dateutil.parser,time
from apscheduler.schedulers.background import BackgroundScheduler

data_up = ""
data_now = ""
data_last = ""
live_status=[{"Kano":False,"Hitona":False,"Hareru":False,"Nonono":False}]


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

if data_now == "null":
    data_now = data_null
else:
    for i in range(len(data_now)):
        if data_now[i]['Data']['ytChannelId'] == "UCfuz6xYbYFGsWWBi3SpJI1w" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Kano"] = True
        elif data_now[i]['Data']['ytChannelId'] == "UCV2m2UifDGr3ebjSnDv5rUA" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Hitona"] = True
        elif data_now[i]['Data']['ytChannelId'] == "UCyIcOCH-VWaRKH9IkR8hz7Q" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Hareru"] = True
        elif data_now[i]['Data']['ytChannelId'] == "UCiexEBp7-D46FXUtQ-BpgWg" and data_now[i]['Data']['status'] == 'live':
            live_status[0]["Nonono"] = True


app = Flask(__name__)

@app.route('/')
def main(name=None):
    return render_template('index.html', name=name)

@app.route('/Upcome')
def up():
    if data_up == "null":
        return render_template('upcome.html',title='Upcoming',data=data_null,status=live_status)
    else:
        return render_template('upcome.html',title='Upcoming',data=data_up,status=live_status)

@app.route('/Live')
def live():
    if data_now == "null":
        return render_template('upcome.html',title='Upcoming',data=data_null,status=live_status)
    else:
        return render_template('live.html',title='Live',data=data_now,status=live_status)

@app.route('/Live/<ytid>')
def live_id(ytid=None):
    return render_template('live_id.html',title='Live',data=data_now,ytid=ytid,status=live_status)


@app.route('/Last')
def last():
    return render_template('last.html',title="Last live",data=data_last,status=live_status)