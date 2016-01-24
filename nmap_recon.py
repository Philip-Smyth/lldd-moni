import nmap
import MySQLdb as msql

nm = nmap.PortScanner()
this = nm.scan("172.26.71.12", '22-443', arguments='-n -O')
os_list = [(x, nm[x]) for x in nm.all_hosts()]
print nm.command_line()
print nm["172.26.71.12"].has_tcp(80)
print nm.csv()
print this
for host, os in os_list:
	host_os = os['osclass']['osfamily']
	#print type(host_os)
	print "OS: " + str(host_os)	
	os_vr = os['osclass']['osgen']
	#print type(os_vr)
	print "Version: " + str(os_vr)	
	os_type = os['osclass']['type']
	#print type(os_type)
	print "Type: " + str(os_type)	
	os_acc = os['osclass']['accuracy']
	#print type(os_acc)
	print "Accuracy: " + str(os_acc) + "%"	

	hostname = os['hostname']
	print "Hostname: " + str(hostname)

	#print type(hostname)
	mac_addr = os['addresses']['mac']
	print "MAC Address: " + str(mac_addr)
	#print type(mac_addr)
	ip_addr = os['addresses']['ipv4']
	print "IP Address: " + str(ip_addr)
	#print type(ip_addr)

con = msql.connect(host="localhost", 
	               user="root", 
	               passwd="password", 
	               db="discover")
cur = con.cursor()
cur.execute('CREATE TABLE nodes Id INTEGER PRIMARY KEY, Hostname VARCHAR(30), MAC_Addr VARCHAR(18), IP_Addr VARCHAR(15), OS VARCHAR(10), OS_Vrs VARCHAR(10), OS_Type VARCHAR(30), OS_Acc VARCHAR(3)')
cur.execute("INSERT INTO nodes VALUES(1, %s,%s,%s,%s,%s,%s,%s)" % hostname, 
	                                  mac_addr,ip_addr,host_os, os_vr, os_type,
	                                  os_acc)
con.commit()