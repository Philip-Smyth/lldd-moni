import requests
import os
import json,subprocess
import threading
def group(lst, n):
    return zip(*[lst[i::n] for i in range(n)])


def list_to_dict(li):  
    dct = {}
    for item in li:
        if dct.has_key(item):
            dct[item] = dct[item] + 1
        else:
            dct[item] = 1
    return dct 

def scan_host():
    threading.Timer(10, scan_host).start()
    ### Collect lldp info
    this=subprocess.check_output("sudo lldptool -t -i eth1", shell=True)
    lldp_array = []
    lldp_array = [this.splitlines()]
    this = group(lldp_array[0], 2)
    #print type(this)
    #print this

    os.environ['NO_PROXY'] = "127.0.0.1:5000"
    gt="http://127.0.0.1:5000/test"
    snd="http://127.0.0.1:5000/send"

    ### Posting host information
    payload_host = {"Grunt01": this}
    print type(payload_host)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    req = requests.post(snd, json.dumps(payload_host), headers=headers)
    data = req.text
    print "Sending data scanned from host..."
#    print data

scan_host()
### Posting hosts neighbour information
#payload_neighbour = {"NeighborA": {"Neighbour data": "random neighbour data"}}
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

#req = requests.post(snd, json.dumps(payload_neighbour), headers=headers)
#data = req.text
#print data
