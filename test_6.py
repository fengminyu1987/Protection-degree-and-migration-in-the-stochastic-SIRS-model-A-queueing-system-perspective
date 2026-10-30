import networkx as nx
import math
import random
from random import choice

from matplotlib.backends.backend_pdf import PdfPages

m=4
n=1000
i0=1
time_total=4000

step=1
lambdas=[3,1.5,6]
lambda_now=[3]
alpha_now=[0.8]
alphas=[.8,.4,1.6]
betas=[.001,.0005,.002]
beta_now=[.001]
gamma_now=[.7]
gammas=[.7,.35,1.4]
retention_now=[.995]
retentions=[.995,.990,.997]
kinds=["S","I","R"]
status=[0]
init_ks=[4,8,16]


#use WS network
graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)

node_kind={}
node_out= {}

continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

I_degree={}
total_degree={}
k_i={}

# exponential distribution
def exp_distri(lamb):
	return math.log(1 - random.random()) * (-1 / lamb)

# the rate of neighbor of special kind
def get_rate(target,kind):
	neighbors=graph.neighbors(target)
	total_n=len(neighbors)
	kind_n=0
	for i in neighbors:
		if node_kind[i]==kind:
			kind_n+=1
	return 1.0*kind_n/total_n

# the rate of special kind
def get_total_rate(kind):
	total_n=len(graph.nodes)
	kind_n=0
	for i in graph.nodes:
		if node_kind[i]==kind:
			kind_n+=1
	return 1.0*kind_n/total_n

# the stay time of node
def get_time_interval(node):
	if node_kind[node]==kinds[0]:
		i_total = get_total_rate(kinds[1])
		k = len(graph.edges)*2.0/len(graph.nodes())
		if beta_now[0] * k * i_total * len(graph.nodes)>0:
			temp = exp_distri(beta_now[0] * k * i_total * len(graph.nodes))
		else:temp =1000
		if temp<node_out[node] or node_out[node]==0:
			node_out[node]=temp
	if node_kind[node]==kinds[1]:
		temp = exp_distri(gamma_now[0])
		if temp<node_out[node] or node_out[node]==0:
			node_out[node]=temp
	if node_kind[node]==kinds[2]:
		temp = exp_distri(alpha_now[0])
		if temp<node_out[node] or node_out[node]==0:
			node_out[node]=temp

# create a new node and add it to the graph
def new_node():
	node_new=0
	while graph.has_node(node_new):
		node_new+=1
	k=0
	while k<m:
		dead = choice(list(graph.nodes()))
		k+=1
		if dead!=node_new:
			graph.add_edge(dead,node_new)
		# 如果连接重复,重roll
		if graph.degree(node_new) < k + 1:
			k = k - 1
	node_kind[node_new]=kinds[0]
	node_out[node_new]=10000
	get_time_interval(node_new)

# initialize the graph
def initialize():
	node_kind.clear()
	node_out.clear()

	for i in graph.nodes:
		node_kind[i]=kinds[0]
	#initial i
	for i in range(i0):
		i_first = random.choice(list(graph.nodes()))
		node_kind[i_first]=kinds[1]
	s_total=get_total_rate(kinds[0])
	i_total = get_total_rate(kinds[1])
	#initial time
	for i in graph.nodes:
		if node_kind[i]==kinds[0]:
			k=graph.degree(i)
			node_out[i]=exp_distri(beta_now[0]*k*i_total*len(graph.nodes))
		elif node_kind[i]==kinds[1]:
			node_out[i] = exp_distri(gamma_now[0])

# simulation
def simulation(t,graph):
	time_left=t
	count_in = 0
	count_out = 0

	last_time=time_total/4
	# CREATE NEW NODE
	next_node = exp_distri(lambda_now[0])

	while time_left > 0:
		# TIME PASS
		min_node = 10000
		min_time = 1000
		for i in node_out.keys():
			if node_out[i] < min_time:
				min_node = i
				min_time = node_out[i]
		is_new_node = False
		if next_node < min_time:
			is_new_node = True

		for i in node_out.keys():
			if is_new_node:
				node_out[i] -= next_node
			elif i == min_node:
				node_out[i] = 0
			else:
				node_out[i] -= min_time

		if not is_new_node:
			time2 = time_left - min_time
			next_node -= min_time
		else:
			time2 = time_left - next_node
			next_node = exp_distri(lambda_now[0])

		decrete_time = int(time_left)

		while decrete_time > time2:
			decrete_time -= step
		time_left = time2

		if not is_new_node:
			if node_kind[min_node] == kinds[0]:
				node_kind[min_node] = kinds[1]
				get_time_interval(min_node)
			elif node_kind[min_node] == kinds[1]:
				node_kind[min_node] = kinds[2]
				get_time_interval(min_node)
			elif node_kind[min_node] == kinds[2]:
				if random.random() < retention_now[0]:
					node_kind[min_node] = kinds[0]
					get_time_interval(min_node)
				else:
					graph.remove_node(min_node)
					node_out.pop(min_node)
					node_kind.pop(min_node)
					count_out += 1

		if is_new_node:
			new_node()
			count_in += 1

		if time_left<last_time:
			for temp in range(len(kinds)):
				Is = sum([1 for i in node_kind.keys() if node_kind[i] == kinds[temp]])
				if Is in continous_time[kinds[temp]].keys():
					continous_time[kinds[temp]][Is]+=last_time-time_left
				else:continous_time[kinds[temp]][Is]=last_time-time_left
			last_time=time_left
		#when_stable(time_left)

	print("in", count_in)
	print("out", count_out)

