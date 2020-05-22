from flask import Flask,json,render_template
import json,pytz,dateutil.parser,time,logging
from werkzeug.middleware.proxy_fix import ProxyFix
from cron import data_up,data_last,data_now,data_null,data_up,live_status
import cron

hanayori = Flask(__name__,static_url_path='/static')
hanayori.wsgi_app = ProxyFix(hanayori.wsgi_app)


@hanayori.route('/')
def main(name=None):
    return render_template('index.html', name=name)

@hanayori.route('/Upcome')
def up():
    if data_up == "null":
        return render_template('upcome.html',title='Upcoming',data=cron.data_null,status=cron.live_status)
    else:
        return render_template('upcome.html',title='Upcoming',data=cron.data_up,status=cron.live_status)

@hanayori.route('/Live')
def live():
    if data_now == "null":
        return render_template('live.html',title='Live',data=cron.data_null,status=cron.live_status)
    else:
        return render_template('live.html',title='Live',data=cron.data_now,status=cron.live_status)

@hanayori.route('/Video/<ytid>')
def video(ytid=None):
    return render_template('video.html',title='Live',data=cron.data_now,ytid=ytid,status=cron.live_status)


@hanayori.route('/Last')
def last():
    return render_template('last.html',title="Last live",data=cron.data_last,status=cron.live_status)