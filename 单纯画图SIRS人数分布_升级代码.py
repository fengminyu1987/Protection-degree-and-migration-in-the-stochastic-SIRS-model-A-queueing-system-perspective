import matplotlib.pyplot as plt
import json
import os

# 定义参数组合和对应的文件映射
parameter_groups = {
    'alpha': {
        0: 0.8,  # baseline
        1: 0.4,
        2: 1.6,
        'label': r'$\alpha$',
        'files': [1, 2, 3],
        'subplot_id': 'a'  # 添加子图编号
    },
    'lambda': {
        0: 3.0,  # baseline
        5: 1.5,
        6: 6.0,
        'label': r'$\lambda$',
        'files': [1, 6, 7],
        'subplot_id': 'b'
    },
    'retention': {
        0: 0.995,  # baseline
        7: 0.990,
        8: 0.997,
        'label': r'$p$',
        'files': [1, 8, 9],
        'subplot_id': 'c'
    },
    'gamma': {
        0: 0.7,  # baseline
        3: 0.35,
        4: 1.4,
        'label': r'$\gamma$',
        'files': [1, 4, 5],
        'subplot_id': 'd'
    },
    'beta': {
        0: 0.001,  # baseline
        11: 0.0005,
        12: 0.002,
        'label': r'$\beta$',
        'files': [1, 12, 13],
        'subplot_id': 'e'
    }
}


def load_and_process_data(filename, state):
    """加载和处理单个JSON文件的数据"""
    with open(f'({filename}).json', 'r') as f:
        dist = json.loads(f.read())
    S = dist[state]

    NS = list(map(int, S.keys()))
    ds = list(S.values())

    # 归一化
    total = sum(ds)
    ds = [d / total for d in ds]

    return NS, ds


def plot_parameter_comparison(param_name, state):
    """为指定参数和状态绘制比较图"""
    param_info = parameter_groups[param_name]
    files = param_info['files']

    # 创建新的图形
    plt.figure(figsize=(8, 6))

    # 设置绘图样式
    markers = ['o', 's', '^']
    colors = ['b', 'r', 'g']

    for i, file_num in enumerate(files):
        NS, ds = load_and_process_data(file_num, state)
        param_value = param_info[i if i == 0 else files[i] - 1]

        plt.scatter(NS, ds,
                    marker=markers[i],
                    color='white',
                    edgecolors=colors[i],
                    label=f'{param_info["label"]} = {param_value:.4f}')

    # 设置图形格式
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.gcf().subplots_adjust(left=0.16, bottom=0.15)

    if state == 'I' and param_name == 'gamma':
        plt.legend(frameon=False, loc='upper center', borderaxespad=0, bbox_to_anchor=(0.65, 1),
                  prop={'family': 'SimSun', 'size': 19}, handletextpad=0.0001)
    else:
        plt.legend(frameon=False, loc='upper right', borderaxespad=0,
                  prop={'family': 'SimSun', 'size': 19}, handletextpad=0.0001)

    plt.xlabel(f"$\mathrm{{{state}}}$", font={'family': 'SimSun', 'size': 20})
    plt.ylabel(f"$P(\mathrm{{{state}}})$", font={'family': 'SimSun', 'size': 20})
    plt.xticks(font={'family': 'SimSun', 'size': 15})
    plt.yticks(font={'family': 'SimSun', 'size': 15})

    # 新的文件命名规则
    filename = f'd{state}_{param_info["subplot_id"]}.pdf'

    # 保存为PDF
    plt.savefig(f"D:\论文\中文 系统工程\中文\新图-审阅后 最新\{filename}", format='pdf', dpi=300, bbox_inches='tight')
    plt.close()


def plot_all_combinations():
    """为所有参数-状态组合生成单独的图表"""
    states = ['S', 'I', 'R']

    # 为每个参数和每个状态生成图表
    for param in parameter_groups.keys():
        for state in states:
            print(f"Plotting {param} for state {state}")
            plot_parameter_comparison(param, state)


if __name__ == "__main__":
    # 生成所有图表
    plot_all_combinations()
    print("All plots have been generated!")