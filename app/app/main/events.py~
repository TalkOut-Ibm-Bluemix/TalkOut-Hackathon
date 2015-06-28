from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio
#from .. import main
#from . import routes as r
#from r import main
import requests
import json
import pymongo
import re
import json
from pymongo import MongoClient
client= MongoClient("mongodb://rishav2708:rishu123@ds031601.mongolab.com:31601/ibm")
db=client["IBM"]
#url="http://192.168.1.30:9200/"

def extract_tag(stri,room):
    col=db[room]
    t1=col.find({"gname":room},{"_id":0,"trending":1})
    t=[]
    for i in t1:
        t=i['trending']
    print t
    l=re.findall('#[a-zA-Z0-9_]+',stri)
    k=[i for i in l if i not in t]
    return k
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    di={}
    room = session.get('room')
    #u=url+room+"/_search"
    join_room(room)
    emit('status', {'msg':"<span style='font-size:18px;color:#ff6600;text-align:center; margin-bottom:10px; border-bottom:1px solid black'>" + session.get('name') + ' has entered the room.'}, room=room)
    coll=db[room]
    chat=coll.find()
    l=[]
    for c in chat:
        try:
            emit('message',{'msg': "<div style='word-wrap:break-word; margin-right:5px;margin-top:3px;min-height:10px'>"+"<span id='names' style='float:left;max-width:10%;width:100%;margin-left:10px; color:#1234df'>"+c['name']+"</span>" + '<span style= "float:left;max-width:85%;width:100%;text-align:justify; margin-left:10px">'+ c['message']+"</span></div>"})
        except:
            l=c['trending']
            print l
            di={i:l.count(i) for i in l}
            #emit('notify',{'msg':'<div>Trending Now: <b>'+c['trend']+'</b></div>'})    
    print di
    da=[]
    for i in di.keys():
        da.append({"label":i,"value":di[i]})
    print da
    emit("draw",{'msg':str(da)})
    #print l
    #print di
    for i in di.keys():
        emit('notify',{'msg':'<div style="width:70%;bottom-border:1px solid #ff6600"><b>'+i+'</b></div>'})
    '''
    try:
        resp=requests.get(u).json()['hits']['hits']
        for i in resp:
    	   print i['_source']['message']
           emit('message',{'msg':i['_source']['message']})
    except: 
        emit('message',{'msg':"no data yet"},room=room)
    '''
def draw():
    col=db[room]
    t1=col.find({"gname":room},{"_id":0,"trending":1})
    t=[]
    for i in t1:
        t=i['trending']
    di={j:t.count(j) for j in t}
    return json.dumps(di)
    
    
    
@socketio.on('text', namespace='/chat')
def left(message):
    global di
    
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print type(room)
    emit('message',{'msg': "<div style='word-wrap:break-word; border:1px solid #6600ff; margin:5px'>"+"<span id='names' style='float:left;max-width:10%;width:100%; color:#1234df'>"+session.get("name")+"</span>" + '<span style= "float:left;max-width:85%;width:100%;text-align:justify; margin-left:10px">'+ message['msg']+"</span></div>"},room=room)
    #emit('message', {'msg': "<div style='word-wrap:break-word'>"+"<span id='names' style='float:left;max-width:10%;width:100%; background-color:#1234df'>"+c('name')+"</span>" + '<span style= "float:left;max-width:85%;width:100%;text-align:justify; margin-left:10px">'+ c['message']+"</span></div><hr>"}, room=room)
    #u=url+room+'/data/'
    print db.collection_names()
    if room not in db.collection_names():
        coll=db[room]
        print "In loop"
        d={"gname":room,"trending":[]}
        try:
            coll.insert(d)
        except:
            print ""
    coll=db[room]
    l=extract_tag(message['msg'],room)
    print l
    for i in l:
        emit('notify',{'msg':'<div style="border-bottom:1px solid #ff6600; width:70%"><b>'+i+'</b></div>'},room=room)
        try:
            coll.update({"gname":room},{"$push":{"trending":i}})
        except:
            print ""
    d={"name":session.get('name'),"message":message['msg'],"trending":l}
    try:
        coll.insert(d)
    except:
        print ""
    #print requests.post(u,data=json.dumps(d))

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    session['room']=''
    session['name']=''
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


