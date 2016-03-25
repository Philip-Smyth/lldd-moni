from flask import Flask as fl
from flask import request, Response, render_template, jsonify
import MySQLdb as msql
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue
import collections, json
from json import loads, dumps

app = fl(__name__)
def collect():
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
    return node_data

def collect_and_sort():    
    node_data = collect()
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
        return data
        count += 1

def table_data():
    raw_data = collect_and_sort()
    yield raw_data

def interactive_map_data():
    raw_data=collect_and_sort()
    cut_data = raw_data[6:]
    data = eval(cut_data)
    initial_json = {'name':'network','children': [{}]}
    node_data = []
    for node in data:
    	ip = data[node]['2']
    	mac = data[node]["3"]
    	os = data[node]["4"] + " " + data[node]["5"] + " " + data[node]["6"]
        node_data.append({"name":"node " + str(node),
                          "children": [{"name": ip},
                          {"name":mac},
                          {"name": os}
                          ]
                        })
    initial_json['children']=node_data
    double_quoted_json = str(initial_json).replace("'",'"')
    map_data=eval(double_quoted_json)
    return map_data

def write_to_file(data):
    f = open('/etc/porthole/static/net.json','w')
    repped_data = repr(data)
    final_data = repped_data.replace("'",'"')
    f.write(final_data)
    f.close()

@app.route('/my_event_source')
def sse_request():
    map_data=interactive_map_data()
    write_to_file(map_data)
    return Response(
             table_data(),
             mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('main.html')

@app.route('/network_map')
def network_map():
    return render_template('map.html')

if __name__ == '__main__':
    app.debug = True
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
