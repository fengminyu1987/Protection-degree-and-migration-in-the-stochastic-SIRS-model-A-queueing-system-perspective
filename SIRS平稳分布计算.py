import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
def SIRS():
    ws = nx.watts_strogatz_graph(100, 5, 0.5)

    #邻接矩阵
    a = nx.to_numpy_matrix(ws)
    #感染率
    beta = 0.8
    #复原率
    gama = 0.2
    rec = 0.1
    #初始患者
    node_state=np.zeros((100,6100))
    n = a.shape[0]
    origin = random.sample(range(0, a.shape[0]), 1)
    h=0
    i = origin
    order=i[0]
    node_state[order][h]=1
    s = np.arange(n)
    s = np.delete(s, origin)
    r = []
    print(order)
    print("--------------------------------")
    h=1
    while h < 6100:
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
                asd3 = np.setdiff1d(asd2, r)
                num = np.random.rand(len(asd2)) - beta
                #新感染者
                asd_final = []
                for k in range(0, len(asd2)):
                        order=int(asd2[k])
                        if num[k] <= 0:
                            asd_final.append(asd2[k])
                            node_state[order][h]=1
                            #print(order)
                        else:
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
                    print(order)
                else:
                    node_state[order][h]=2
            s = np.union1d(s, asd_final)
            r = np.delete(r, asd)

            i = np.union1d(i, temp_i)
            r = np.union1d(r, temp_r)
            h=h+1
    for i in range(20):
            print("----------------------------------------")
     
    for i in range(0,10):
        print("节点",i,"------------")
        n_0=n_1=n_2=0
        for j in range(100,2100):
            if node_state[i][j]==0:
                n_0=n_0+1
            if node_state[i][j]==1:
                n_1=n_1+1
            if node_state[i][j]==2:
                n_2=n_2+1
        d0=n_0/(n_0+n_1+n_2)
        d1=n_1/(n_0+n_1+n_2)
        d2=n_2/(n_0+n_1+n_2)
        print("第一次",d0,d1,d2)

        n_0=n_1=n_2=0
        for j in range(2100,4100):
            if node_state[i][j]==0:
                n_0=n_0+1
            if node_state[i][j]==1:
                n_1=n_1+1
            if node_state[i][j]==2:
                n_2=n_2+1
        d0=n_0/(n_0+n_1+n_2)
        d1=n_1/(n_0+n_1+n_2)
        d2=n_2/(n_0+n_1+n_2)
        print("第二次",d0,d1,d2)

        n_0=n_1=n_2=0
        for j in range(4100,6100):
            if node_state[i][j]==0:
                n_0=n_0+1
            if node_state[i][j]==1:
                n_1=n_1+1
            if node_state[i][j]==2:
                n_2=n_2+1
        d0=n_0/(n_0+n_1+n_2)
        d1=n_1/(n_0+n_1+n_2)
        d2=n_2/(n_0+n_1+n_2)
        print("第三次",d0,d1,d2)
'''
    list_i=[]
    list_s=[]
    list_r=[]
    for i in range(0,n):
            list_i.append(d_matrix[i][1])
    for i in range(0,n):
            list_s.append(d_matrix[i][0])
    for i in range(0,n):
            list_r.append(d_matrix[i][2])
            '''

SIRS()

