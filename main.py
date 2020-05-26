from flask import Flask,json,render_template
import json,pytz,dateutil.parser,time,logging
from werkzeug.middleware.proxy_fix import ProxyFix
from engine import curlup,curlnow,curlnow
import engine

live_member = ""
live_count = 0


hanayori = Flask(__name__,static_url_path='/static')
hanayori.wsgi_app = ProxyFix(hanayori.wsgi_app)


@hanayori.route('/')
def main():
    global live_count
    global live_member
    live_member,live_count = engine.live_status()
    return render_template('index.html',status=live_member,cnid=engine.channelid)

@hanayori.route('/Upcome')
def up():
    return render_template('upcome.html',title='Upcoming',data=engine.curlup(),status=live_member,cnid=engine.channelid)

@hanayori.route('/Live')
def live():
    return render_template('live.html',title='Live',data=engine.curlnow(),status=live_member,live_count=live_count,cnid=engine.channelid)

@hanayori.route('/Video/<ytid>')
def video(ytid=None):
    return render_template('video.html',title='Video',ytid=ytid,status=live_member,cnid=engine.channelid)

@hanayori.route('/Last')
def last():
    return render_template('last.html',title="Last live",data=engine.curllast(),status=live_member,cnid=engine.channelid)
