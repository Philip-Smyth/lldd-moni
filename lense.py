from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt

def draw_map(node_num, ips):
	n = node_num
	G = nx.generators.star_graph(n)
	labels=ips
	node_and_degree = G.degree()
	(largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]

	hub_ego=nx.ego_graph(G,largest_hub)

	pos = nx.spring_layout(hub_ego)
	
	
	posi = None
	posi = nx.spring_layout(G) if posi is None else posi
	nx.draw(G, posi, font_size=16, with_labels=False)
	#for p in posi:
	#	print p
	#	posi['test' + str(p)] = posi[p]
	#	posi['test' + str(p)] = posi[p]
	#	del posi[p]
	
	#labels[0]='test0'
	#labels[1]='test1'
	#labels[2]='test2'

	for p in posi:
		print posi[p]
		posi[p][1] += 0.05
	nx.draw_networkx_labels(G,posi,labels,font_size=16)
	plt.savefig('test.png')
	plt.show()