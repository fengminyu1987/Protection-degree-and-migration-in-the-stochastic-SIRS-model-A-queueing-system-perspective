import networkx as nx
import math
import random
from random import choice
import time


m=4
n=1000
i0=1
time_left=3000
step=30
lamb=3
alpha=.8
beta=.001
gamma=1.4
retention=.995
kinds=["S","I","R"]

count_in=0
count_out=0

#use WS network
graph=nx.generators.random_graphs.watts_strogatz_graph(n,m,.7)

time_seq=[]
node_kind={}

node_out= {}

I_degree={}
total_degree={}
k_i={}

#record time sequnce
def record_time():
    total_node=len(graph.nodes)
    time_seq.append((get_total_rate(kinds[0])*total_node,get_total_rate(kinds[1])*total_node,get_total_rate(kinds[2])*total_node))

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
        if beta * k * i_total * len(graph.nodes)>0:
            temp = exp_distri(beta * k * i_total * len(graph.nodes))
        else:temp =1000
        if temp<node_out[node] or node_out[node]==0:
            node_out[node]=temp
    if node_kind[node]==kinds[1]:
        temp = exp_distri(gamma)
        if temp<node_out[node] or node_out[node]==0:
            node_out[node]=temp
    if node_kind[node]==kinds[2]:
        temp = exp_distri(alpha)
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
            node_out[i]=exp_distri(beta*k*i_total*len(graph.nodes))
        elif node_kind[i]==kinds[1]:
            node_out[i] = exp_distri(gamma)

print("BEGINS")

initialize()

print("node_degree ",graph.degree)
print("node_out ",node_out)
print("node_kind ",node_kind)

# CREATE NEW NODE
next_node=exp_distri(lamb)

print(time.asctime())
print("BEGIN")


decrete_time=int(time_left)
degree_dis=[]
avg_degree=[]
while time_left>0:
    if time_left<=1000:
        degree=nx.degree(graph)
        degree_dis.append(dict(degree))
        avg_degree.append(sum(dict(degree).values())/len(graph.nodes))
    # TIME PASS
    min_node=10000
    min_time=1000
    for i in node_out.keys():
        if node_out[i]<min_time:
            min_node=i
            min_time=node_out[i]
    is_new_node=False
    if next_node<min_time:
        is_new_node=True

    for i in node_out.keys():
        if is_new_node:
            node_out[i] -=next_node
        elif i==min_node :
            node_out[i]=0
        else:
            node_out[i]-=min_time

    if not is_new_node:
        time2=time_left-min_time
        next_node-=min_time
    else:
        time2=time_left-next_node
        next_node=exp_distri(lamb)

    if time_left<decrete_time:
        decrete_time=int(time_left)
    while decrete_time>time2:
        record_time()
        decrete_time-=step
        print("\r%d "%decrete_time,end=time.asctime())
    time_left=time2

    if not is_new_node:
        if node_kind[min_node]==kinds[0]:
            node_kind[min_node]=kinds[1]
            get_time_interval(min_node)
        elif node_kind[min_node]==kinds[1]:
            node_kind[min_node]=kinds[2]
            get_time_interval(min_node)
        elif node_kind[min_node]==kinds[2]:
            if random.random()<retention:
                node_kind[min_node]=kinds[0]
                get_time_interval(min_node)
            else:
                graph.remove_node(min_node)
                node_out.pop(min_node)
                node_kind.pop(min_node)
                count_out+=1

    if is_new_node:
        new_node()
        count_in+=1

    #when_stable()

name="lambda=0.75"
import json
file=open("%s.json"%name,mode="w")
file.write(json.dumps(time_seq))
file.close()