import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = "../Data/MultiSourceData.xlsx"
data = pd.read_excel(filename)
data.loc[data['Constitution'] == 'excellent', 'Constitution'] = 90  # Constitution等于‘excellent’的Constitution赋值90
data.loc[data['Constitution'] == 'good', 'Constitution'] = 80  # Constitution等于‘good’的Constitution赋值80
data.loc[data['Constitution'] == 'general', 'Constitution'] = 70  # Constitution等于‘general’的Constitution赋值70
data.loc[data['Constitution'] == 'bad', 'Constitution'] = 50  # Constitution等于‘bad’的Constitution赋值50

# 读取课程1成绩和体能成绩
c1 = np.array(data['C1'])
constitution = np.array(data['Constitution'])

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# matplotlib画图中中文显示会有问题，需要这两行设置默认字体

plt.xlabel('课程1')
plt.ylabel('体能成绩')

colors1 = '#FF6347'  # 点的颜色
area = 30  # 点面积
plt.scatter(c1, constitution, s=area, c=colors1, label='课程1-体能成绩散点图')

plt.savefig(r'../Data/scatter_plot', dpi=300)