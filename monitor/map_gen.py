from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def setup_list(G_info, l_ip, d_ip):
	live_list = [];	dead_list = []
	ips = l_ip; dead_ips = d_ip
	live_labels={}; dead_labels={}
	subnet_list = []
	for key, value in G_info.node.iteritems():
		if value and "active" in value['status']:
			live_list.append(key)
		elif value and "dead" in value['status']:
			dead_list.append(key)
		else:
			subnet_list.append(key)

	ll = live_list[0]
	for i in ips:
		print ips[i]
		live_labels[ll] = []
		live_labels[ll].append(ips[i])
		live_labels[ll].append("active")
		ll += 1

	dl=dead_list[0]
	for i in dead_ips:
		print dead_ips[i]
		dead_labels[dl] = []
		dead_labels[dl].append(dead_ips[i])
		dead_labels[dl].append("dead") 
		dl += 1
		## merge live_labels and dead_labels in corrected
		## order and format
	complete_list = live_labels.copy()
	complete_list.update(dead_labels)
	final_list = sorted(complete_list.items(),key=itemgetter(1))
	
	complete_dict = {}
	i = 1
	for key, val in final_list:
		print str(key)
		complete_dict[i] = val
		print str(complete_dict)
		i += 1
	return (complete_dict, subnet_list)

def draw_map(G, posi, sorted_dict):
	complete_dict = sorted_dict
	live_labels = {}
	dead_labels = {}
	live_list = []
	dead_list = []

	posi = None
	posi = nx.circular_layout(G) if posi is None else posi
	nx.draw_circular(G, nodelist=subnet_list, font_size=16, node_color="black",with_labels=False)

	for p in posi:
		posi[p][1] += 0.05
	
	for key,values in complete_dict.iteritems():
		if values[1] == "active":
			##run active node creation
			live_list.append(key)
			print "list: " + str(live_list)
			live_labels[key] = values[0]
			print "test " + str(live_labels)
			nx.draw_circular(G, nodelist=live_list, font_size=16, node_color="green", with_labels=False)
			nx.draw_networkx_labels(G, posi, live_labels,font_size=16)
		elif values[1] == "dead":
			##run dead node creation
			dead_list.append(key)
			print "dead list " + str(dead_list)
			dead_labels[key] = values[0]
			print "dead test " + str(dead_labels)
			nx.draw_circular(G, nodelist=dead_list, font_size=16, node_color="red", with_labels=False)
			nx.draw_networkx_labels(G, posi, dead_labels, font_size=16)


def gen_lense(node_active, node_dead, ips, dead_ips):
	n = node_active
	m = node_dead
	plt.clf()
	G = nx.star_graph(0)

	for i in range(n):		
		G.add_node(i+1, status="active")
		G.add_edge(0, i+1)
	for i in range(m):
		a = len(G.node)
		G.add_node(a, status="dead")
		G.add_edge(0,a)

	node_and_degree = G.degree()
	(largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
	hub_ego=nx.ego_graph(G,largest_hub)
	pos = nx.circular_layout(hub_ego)

	complete_dict, subnet_list = setup_list(G, ips, dead_ips)

	print "Final and complete node dictionary: " + str(complete_dict)
    draw_map(G, posi, complete_dict)
	plt.savefig('/var/www/FlaskApp/FlaskApp/static/img/map.png')
