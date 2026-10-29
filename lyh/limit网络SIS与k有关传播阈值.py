import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import scipy.io as sio
#ws = nx.watts_strogatz_graph(500, 5, 0.5)

'''
A=numpy.zeros((N,N),dtype=int)

#随机连边  1表示有边
for i in range(
    for j in range((i+1),m0)
        A[i,j]= round(rand())
        A[j,i] =  A[i,j]
#初始完成
n=m0#节点个数

for new in range(m0+1,N)
    oldlist=[]
    degree_a=[]
    degree_b=[]
    print(new)
    
    #old vertice 速度越大连接上的概率越大
    Degree = sum(A(1:new-1,1:new-1))  %每个顶点的总度数
    Pi=Degree.*(K-Degree)
    %----------找正pi最小值-------------------
    alist=find(Degree(1:new-1)<K)%非饱和节点序列
    for i=1:length(alist)
        degree_a(i)=Degree(alist(i))
    end
    Pi_a=degree_a.*(K-degree_a)
    min_pi=min(Pi_a)
    %-----------------------------------------
    position=find(Pi<=0);%用正最小值替换负数节点的pi值
    position
    for i=1:length(position)
        Pi(position(i))=min_pi;  %一开始写的Degree 好像写错了
    end
    %----------------------------------
    
    blist=find(Degree(1:new-1)>=K);%饱和节点序列
    for i=1:length(blist)
        degree_b(i)=Degree(blist(i));
    end
    
    Pi_b=-(degree_b+1).*(K-degree_b-1)
    %n_a=length(alist);
    n_b=length(blist);
    %制造出一个pi的分布区间，模拟概率
    PiInterval(1) = Pi(1);
    for i=2:new-1
        PiInterval(i) = Pi(i)+PiInterval(i-1);
    end
    %连接 新节点 与 m个old节点
    Allpi = sum(Pi); %整个图的总pi
    
    %b同理
    if isempty(Pi_b)==0
        PiInterval_b(1) = Pi_b(1);
        if length(blist)>1
            for i=2:length(blist)
                PiInterval_b(i) = Pi_b(i)+PiInterval_b(i-1);
            end
        end
        Allpi_b = sum(Pi_b);
    end
    %全部节点增
    for i = 1:m1 
       while 1
 %以概率从old节点中找到合适的顶点连接
         Randpi  = fix(Allpi*rand()+1); %要与度区间包含RandDegree的顶点相连
         %找到 符合 要求的区间所属顶点
         Ans = find(Randpi <= PiInterval(1:new-1));
         old = Ans(1);
         if A(new,old) == 0
            oldlist(i)=old;
            A(new,old) = 1;
            A(old,new) = 1;
            break;
         end
       end
    end
'''

#邻接矩阵
#a = nx.to_numpy_matrix(ws)
file = 'K40N1000.mat'
data = sio.loadmat(file)

A= data['A']
a=A.todense()
print(a)
kmedian=min(np.sum(a,axis=1))
print("k_median")
print(kmedian)
k_list=np.sum(a,axis=1)
print("k_list")
print(k_list)
#感染率
#betas = [0.01,0.042,0.044,0.046,0.048,0.05,0.052,0.054,0.056,0.058,0.06,0.07,0.076,0.078,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20,0.21,0.22,0.23,0.24,0.25]
betass=[0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24]
#复原率
gama = 0.3

#出生率死亡率
#lamda
#miu
#初始患者
origin = random.sample(range(0, a.shape[0]), 3)

