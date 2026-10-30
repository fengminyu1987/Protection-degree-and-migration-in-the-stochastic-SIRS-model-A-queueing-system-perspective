import numpy as np
import matplotlib.pyplot as plt

# 定义wmape函数
def wmape(arr1, arr2):
    return np.sum(np.abs(arr1 - arr2)) / np.sum(np.abs(arr1))

# 读取保存的模拟结果
solutions = np.load('solution_sampled4c5d8d60-a188-4ae5-becf-bba5439f1d10.npz')
solutions_sampled = solutions['arr_0']  # 所有的模拟结果

# 真实数据
real_data = np.array([43, 67, 108, 145, 152, 155, 186, 190, 195, 201, 193, 191,
                      181, 175, 171, 153, 153, 149, 142, 128, 124, 118, 109])

# 计算每个模拟结果的wmape
wmape_values = []
for simu in solutions_sampled:
    wmape_values.append(wmape(real_data, simu))

# 找到wmape最小的模拟结果
best_idx = np.argmin(wmape_values)
simu_best = solutions_sampled[best_idx]

print(f"最小的WMAPE值: {min(wmape_values)}")

# 设置绘图参数
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 创建图形
fig = plt.figure(figsize=(9, 6))
plt.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.12)

# 绘制理论模型和真实数据
plt.plot(range(len(simu_best)), simu_best, "b-", linewidth=3, label="理论模型")
plt.plot(range(len(real_data)), real_data, "-.", c="r", linewidth=3, label="真实数据")

# 添加垂直线
plt.axvline(x=12, ls="-", c="g")

# 设置标签和字体
plt.xlabel("$t$", font={'family':'SimSun', 'size':20})
plt.ylabel("$N$", font={'family':'SimSun', 'size':20})
plt.xticks(font={'family':'SimSun', 'size':20})
plt.yticks(font={'family':'SimSun', 'size':20})
plt.legend(frameon=False, loc="lower right", prop={'family': 'SimSun', 'size': 20})

# 显示图形
plt.show()

# 如果需要保存图形
# plt.savefig("henan.pdf", bbox_inches='tight', dpi=300)