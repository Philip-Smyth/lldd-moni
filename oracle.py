from scapy.all import *
import netaddr
from netaddr import iter_iprange
import socket
import netifaces as net
import argparse
import lense
import nmap_recon as recon

parser = argparse.ArgumentParser()
parser.add_argument("range_begin")
parser.add_argument("range_end")

args = parser.parse_args()
start_range = args.range_begin
end_range = args.range_end

#get ip of this device
net.ifaddresses('eth0')
host_ip = net.ifaddresses('eth0')[2][0]['addr']

# use device address to determine subnet
s_net,scrap = host_ip.rsplit(".", 1)
for i in range(5):
	# use subnet of device and defined range to create address list for iteration
	addresses = list(iter_iprange(str(s_net) +"."+ str(start_range), str(s_net) +"."+ str(end_range)))
	#set counter for active devices
	liveCounter = 0
	deadCounter = 0
	i=1
	active_addr = {}
	dead_addr = {}
	for host in addresses:
		#if(host == addresses.network or host == addresses.broadcast):
		#	continue
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
	#print "From " + str(len(addresses)) + " possible addresses, " + str(liveCounter) + " are active."
	#	print active_addr[key]
	print active_addr
	recon.recon_address(active_addr)
	#print deadCounter
	#print liveCounter
	lense.gen_lense(liveCounter, deadCounter, active_addr, dead_addr)