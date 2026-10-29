import numpy as np
import matplotlib.pyplot as plt
import json
f = open('D:\论文\CHAOS\SIRS代码\p-k_WITHOUT-yis.txt', 'r')
content = f.read()
y_without = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k_WITHOUT-xis.txt', 'r')
content = f.read()
x_without = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-xis_u=1.txt', 'r')
content = f.read()
x_1 = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-yis_u=1.txt', 'r')
content = f.read()
y_1 = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-xis_u=2.txt', 'r')
content = f.read()
x_2 = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-yis_u=2.txt', 'r')
content = f.read()
y_2 = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-xis_u=3.txt', 'r')
content = f.read()
x_3 = json.loads(content)
f.close()

f = open('D:\论文\CHAOS\SIRS代码\p-k-yis_u=3.txt', 'r')
content = f.read()
y_3 = json.loads(content)
f.close()

x_1=x_1[:10]
x_2=x_2[:10]
for i in range(0,len(x_2)):
    x_2[i]=x_2[i]-1
x_3=x_3[:10]
x_without=x_without[:10]
y_1=y_1[:10]
y_2=y_2[:10]
y_3=y_3[:10]
y_without=y_without[:10]
plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内`

plt.plot(np.array(x_without),np.array(y_without).reshape(-1,1),marker="o",color="black",
             markerfacecolor="w",markersize=7,markeredgecolor="black")
plt.plot(np.array(x_1),np.array(y_1).reshape(-1,1),marker="^",color="k",
             markerfacecolor="w",markersize=7,markeredgecolor="black")
plt.plot(np.array(x_2),np.array(y_2).reshape(-1,1),marker="s",color="k",
             markerfacecolor="w",markersize=6,markeredgecolor="black")
plt.plot(np.array(x_3),np.array(y_3).reshape(-1,1),marker='+',color="k",
             markerfacecolor="w",markersize=7,markeredgecolor="black")
plt.xlabel("$\it{k}$",fontsize=15)
plt.ylabel("$\it{P}$",fontsize=15)
plt.legend(['无保护度',"保护度"+str(chr(956).lower())+"=1","保护度"+str(chr(956).lower())+"=2",
            "保护度"+str(chr(956).lower())+"=3"],frameon=False,fontsize=12)
plt.show()