from flask import Flask,json,render_template
import json,pytz,dateutil.parser,time
from cron import *

if data_now == "null":
    data_now = data_null
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


app = Flask(__name__,static_url_path='/static')

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