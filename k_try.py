import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
def SIRS(b,g,r,u):
    number=1000
    ws = nx.watts_strogatz_graph(number, 10, 0.5)
    print(nx.degree_histogram(ws))
    print(ws.degree())
    a = nx.to_numpy_array(ws)
    #感染率
    beta = b
    #复原率
    gama = g
    rec = r
    #初始患者
    terminal=1500
    node_state=np.zeros((number,terminal))
    n = a.shape[0]
    d_uni_ls=[]
    for i in range(n):
        d_unique=ws.degree(i)
        if d_unique not in d_uni_ls:
            d_uni_ls.append(d_unique)
    d_uni_ls.sort()
    print(d_uni_ls)
    dh=list(filter(lambda x: x!=0, nx.degree_histogram(ws)))
    print(dh)
    pI_list=[0]*len(d_uni_ls)
    print(pI_list)
    print(len(pI_list))
    origin = random.sample(range(0, a.shape[0]), 1)
    h=0
    i = origin
    order=i[0]
    node_state[order][h]=1
    s = np.arange(n)
    s = np.delete(s, origin)
    r = []
    h=1
    while h < terminal:
            #新一轮感染者
            temp_i = []
            m = len(i)
            q = len(r)
            #感染
            for j in range(0, m):
                #感染者
                node = int(i[j])
                asd = []
                for k in range(0, n):
                    if a[node, k] == 1:
                        asd.append(k)
                #未被感染者且不为复原者
                asd2 = np.intersect1d(asd, s)
                asd2 = np.setdiff1d(asd2, r)

                num = np.random.rand(len(asd2)) - beta

                #新感染者
                asd_final = []
                for k in range(0, len(asd2)):
                        order=int(asd2[k])
                        neighbour=0
                        for j in range(0,m):
                            if a[order,int(i[j])]==1:
                                neighbour+=1
                        f=math.exp(-np.random.poisson(u))
                        neighbour=int(round(neighbour*f))
                        print(neighbour)
                        for j in range(0,neighbour):
                            if np.random.rand() - beta <= 0:
                                asd_final.append(asd2[k])
                                node_state[order][h]=1
                                break
                            #print(order)
                        if node_state[order][h]!=1:
                            node_state[order][h]=0
                temp_i = np.union1d(temp_i, asd_final)
                s = np.setdiff1d(s, asd_final)
            #免疫
            temp_r=[]
            num = np.random.rand(m) - gama
            asd = []
            asd_final = []
            for k in range(0, m):
                    order=int(i[k])
                    if num[k] <= 0:
                            asd.append(k)
                            asd_final.append(i[k])
                            node_state[order][h]=2
                            #print(order)
                    else:
                        node_state[order][h]=1
            #原感染者部分免疫
            temp_r = np.union1d(temp_r, asd_final)
            i = np.delete(i, asd)

            
            #免疫者又变为易感者过程
            num = np.random.rand(q) - rec
            asd = []
            asd_final = []
            for k in range(0, q):
                order=int(r[k])
                if num[k] <= 0:
                    asd.append(k)
                    asd_final.append(r[k])
                    node_state[order][h]=0
                    #print(order)
                else:
                    node_state[order][h]=2
            s = np.union1d(s, asd_final)
            r = np.delete(r, asd)

            i = np.union1d(i, temp_i)
            r = np.union1d(r, temp_r)
            h=h+1
            
    d_matrix=np.zeros((n,3))         
    for i in range(0,n):
        n_0=n_1=n_2=0
        for j in range(500,h):
                if node_state[i][j]==0:
                        n_0=n_0+1
                if node_state[i][j]==1:
                        n_1=n_1+1
                if node_state[i][j]==2:
                        n_2=n_2+1
        d_matrix[i][0]=n_0/(n_0+n_1+n_2)
        d_matrix[i][1]=n_1/(n_0+n_1+n_2)
        d_matrix[i][2]=n_2/(n_0+n_1+n_2)

    #pS_list=[0 for i in range(0,10)]
    #pR_list=[0 for i in range(0,10)]
    pS_list=[0]*len(d_uni_ls)
    pR_list=[0]*len(d_uni_ls)
    for i in range(n):
        PI=d_matrix[i][1]
        PS=d_matrix[i][0]
        PR=d_matrix[i][2]
        k_i=ws.degree(i)
        for j in range(0,len(d_uni_ls)):
            if k_i==d_uni_ls[j]:
                pI_list[j]+=PI
                pS_list[j]+=PS
                pR_list[j]+=PR
    for i in range(0,len(pI_list)):
        pI_list[i]/=dh[i]
    print(pI_list)
    for i in range(0,len(pS_list)):
        pS_list[i]/=dh[i]
    for i in range(0,len(pR_list)):
        pR_list[i]/=dh[i]
    print("i shape:",len(pI_list))
    print("u_list shape:",len(d_uni_ls))
    return pI_list,pS_list,pR_list,d_uni_ls

