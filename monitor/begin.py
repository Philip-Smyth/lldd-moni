import threading
import spawn
import scout
print "Working"

start_range, end_range = spawn.configScout()
print start_range
print end_range
scout.monitor_network(start_range, end_range)