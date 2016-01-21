from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_map(node_active, node_dead, ips, dead_ips):
	n = node_active
	m = node_dead
	
	G = nx.star_graph(0)
	print G.graph
	for i in range(n):
		
		G.add_node(i+1, status="active")#
		G.add_edge(0, i+1)

	for i in range(m):
		a = len(G.node)
		G.add_node(a, status="dead")
		G.add_edge(0,a)

	live_list = []
	dead_list = []
	subnet_list = []
	
	for key, value in G.node.iteritems():
		if value and "active" in value['status']:
			live_list.append(key)
		elif value and "dead" in value['status']:
			dead_list.append(key)
		else:
			subnet_list.append(key)

	print "Number of active nodes = " + str(live_list)
	print "Number of dead nodes = " + str(dead_list)

	live_labels={}
	e = live_list[0]
	for i in ips:
		print ips[i]
		live_labels[e] = ips[i]
		e += 1
	dead_labels={}
	e=dead_list[0]
	for i in dead_ips:
		print dead_ips[i]
		dead_labels[e] = dead_ips[i]
		e += 1
	node_and_degree = G.degree()
	(largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]

	hub_ego=nx.ego_graph(G,largest_hub)
	pos = nx.spring_layout(hub_ego)
	
	posi = None

	posi = nx.spring_layout(G) if posi is None else posi
	nx.draw(G, posi, nodelist=subnet_list, font_size=16, node_color="black",with_labels=False)
	nx.draw(G, posi, nodelist=live_list, font_size=16, node_color="green",with_labels=False)
	nx.draw(G, posi, nodelist=dead_list, font_size=16, node_color="red",with_labels=False)

	nx.draw_networkx_labels(G, posi, live_labels,font_size=16)
	nx.draw_networkx_labels(G, posi, dead_labels, font_size=16)

	plt.savefig('test.png')
	plt.show()