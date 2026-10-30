import matplotlib.pyplot as plt
import json

with open('lambda=0.75,k(3).json','r') as file:
    str = file.read()
    data = json.loads(str)
print(len(data[542:]))

plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内`
plt.plot(range(0, len(data[542:]), 20), [i for i in data[542::20]], marker='^',color='b', markerfacecolor="w",markersize=7,markeredgecolor="b", label='$<k>$')
plt.plot(range(0, len(data[542:]), 20), [round(i) for i in data[542::20]],'--', markerfacecolor="w",markersize=7,markeredgecolor="b",label='$[<k>]$')
#plt.xticks(fontsize=15)
#plt.yticks(fontsize=15)
plt.xlabel('$t$',fontsize=15)
plt.ylabel('$<k>$', fontsize=15)
plt.legend(frameon=False, fontsize=15)
plt.show()