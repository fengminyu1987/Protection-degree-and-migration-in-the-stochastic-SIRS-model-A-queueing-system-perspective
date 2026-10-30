import matplotlib.pyplot as plt
import json
#---------------------------------
state='R'
f = open('(1).json', 'r')
content = f.read()
dist= json.loads(content)
S=dist[state]


NS1=list(S.keys())
ds1=list(S.values())

s=0
for i in NS1:
   s=s+S[i]
for i in range(0, len(ds1)):
    ds1[i]=ds1[i]/s

for i in range(0, len(NS1)):
    NS1[i]=int(NS1[i])



#---------------------------------
u= open('(12).json', 'r')
content = u.read()
dist2= json.loads(content)
S=dist2[state]


NS2=list(S.keys())
ds2=list(S.values())

s=0
for i in NS2:
   s=s+S[i]
for i in range(0, len(ds2)):
    ds2[i]=ds2[i]/s

for i in range(0, len(NS2)):
    NS2[i]=int(NS2[i])

#---------------------------------
n = open('(13).json', 'r')
content = n.read()
dist3= json.loads(content)
S=dist3[state]


NS3=list(S.keys())
ds3=list(S.values())

s=0
for i in NS3:
   s=s+S[i]
for i in range(0, len(ds3)):
    ds3[i]=ds3[i]/s

for i in range(0, len(NS3)):
    NS3[i]=int(NS3[i])



plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签


plt.gcf().subplots_adjust(left=0.16, bottom=0.15)
plt.scatter(NS2,ds2,marker="s",color="white",edgecolors="r",label=r'$\beta$'+' = 0.0005')
plt.scatter(NS1,ds1,color="white",edgecolors="b",label=r'$\beta$'+' = 0.0010')
plt.scatter(NS3,ds3,marker="^",color="white",edgecolors="g",label=r'$\beta$'+' = 0.0020')
plt.legend(frameon=False,loc='upper right',borderaxespad=0, prop={'family' : 'SimSun', 'size': 19}, handletextpad=0.0001)
plt.xlabel(state,font={'family':'SimSun', 'size':20})
plt.ylabel("P("+state+")",font={'family':'SimSun', 'size':20})
plt.xticks(font={'family':'SimSun', 'size':15})
plt.yticks(font={'family':'SimSun', 'size':15})
plt.show()