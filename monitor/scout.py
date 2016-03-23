from scapy.all import *
import netaddr
from netaddr import iter_iprange
import socket
import netifaces as net
import argparse
import map_gen
import recon
import threading

def monitor_network(min_range, max_range):
	#get ip of this device
	net.ifaddresses('eth0')
	host_ip = net.ifaddresses('eth0')[2][0]['addr']

	# use device address to determine subnet
	s_net,scrap = host_ip.rsplit(".", 1)
	##### Iterate the process 4 times
	# TODO need to make this iterative for deamon

	while True:
		# use subnet of device and defined range to create address list for iteration
		addresses = list(iter_iprange(str(s_net) +"."+ str(min_range), str(s_net) +"."+ str(max_range)))
		#set counter for active devices
		liveCounter = 0
		deadCounter = 0
		i=0
		active_addr = {}
		dead_addr = {}
		for host in addresses:
			resp = sr1(IP(dst=str(host))/ICMP(), timeout=2, verbose=0)
			if (str(host) == str(host_ip)):
				print str(host) + " is active(host)"
				active_addr[i]=str(host)
				liveCounter +=1
				i+=1
			elif(str(type(resp)) == "<type 'NoneType'>"):
				print str(host) + " is dead"
				deadCounter += 1
				dead_addr[i]=str(host)
				i+=1
			elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
				print str(host) + " is blocking ICMP"
			else:
				print str(host) + " is active"
				active_addr[i]=str(host)
				i+=1
				liveCounter += 1
		print active_addr
		rec = threading.Thread(target=recon.recon_address(active_addr))
		rec.start()
		gen = threading.Thread(target=map_gen.gen_lense(liveCounter, deadCounter, active_addr, dead_addr))
		gen.start()