def SIRS2(b,g,r):
    number=1000
    ws = nx.watts_strogatz_graph(number, 10, 0.5)
    print(nx.degree_histogram(ws))
    print(ws.degree())
    a = nx.to_numpy_array(ws)
    #感染率
    beta = b
    #复原率
    gama = g
    rec = r
    #初始患者
    terminal=1500
    node_state=np.zeros((number,terminal))
    n = a.shape[0]
    d_uni_ls=[]
    for i in range(n):
        d_unique=ws.degree(i)
        if d_unique not in d_uni_ls:
            d_uni_ls.append(d_unique)
    d_uni_ls.sort()
    print(d_uni_ls)
    dh=list(filter(lambda x: x!=0, nx.degree_histogram(ws)))
    print(dh)
    pI_list=[0]*len(d_uni_ls)
    print(pI_list)
    print(len(pI_list))
    origin = random.sample(range(0, a.shape[0]), 1)
    h=0
    i = origin
    order=i[0]
    node_state[order][h]=1
    s = np.arange(n)
    s = np.delete(s, origin)
    r = []
    h=1
    while h < terminal:
            #新一轮感染者
            temp_i = []
            m = len(i)
            q = len(r)
            #感染
            for j in range(0, m):
                #感染者
                node = int(i[j])
                asd = []
                for k in range(0, n):
                    if a[node, k] == 1:
                        asd.append(k)
                #未被感染者且不为复原者
                asd2 = np.intersect1d(asd, s)
                asd2 = np.setdiff1d(asd2, r)

                num = np.random.rand(len(asd2)) - beta

                #新感染者
                asd_final = []
                for k in range(0, len(asd2)):
                        order=int(asd2[k])
                        neighbour=0
                        for j in range(0,m):
                            if a[order,int(i[j])]==1:
                                neighbour+=1
                        
                        print(neighbour)
                        for j in range(0,neighbour):
                            if np.random.rand() - beta <= 0:
                                asd_final.append(asd2[k])
                                node_state[order][h]=1
                                break
                            #print(order)
                        if node_state[order][h]!=1:
                            node_state[order][h]=0
                temp_i = np.union1d(temp_i, asd_final)
                s = np.setdiff1d(s, asd_final)
            #免疫
            temp_r=[]
            num = np.random.rand(m) - gama
            asd = []
            asd_final = []
            for k in range(0, m):
                    order=int(i[k])
                    if num[k] <= 0:
                            asd.append(k)
                            asd_final.append(i[k])
                            node_state[order][h]=2
                            #print(order)
                    else:
                        node_state[order][h]=1
            #原感染者部分免疫
            temp_r = np.union1d(temp_r, asd_final)
            i = np.delete(i, asd)

            
            #免疫者又变为易感者过程
            num = np.random.rand(q) - rec
            asd = []
            asd_final = []
            for k in range(0, q):
                order=int(r[k])
                if num[k] <= 0:
                    asd.append(k)
                    asd_final.append(r[k])
                    node_state[order][h]=0
                    #print(order)
                else:
                    node_state[order][h]=2
            s = np.union1d(s, asd_final)
            r = np.delete(r, asd)

            i = np.union1d(i, temp_i)
            r = np.union1d(r, temp_r)
            h=h+1
            
    d_matrix=np.zeros((n,3))         
    for i in range(0,n):
        n_0=n_1=n_2=0
        for j in range(500,h):
                if node_state[i][j]==0:
                        n_0=n_0+1
                if node_state[i][j]==1:
                        n_1=n_1+1
                if node_state[i][j]==2:
                        n_2=n_2+1
        d_matrix[i][0]=n_0/(n_0+n_1+n_2)
        d_matrix[i][1]=n_1/(n_0+n_1+n_2)
        d_matrix[i][2]=n_2/(n_0+n_1+n_2)

    #pS_list=[0 for i in range(0,10)]
    #pR_list=[0 for i in range(0,10)]
    pS_list=[0]*len(d_uni_ls)
    pR_list=[0]*len(d_uni_ls)
    for i in range(n):
        PI=d_matrix[i][1]
        PS=d_matrix[i][0]
        PR=d_matrix[i][2]
        k_i=ws.degree(i)
        for j in range(0,len(d_uni_ls)):
            if k_i==d_uni_ls[j]:
                pI_list[j]+=PI
                pS_list[j]+=PS
                pR_list[j]+=PR
    for i in range(0,len(pI_list)):
        pI_list[i]/=dh[i]
    print(pI_list)
    for i in range(0,len(pS_list)):
        pS_list[i]/=dh[i]
    for i in range(0,len(pR_list)):
        pR_list[i]/=dh[i]
    print("i shape:",len(pI_list))
    print("u_list shape:",len(d_uni_ls))
    return pI_list,pS_list,pR_list,d_uni_ls

markers=['o','s','^']
parameters=[1,2]
colors=['b','g']
pI_list,pS_list,pR_list,d_uni_ls=SIRS2(0.9,0.3,0.1)
plt.plot(np.array(d_uni_ls),np.array(pI_list).reshape(-1,1),marker='^',color='r')
#plt.plot(np.array(d_uni_ls),np.array(pS_list).reshape(-1,1),marker='^',color='b')
#plt.plot(np.array(d_uni_ls),np.array(pR_list).reshape(-1,1),marker='^',color='g')
for i in range(0,2):
    pI_list,pS_list,pR_list,d_uni_ls=SIRS(0.9,0.3,0.1,parameters[i])
    plt.plot(np.array(d_uni_ls),np.array(pI_list).reshape(-1,1),marker=markers[i],color=colors[i])
    #plt.plot(np.array(d_uni_ls),np.array(pS_list).reshape(-1,1),marker=markers[i],color='b')
    #plt.plot(np.array(d_uni_ls),np.array(pR_list).reshape(-1,1),marker=markers[i],color='g')
plt.xlabel("k")
plt.ylabel("p")
#plt.legend([chr(955).lower()+"=0",chr(955).lower+'=1'])
#plt.legend(['Without protection degree',chr(956).lower()+"=0,"+chr(963).lower()+"=0.8",chr(956).lower()+"=0,"+chr(963).lower()+"=0.2",
 #           chr(955).lower()+"=4",chr(955).lower()+"=4",chr(956).lower()+"=4"])
plt.legend(['Without protection degree',chr(956).lower()+"=1",chr(956).lower()+"=2"],frameon=False)
plt.show()
