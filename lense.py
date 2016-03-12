from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def setup_list(G_info, l_ip, d_ip):
	live_list = [];	dead_list = []
	ips = l_ip; dead_ips = d_ip
	live_labels={}; dead_labels={}
	subnet_list = []
        ## If the node is active add to live_list
        ## if dead add to dead_list
        ## otherwise its the subnet so add to subnet list
	for key, value in G_info.node.iteritems():
		if value and "active" in value['status']:
			live_list.append(key)
		elif value and "dead" in value['status']:
			dead_list.append(key)
		else:
			subnet_list.append(key)
        ## for every active ip address
        ## add to active label dict
	e = live_list[0]
	for i in ips:
		print ips[i]
		live_labels[e] = []
		live_labels[e].append(ips[i])
		live_labels[e].append("active")
		e += 1
        ## for every dead ip address
        ## add to dead label dict
	e = dead_list[0]
	for i in dead_ips:
		print dead_ips[i]
		dead_labels[e] = []
		dead_labels[e].append(dead_ips[i])
		dead_labels[e].append("dead") 
		e += 1

	return (live_list, live_labels, dead_list, dead_labels, subnet_list)

def draw_map(G, posi, sorted_dict):
	complete_dict = sorted_dict
	live_labels = {}
	dead_labels = {}
	live_list = []
	dead_list = []

	for p in posi:
		posi[p][1] += 0.05
	
	for key,values in complete_dict.iteritems():
		if values[1] == "active":
			##run active node creation
			live_list.append(key)
			print "live list: " + str(live_list)
			live_labels[key] = values[0]
			print "live labels" + str(live_labels)
                        ## Draw the live nodes, making it green to show it as active
			nx.draw_circular(G, nodelist=live_list, font_size=16, node_color="green", with_labels=False)
                        ## Add the label to each node respectively
			nx.draw_networkx_labels(G, posi, live_labels,font_size=16)
		elif values[1] == "dead":
			##run dead node creation
			dead_list.append(key)
			print "dead list " + str(dead_list)
			dead_labels[key] = values[0]
			print "dead labels" + str(dead_labels)
                        ## Draw the dead nodes, making it red to show it as inactive
			nx.draw_circular(G, nodelist=dead_list, font_size=16, node_color="red", with_labels=False)
                        ## Add the label to each node respectively
			nx.draw_networkx_labels(G, posi, dead_labels, font_size=16)


def gen_lense(node_active, node_dead, ips, dead_ips):
	n = node_active
	m = node_dead
	plt.clf()
	G = nx.star_graph(0) ## empty graph, blank canvas

        ## add the active and inactive nodes to graph
	for i in range(n):		
		G.add_node(i+1, status="active")
		G.add_edge(0, i+1)
	for i in range(m):
		a = len(G.node)
		G.add_node(a, status="dead")
		G.add_edge(0,a)

	node_and_degree = G.degree()
        ## sort the nodes
	(largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]

	hub_ego=nx.ego_graph(G,largest_hub)
	pos = nx.circular_layout(hub_ego)
        ## Getting the data last that we need
        ## list = unneeded, live_list = unneeded, live_labels = list of active addresses for labels
        ## dead_labels = list of inactive addresses, subnet_list = subnet list 
	live_list, live_labels, dead_list, dead_labels, subnet_list = setup_list(G, ips, dead_ips)

	## Merge live_labels and dead_labels
        ## sort labels by their IP address order
	complete_dict = {}
	merged_list = live_labels.copy()
	merged_list.update(dead_labels)
	merged_list = sorted(merged_list.items(),key=itemgetter(1))
	i = 1
	for key, val in merged_list:
		print str(key)
		complete_dict[i] = val
		print str(complete_dict)
		i += 1
	print "Really completely sorted: " + str(complete_dict)

        ## Set the positions to follow the the spoke diagram desired
	posi = None
	posi = nx.circular_layout(G) if posi is None else posi
        ## Finally draw the graph and save it in file location
	nx.draw_circular(G, nodelist=subnet_list, font_size=16, node_color="black",with_labels=False)
        draw_map(G, posi, complete_dict)
	plt.savefig('/var/www/FlaskApp/FlaskApp/static/img/map.png')
