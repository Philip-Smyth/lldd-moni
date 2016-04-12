import recon
import pytest
import unittest

class TestParse(unittest.TestCase):
	def testReconParsing(self):
		test=[('172.26.71.11', 
			{
			  'status': {'state': 'up', 'reason': 'localhost-response'}, 
			  'uptime': {'seconds': '1116', 'lastboot': 'Thu Mar 24 12:46:21 2016'}, 
			  'vendor': {}, 
			  'addresses': {'ipv4': '172.26.71.11'}, 
			  'hostname': '', 
			  'tcp': {80: {'product': '', 'state': 'open', 'version': '', 'name': 'http', 
			               'conf': '3', 'extrainfo': '', 'reason': 'syn-ack', 'cpe': ''}, 
			          22: {'product': '', 'state': 'open', 'version': '', 'name': 'ssh', 
			               'conf': '3', 'extrainfo': '', 'reason': 'syn-ack', 'cpe': ''}
			          }, 
			  'osclass': {'vendor': 'Linux', 'osfamily': 'Linux', 'type': 'general purpose', 
			               'osgen': '3.X', 'accuracy': '100'}
			})]

		for host, os in test:
			host_os, vr, type, acc, hostname, mac, ip=recon.gatherItems(host,os)
			host_os=str(host_os)
			os_vr = str(vr)
			os_type = str(type)
			os_acc = str(acc)
			hostname = str(hostname)
			mac = str(mac)
			ip = str(ip)
			self.assertEqual(host_os, "Linux")
			self.assertEqual(os_vr, "3.X")
			self.assertEqual(os_type, "general purpose")
			self.assertEqual(os_acc, "100")
			self.assertEqual(hostname, "")
			self.assertEqual(mac, "n/a(host)")
			self.assertEqual(ip, "172.26.71.11")

if __name__ == '__main__':
	unittest.main()