from flask import Flask,json,render_template
import urllib,json,pytz,dateutil.parser,time
from apscheduler.schedulers.background import BackgroundScheduler

data_up = ""
data_now = ""
data_last = ""

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


app = Flask(__name__)

#2020-05-16 18:32:05-04:00
@app.before_request
def before_request_func():
    curlup()
    curlnow()
    curllast()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(curlup,'interval',minutes=10)
    sched.add_job(curlnow,'interval',minutes=50)
    sched.add_job(curllast,'interval',hours=1)
    sched.start()

@app.route('/')
def main(name=None):
    return render_template('index.html', name=name)

@app.route('/Upcome')
def up():
    if data_up == "null":
        status = {'status': 'foo'}
        channel = {'channelid' : 'bar'}
        return render_template('upcome.html', title='Upcoming', status=status,channel=channel)

    else:
        status = {'status': data_up[0]['Data']['status']}
        live = dateutil.parser.parse(data_up[0]['Data']['liveSchedule'])
        jst = {'time': live.astimezone(pytz.timezone("Asia/Tokyo"))}
        video = {'videoid' : data_up[0]['Data']['ytVideoId']}
        channel = {'channelid' : data_up[0]['Data']['ytChannelId']}
        return render_template('upcome.html', title='Upcoming', status=status,live=jst,video=video,channel=channel)


@app.route('/Live')
def live():
    if data_now == "null":
        status = {'status': 'null'}
        channel = {'channelid' : 'bar'}
        return render_template('live.html', title='Live', status=status,channel=channel)

    else:
        status = {'status': data_now[0]['Data']['status']}
        title_video = {'title': data_now[0]['Data']['title']}
        channel = {'channelid' : data_now[0]['Data']['ytChannelId']}
        video = {'videoid' : data_now[0]['Data']['ytVideoId']}
        return render_template('live.html', title='Live', title_video=title_video,channel=channel,video=video,status=status)