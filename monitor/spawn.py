import ConfigParser


def readConfig(header, value):
	config = ConfigParser.ConfigParser()
	config.read("discover.conf")
	conf_val = config.get(header, value)
	conf_val = conf_val.strip('"')
	return conf_val

def configScout():
	min_range = readConfig("network", "min_range")
	max_range = readConfig("network", "max_range")
	return min_range, max_range

def configRecon():
	host = readConfig("database", "host")
	user = readConfig("database", "user")
	pwd = readConfig("database", "password")
	db = readConfig("database", "db")
	return host,user,pwd,db	