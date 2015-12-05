from bottle import route, run,response, request, re
import requests, json
import re
import simplejson
import sqlite3
import string
import ast

conn = sqlite3.connect("example.db")
c = conn.cursor()

def list_to_dict(li):
    dct = {}
    for item in li:
        if dct.has_key(item):
            dct[item] = dct[item] + 1
        else:
            dct[item] = 1
    return dct

@route('/test', method='GET')
def basic():
    response.set_header('Accept', '*/*')
    response.set_header('Allow', 'GET, HEAD')
    return 'Test'

@route('/send', method='POST')
def sending():
    response.content_type = 'application/json'
    resp_json=request.json
    columns = list(resp_json.keys())
    for i in columns:
        y = 0
        col = i
        val = request.json[i]
        print "TEST:" 
        print "col type", type(col)
        print val, type(val)
        c.execute('CREATE TABLE IF NOT EXISTS ' + col + '(id INT PRIMARY KEY, info TEXT)')
#       ''' NEED TO ITERATE THROUGH LIST AND ADD TO SQLITE '''
        for x in val:
            test = str(x)
            work= re.sub("[\t](2,)",'',test)
            work = re.sub("[^a-zA-Z0-9 \n\.\:]",'',test)
            work = re.sub("TLV t*", "TLV: ", work)
#            work = re.sub(":", "\:", work)
            print work, type(work)
#            print col
            test = str(x)
            c.execute('INSERT INTO ' + col + ' VALUES (?,?)', (y,work))
            y += 1
        conn.commit()

    print columns, type(columns)

#    print vals, type(vals)
    return columns

if __name__ == "__main__":
    run(host='localhost', port=5000, debug=True)
