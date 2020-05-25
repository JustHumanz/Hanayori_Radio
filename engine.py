from flask import Flask,json,render_template
import pytz,json,dateutil.parser
from auth import urllib

channelid = ""


def timejst(value,format_time):
    utctime = dateutil.parser.parse(value)
    localtime = utctime.astimezone(pytz.timezone("Asia/Tokyo"))
    return localtime.strftime(format_time)

def curlup():
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/upcoming')
    response = urllib.request.urlopen(req)
    data_up = json.loads(response.read())

    if data_up is None:
        return([{"message": "Look like no scheduled live stream for now","null": True}])
    else:
        for i in range(len(data_up)):
            tmp = data_up[i]["Data"]["liveSchedule"]
            data_up[i]["Data"]["liveSchedule"] = timejst(tmp,"%H:%M:%S")

        return(data_up)

def curlnow():
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/now')
    response = urllib.request.urlopen(req)
    data_now = json.loads(response.read())
    if data_now is None:
        return([{"message": "Look like no live stream for now","null": True}])
    else:                
        return (data_now)

def curllast():
    req = urllib.request.Request('https://api.justhumanz.me/hanayori/live/last')
    response = urllib.request.urlopen(req)
    data_last = json.loads(response.read())
    for i in range(len(data_last)):
        tmp = data_last[i]["Data"]["liveSchedule"]
        data_last[i]["Data"]["liveSchedule"] = timejst(tmp,"%Y-%m-%d %H:%M")
    return(data_last)



def live_status():
    global channelid
    channelid=["UCfuz6xYbYFGsWWBi3SpJI1w","UCV2m2UifDGr3ebjSnDv5rUA","UCyIcOCH-VWaRKH9IkR8hz7Q","UCiexEBp7-D46FXUtQ-BpgWg"]
    live_count = 0
    live_member=[{"Kano":False,
    "Hitona":False,
    "Hareru":False,
    "Nonono":False}]
    data_now = curlnow()

    if data_now[0]['null'] == False :
        for i in range(len(data_now)):
            if data_now[i]['Data']['ytChannelId'] == channelid[i] and data_now[i]['Data']['status'] == 'live':
                live_member[0]["Kano"] = True
                live_count += 1
            elif data_now[i]['Data']['ytChannelId'] == channelid[i] and data_now[i]['Data']['status'] == 'live':
                live_member[0]["Hitona"] = True
                live_count += 1
            elif data_now[i]['Data']['ytChannelId'] == channelid[i] and data_now[i]['Data']['status'] == 'live':
                live_member[0]["Hareru"] = True
                live_count += 1
            elif data_now[i]['Data']['ytChannelId'] == channelid[i] and data_now[i]['Data']['status'] == 'live':
                live_member[0]["Nonono"] = True
                live_count += 1
                
        return live_member,live_count

    else:
        return live_member,live_count