print("BEGINS")

initialize()

print("node_degree ",graph.degree)
print("node_out ",node_out)
print("node_kind ",node_kind)


sir_pi=[{} for i in range(20)]


import json
def save_time(ct,num):
	file1 = open("sir_result/%d.json" % num, mode='w')
	data = json.dumps(ct)
	print(data,file=file1)
	file1.close()


status[0]=0
graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
initialize()
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][0] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][0][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
initialize()
status[0]=1
alpha_now[0]=alphas[1]
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][1] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][1][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
initialize()
status[0]=2
alpha_now[0]=alphas[2]
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][2] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][2][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
initialize()
status[0]=3
alpha_now[0]=alphas[0]
gamma_now[0]=gammas[1]
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][3] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][3][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
initialize()
status[0]=4
gamma_now[0]=gammas[2]
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][4] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][4][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
lambda_now[0]=lambdas[1]
initialize()
status[0]=5
gamma_now[0]=gammas[0]
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][5] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][5][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
lambda_now[0]=lambdas[2]
initialize()
status[0]=6
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][6] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][6][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
lambda_now[0]=lambdas[0]
retention_now[0]=retentions[1]
initialize()
status[0]=7
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][7] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][7][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)
retention_now[0]=retentions[2]
initialize()
status[0]=8
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][8] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][8][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,init_ks[1],.7)
retention_now[0]=retentions[0]
initialize()
status[0]=9
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][9] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][9][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,init_ks[2],.7)
initialize()
status[0]=10
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][10] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][10][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,init_ks[0],.7)
beta_now[0]=betas[1]
initialize()
status[0]=11
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][11] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][11][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

graph=nx.generators.random_graphs.watts_strogatz_graph(n,init_ks[0],.7)
beta_now[0]=betas[2]
initialize()
status[0]=12
simulation(time_total,graph)
for k in range(len(kinds)):
	sir_pi[k][12] = [0 for i in range(1 + max(continous_time[kinds[k]].keys()))]
	for i in continous_time[kinds[k]].keys():
		sir_pi[k][12][i]=continous_time[kinds[k]][i]
save_time(continous_time, status[0])
continous_time={kinds[0]:{},kinds[1]:{},kinds[2]:{}}

print(len(graph.nodes))
print("node_degree ",graph.degree)
print("node_out ",node_out)
print("node_kind ",node_kind)


import matplotlib.pyplot as plt
import numpy as np

for k in range(len(kinds)):
	for i in sir_pi[k].keys():
		total_is=sum(sir_pi[k][i])
		sir_pi[k][i]=[j * 1.0 / total_is for j in sir_pi[k][i]]


font = {'family': 'serif',
        'weight': 'normal',
        'size': 18,
        }


variables=[r"$\alpha$=%.3f",r"$\gamma$=%.3f",r"$\lambda$=%.3f",r"p=%.3f",r"k=%d",r"$\beta$=%.4f"]
asdad=[alphas,gammas,lambdas,retentions,init_ks,betas]
for k in range(len(kinds)):
	for j in range(len(variables)):
		fig = plt.figure()
		plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9)
		plt.scatter(range(len(sir_pi[k][0])), sir_pi[k][0], color="green", label=variables[j] % asdad[j][0])
		plt.scatter(range(len(sir_pi[k][1+j*2])), sir_pi[k][1+j*2], color="blue", marker="^", label=variables[j] % asdad[j][1])
		plt.scatter(range(len(sir_pi[k][2+j*2])), sir_pi[k][2+j*2], color="red", marker="+", label=variables[j] % asdad[j][2])
		plt.xlabel("%s"%kinds[k],fontdict=font)
		plt.ylabel("P(%s)"%kinds[k],fontdict=font)
		plt.legend(frameon=False)
		with PdfPages('sir_result/%d.pdf'%(j*3+k)) as pdf:
		     # As many times as you like, create a figure fig and save it:
		     pdf.savefig(fig)
#
# fig = plt.figure()
# plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9)
# plt.scatter(range(len(sir_pi[0])), sir_pi[0], color="green", label=r"$\gamma$=%.2f" % gammas[0])
# plt.scatter(range(len(sir_pi[3])), sir_pi[3], color="blue", marker="^", label=r"$\gamma$=%.2f" % gammas[1])
# plt.scatter(range(len(sir_pi[4])), sir_pi[4], color="red", marker="+", label=r"$\gamma$=%.2f" % gammas[2])
# plt.xlabel("R",fontdict=font)
# plt.ylabel("P(R)",fontdict=font)
# plt.legend(frameon=False)
# with PdfPages('8.pdf') as pdf:
#      # As many times as you like, create a figure fig and save it:
#      pdf.savefig(fig)
#
#
# fig = plt.figure()
# plt.subplots_adjust(left=0.2, bottom=0.2, right=0.9)
# plt.scatter(range(len(sir_pi[5])), sir_pi[5], color="green", label=r"$\lambda$=%.2f" % lambdas[0])
# plt.scatter(range(len(sir_pi[6])), sir_pi[6], color="blue", marker="^", label=r"$\lambda$=%.2f" % lambdas[1])
# plt.scatter(range(len(sir_pi[7])), sir_pi[7], color="red", marker="+", label=r"$\lambda$=%.2f" % lambdas[2])
# plt.xlabel("R",fontdict=font)
# plt.ylabel("P(R)",fontdict=font)
# plt.legend(frameon=False)
# with PdfPages('9.pdf') as pdf:
#      # As many times as you like, create a figure fig and save it:
#      pdf.savefig(fig)