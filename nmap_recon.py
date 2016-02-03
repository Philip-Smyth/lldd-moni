# Embedded file name: /home/lab2/lldp-moni/nmap_recon.py
import nmap
import MySQLdb as msql

def recon_address(active_addresses):
    con = msql.connect(host='localhost', user='root', passwd='password', db='discover')
    cur = con.cursor()
    check = "SHOW TABLES LIKE 'nodes'"
    cur.execute(check)
    result = cur.fetchone()
    if result:
        pass
    else:
        cur.execute('CREATE TABLE nodes (Id INTEGER NOT NULL AUTO_INCREMENT,Hostname VARCHAR(30), MAC_Addr VARCHAR(18),IP_Addr VARCHAR(15), OS VARCHAR(10),OS_Vrs VARCHAR(10), OS_Type VARCHAR(30),OS_Acc VARCHAR(3),PRIMARY KEY (Id))')
    for key, value in active_addresses.iteritems():
        print 'Value: ' + str(value)
        nm = nmap.PortScanner()
        this = nm.scan(value, '22-443', arguments='-n -O')
        os_list = [ (x, nm[x]) for x in nm.all_hosts() ]
        print nm.command_line()
        print nm[value].has_tcp(80)
        print nm.csv()
        print this
        for host, os in os_list:
            host_os = os['osclass']['osfamily']
            print 'OS: ' + str(host_os)
            os_vr = os['osclass']['osgen']
            print 'Version: ' + str(os_vr)
            os_type = os['osclass']['type']
            print 'Type: ' + str(os_type)
            os_acc = os['osclass']['accuracy']
            print 'Accuracy: ' + str(os_acc) + '%'
            hostname = os['hostname']
            print 'Hostname: ' + str(hostname)
            try:
                mac_addr = os['addresses']['mac']
                print 'MAC Address: ' + str(mac_addr)
            except KeyError as e:
                mac_addr = 'n/a(host)'
                print 'Error, localhost MAC not shown'
                pass

            ip_addr = os['addresses']['ipv4']
            print 'IP Address: ' + str(ip_addr)
            val = str(value)
            cur.execute('SELECT IP_Addr, COUNT(*) FROM nodes WHERE IP_Addr = %s', [val])
            if cur.fetchone()[0]:
                print "Updating"
                cur.execute("""UPDATE nodes SET Hostname=%s, MAC_Addr=%s, OS=%s, OS_Vrs=%s, 
                            OS_Type=%s, OS_Acc=%s WHERE IP_Addr=%s""", (hostname,mac_addr,host_os,os_vr,os_type,os_acc,ip_addr))
            else:
                print "Inserting"
                cur.execute("""INSERT INTO nodes (Hostname, MAC_Addr, IP_Addr, OS, OS_Vrs, OS_Type, OS_Acc) 
                            VALUES(%s,%s,%s,%s,%s,%s,%s)""", (hostname,mac_addr,ip_addr,host_os,os_vr,os_type,os_acc))
        con.commit()

this = {1: '172.26.71.11', 2: '172.26.71.12'}
#recon_address(this)