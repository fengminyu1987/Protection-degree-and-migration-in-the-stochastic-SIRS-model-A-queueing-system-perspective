name="a"
import matplotlib.pyplot as plt
import json
f = open('n6.json', 'r')
content = f.read()
time_seq= json.loads(content)

short=int(1*len(time_seq))
time_seq=time_seq[:short]

plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签


fig = plt.figure(figsize=(9, 6))
plt.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.12)

plt.plot(range(0,40*len(time_seq[:100]),40), [i[0] for i in time_seq[:100]], "-", c="b",linewidth=3, label="易感人数")
plt.plot(range(0,40*len(time_seq[:100]),40), [i[1] for i in time_seq[:100]], "-.", c="r",linewidth=3, label="感染人数")
plt.plot(range(0,40*len(time_seq[:100]),40), [i[2] for i in time_seq[:100]], '--', c="g",linewidth=3, label="免疫人数")
plt.xlabel("$t$",fontsize=20)
plt.ylabel("$N$",fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20,frameon=False,loc="upper right")
plt.show()
# plt.savefig("%s.pdf"%name)
