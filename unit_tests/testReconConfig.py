import unittest
import spawn

class TestConfig(unittest.TestCase):
	def testConfig(self):
		host, user, pwd, db = spawn.configRecon()
		self.assertEqual(host, "localhost")
		self.assertEqual(user, "root")
		self.assertEqual(pwd, "password")
		self.assertEqual(db, "discover")

if __name__ == '__main__':
	unittest.main()