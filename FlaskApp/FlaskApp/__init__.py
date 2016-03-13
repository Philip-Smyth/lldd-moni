from flask import Flask as fl
from flask import request, Response, render_template, jsonify
import MySQLdb as msql
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
import collections, json
from json import loads, dumps
from flask_bootstrap import Bootstrap
app = fl(__name__)

def event_stream():
    con = msql.connect(host='localhost', user='root', passwd='password', db='discover')
    cur = con.cursor()
    check = "SHOW TABLES LIKE 'nodes'"
    cur.execute(check)
    result = cur.fetchone()
    if result:
        pass
    else:
        cur.execute('CREATE TABLE nodes (Id INTEGER NOT NULL AUTO_INCREMENT,Hostname VARCHAR(30), MAC_Addr VARCHAR(18),IP_Addr VARCHAR(15), OS VARCHAR(10),OS_Vrs VARCHAR(10), OS_Type VARCHAR(30),OS_Acc VARCHAR(3),PRIMARY KEY (Id))')
    cur.execute('SELECT * from nodes')
    node_data = cur.fetchall()

    dictionary = collections.OrderedDict()
    dt={}   
    count = 0

    while True:
        gevent.sleep(2)
        for node in node_data:
            index="%s" % str(int(node[0]))
            dictionary[index]=collections.OrderedDict()
            y=0
            for info in node:

                if y==0:
                    key="0"
                    info=str(info)
                elif y==1:
                    key="1"
                elif y==2:
                    key="2"
                elif y==3:
                    key="3"
                elif y==4:
                    key="4"
                elif y==5:
                    key="5"
                elif y==6:
                    key="6"
                elif y==7:
                    key="7"
                y+=1
                dictionary[index][key]=info             
            dictionary[index]= collections.OrderedDict(sorted(dictionary[index].items()))

        #need to apply sql collection to output like this
        dictionary=dict(dictionary)
        dt=dumps(dictionary, sort_keys=True)
        data='data: %s\n\n' % str(dt)
        yield data
        count += 1

@app.route('/my_event_source')
def sse_request():
    return Response(
             event_stream(),
             mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('main.html')

if __name__ == '__main__':
    app.debug = True
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()