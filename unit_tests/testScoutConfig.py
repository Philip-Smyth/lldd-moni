import unittest
import spawn

class TestConfig(unittest.TestCase):
	def testConfig(self):
		start, end = spawn.configScout()
		self.assertEqual(start, "11")
		self.assertEqual(end, "14")

if __name__ == '__main__':
	unittest.main()