def sir_(a, origin, beta, gama):
    #总人数
    n = a.shape[0]
    #控制符
    #judge = 1
    #未感染人群
    s = np.arange(n)
    s = np.delete(s, origin)
    # 未感染人数记录
    snum = list()
    snum.append(len(s))
    #感染人群
    i = origin
    #感染人数记录
    inum = list()
    inum.append(len(i))
    #复原人群
    #r = []
    #复原人数记录
    #rnum = list()
    #rnum.append(0)
    #计时器
    h = 1
    #开始传播
    while h < 3000:
        print(i)
        #新一轮感染者
        temp_i = []
        m = len(i)
        #q = len(r)
        #感染
        asd = []
        for j in range(0, m):
            #感染者
            node = int(i[j])
            for k in range(0, len(s)):
                if a[node, int(s[k])] == 1:
                    asd.append(int(s[k]))

        asd2=np.unique(asd)
        #print(asd2)
            #未被感染者且不为复原者
            #asd2 = np.intersect1d(asd2, s)
            #asd2 = np.setdiff1d(asd2, r)
        asd_final = []
        if len(asd2)!=0:
            for j in range(0,len(asd2)):
                order=asd2[j]
                beta_j=k_list[order]/kmedian*beta
                for k in range(0,m):
                    if a[int(asd2[j]),int(i[k])]==1:
                        num = np.random.rand() - beta_j
                        if num<=0:
                            asd_final.append(int(asd2[j]))
                            break
        #print("asdf")
        #print(asd_final)
       # num = np.random.rand(len(asd2)) - beta
            #新感染者
            #asd_final = []
       
            #for k in range(0, len(asd2)):
             #   if num[k] <= 0:
                    #asd_final.append(asd2[k])
        temp_i = np.union1d(temp_i, asd_final)
        #print("tempi")
        #print(temp_i)
        s = np.setdiff1d(s, asd_final)
        
        """   
        #免疫
        temp_r=[]
        num = np.random.rand(m) - gama
        asd = []
        asd_final = []
        for k in range(0, m):
            if num[k] <= 0:
                asd.append(k)
                asd_final.append(i[k])
        #原感染者部分免疫
        temp_r = np.union1d(temp_r, asd_final)
        i = np.delete(i, asd)
        """
        
        #免疫者又变为易感者过程
        num = np.random.rand(m) - gama
        asd = []
        asd_final = []
        for k in range(0, m):
            if num[k] <= 0:
                asd.append(k)
                asd_final.append(i[k])

        s = np.union1d(s, asd_final)
        #r = np.delete(r, asd)
        i = np.setdiff1d(i, asd_final)
        
        #这一轮后总感染者
        i = np.union1d(i, temp_i)
        #r = np.union1d(r, temp_r)
        snum.append(len(s))
        inum.append(len(i))
        #rnum.append(len(r))
        h = h + 1

    h_s=2800
    '''
    inum_uni_set=set(inum)
    inum_uni_ls=list(inum_uni_set)
    inum_uni_ls.sort()
    i_dis=[0 for i in range(0,len(inum_uni_ls))]
    for i in range(h_s,h):
        for j in range(0,len(inum_uni_ls)):
            if inum[i]==inum_uni_ls[j]:
                i_dis[j]+=1
    for i in range(0,len(inum_uni_ls)):
        i_dis[i]/=(h-h_s)
    '''
    plt.plot(inum,"-bo")
    
    i_sta_list=inum[h_s:]
    i_ave_f=sum(i_sta_list)/len(i_sta_list)/1000
    return i_ave_f
    
    
    #plt.plot(inum_uni_ls,i_dis)    
    #plt.plot(snum, "-bo", label='Susceptibles')
    #plt.plot(inum, "-ro", label='Infectious')
    ##plt.plot(rnum, "-go", label='Recovereds')
    #plt.title('SIR')
    #plt.legend()
    #plt.show()


def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()   

fs=[]
#for q in range(0,len(betas)):
f=sir_(a, origin, betass[15], gama)
fs.append(f)
#保存
text_save(fs,str(betass[15])+'_median.txt')
#plt.plot(betas[20],fs,"-v",markerfacecolor='none')
plt.xlabel(chr(946).lower())
plt.ylabel("P(i)")
plt.show()



