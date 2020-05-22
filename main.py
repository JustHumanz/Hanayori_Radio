from flask import Flask,json,render_template
import json,pytz,dateutil.parser,time
from werkzeug.middleware.proxy_fix import ProxyFix
from cron import *

hanayori = Flask(__name__,static_url_path='/static')
hanayori.wsgi_app = ProxyFix(hanayori.wsgi_app)


@hanayori.route('/')
def main(name=None):
    return render_template('index.html', name=name)

@hanayori.route('/Upcome')
def up():
    if data_up == "null":
        return render_template('upcome.html',title='Upcoming',data=data_null,status=live_status)
    else:
        return render_template('upcome.html',title='Upcoming',data=data_up,status=live_status)

@hanayori.route('/Live')
def live():
    if data_now == "null":
        return render_template('upcome.html',title='Upcoming',data=data_null,status=live_status)
    else:
        return render_template('live.html',title='Live',data=data_now,status=live_status)

@hanayori.route('/Live/<ytid>')
def live_id(ytid=None):
    return render_template('live_id.html',title='Live',data=data_now,ytid=ytid,status=live_status)


@hanayori.route('/Last')
def last():
    return render_template('last.html',title="Last live",data=data_last,status=live_status)