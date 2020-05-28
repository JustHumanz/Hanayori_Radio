from flask import Flask,json,render_template
import json,pytz,dateutil.parser,time,logging
from werkzeug.middleware.proxy_fix import ProxyFix
from engine import curlup,curlnow,curlnow
import engine

#live member variable for temporary
live_member = ""
live_count = 0


hanayori = Flask(__name__,static_url_path='/static')
hanayori.wsgi_app = ProxyFix(hanayori.wsgi_app)

logging.basicConfig(filename='hanayori.log',level=logging.DEBUG)


@hanayori.route('/')
def main():
    global live_count
    global live_member
    #take data from live_status func in engine.py 
    live_member,live_count = engine.live_status()
    hanayori.logger.debug("Live count "+str(live_count))
    hanayori.logger.debug("Live member "+str(live_member))
    return render_template('index.html',status=live_member,cnid=engine.channelid)

@hanayori.route('/Upcome')
def up():
    data = engine.curlup()
    if data is None:
        hanayori.logger.debug("Upcome data is null")    
    else:
        hanayori.logger.debug("Upcome data "+str(data))
    return render_template('upcome.html',title='Upcoming',data=data,status=live_member,cnid=engine.channelid)

@hanayori.route('/Live')
def live():
    data = engine.curlnow()
    if data is None:
        hanayori.logger.debug("Upcome data is null")
    else:
        hanayori.logger.debug("Live data "+str(data))
    return render_template('live.html',title='Live',data=data,status=live_member,live_count=live_count,cnid=engine.channelid)

@hanayori.route('/Video/<ytid>')
def video(ytid=None):
    hanayori.logger.debug("Youtube ID "+str(ytid))
    return render_template('video.html',title='Video',ytid=ytid,status=live_member,cnid=engine.channelid)

@hanayori.route('/Last')
def last():
    data = engine.curllast()
    hanayori.logger.debug("Last len data "+str(len(data)))
    return render_template('last.html',title="Last live",data=engine.curllast(),status=live_member,cnid=engine.channelid)
