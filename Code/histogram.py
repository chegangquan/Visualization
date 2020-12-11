import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = "../Data/MultiSourceData.xlsx"
data = pd.read_excel(filename)
# 读取课程1的成绩，及其最大值、最小值
c1_max = data['C1'].max()
c1_min = data['C1'].min()
c1 = np.array(data['C1'])

# 计算直方图x轴的范围
n = int(c1_max / 10) * 10
if c1_max == n:
    right = n
else:
    if (c1_max > n) and (c1_max <= n + 5):
        right = n + 5
    else:
        right = n + 10
w = int(c1_min / 10) * 10
if (c1_min >= w) and (c1_min < w + 5):
    left = w
else:
    if c1_min >= w + 5:
        left = w + 5

# 直方图的柱子数
num = int((right - left) / 5)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# matplotlib画图中中文显示会有问题，需要这两行设置默认字体
plt.xlabel('课程1成绩')
plt.ylabel('人数')

counts, _, patches = plt.hist(x=c1,  # 指定绘图数据
                              bins=num,  # 指定直方图中条块的个数
                              range=[left, right],  # 指定直方图的统计范围
                              color='steelblue',  # 指定直方图的填充色
                              edgecolor='black'  # 指定直方图的边框色
                              )

# 标注每个柱的高度
for count, patch in zip(counts, patches):
    plt.annotate(str(int(count)), xy=(patch.get_x() + 2, patch.get_height() + 0.5))

plt.savefig(r'../Data/histogram', dpi=300)
