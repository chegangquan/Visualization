import pandas as pd
import math
import numpy as np

from matplotlib import pyplot as plt


# 读取数据
def read(file):
    df = pd.read_excel(file)
    # 体测成绩数值化
    df.loc[df['Constitution'] == 'excellent', 'Constitution'] = 90  # Constitution等于‘excellent’的Constitution赋值90
    df.loc[df['Constitution'] == 'good', 'Constitution'] = 80  # Constitution等于‘good’的Constitution赋值80
    df.loc[df['Constitution'] == 'general', 'Constitution'] = 70  # Constitution等于‘general’的Constitution赋值70
    df.loc[df['Constitution'] == 'bad', 'Constitution'] = 50  # Constitution等于‘bad’的Constitution赋值50
    # C10成绩缺失，这里将其赋值为C6成绩
    df['C10'] = df['C6']
    return df


# 均值函数 E(x)=1/n∑xi
def avg(a):
    return sum(a) / len(a)


# 标准差 √a=√(E[a-E(a)]^2)
def std(a):
    return math.sqrt(avg((a - avg(a)) ** 2))


# x与y的斜方差 cov(x,y)=E( (x-E(x))*(y-E(y)) )
def covf(x, y):
    return avg((x - avg(x)) * (y - avg(y)))


# 相关系数 pxy=cov(x,y)/(√x*√y)
def cor(x, y):
    return covf(x, y) / (std(x) * std(y))


# z_score标准化
def z_score(a):
    E = avg(a)  # 均值
    S = std(a)  # 标准差
    Z = []
    for i in range(len(a)):
        Z.append((a[i] - E) / S)  # 标准化
    return Z


# 成绩标准化
def score_standard(arr):
    for i in range(arr.shape[1]):
        arr[:, i] = z_score(arr[:, i])
    return arr


# 构造相关矩阵
def cor_matrix(a, b):
    mar = []  # 用于存储相关矩阵
    for i in range(a.shape[0]):
        mar.append([])
        for j in range(b.shape[0]):
            mar[i].append(cor(a[i], b[j]))  # 得出两者的相关系数
    return np.array(mar)


# 画图
def paint(correlation_matrix):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig = plt.figure()  # 调用figure创建一个绘图对象
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlation_matrix, vmin=-1, vmax=1)  # 绘制热力图，从-1到1
    fig.colorbar(cax)  # 将matshow生成热力图设置为颜色渐变条
    ax.set_title("相关矩阵")
    ax.set_xlabel("ID")
    ax.set_ylabel("ID")
    plt.savefig('../Data/correlation_matrix.jpg')


# 找到距离每个样本最近的三个样本
def find_similar(correlation_matrix):
    minindex = []  # 最相近表
    nearindex = 0
    for i in range(correlation_matrix.shape[0]):
        minindex.append([])
        for k in range(3):
            min = 1
            for j in range(correlation_matrix.shape[1]):
                # 排除对角线的值，排除已经位于最相近表的值
                if i != j & j not in minindex[i]:
                    diff = 1 - correlation_matrix[i][j]  # 计算二者的差异度
                    if diff <= min:
                        min = diff  # 记住此轮循环最小的差异度
                        nearindex = j  # 记住此轮循环的最接近样本的索引
            minindex[i].append(nearindex)  # 获得3个索引值

    for i in range(correlation_matrix.shape[0]):
        for j in range(3):
            minindex[i][j] = df.loc[minindex[i][j]]['ID']  # 根据索引转换为学生ID

    return minindex


if __name__ == '__main__':
    df = read('../Data/MultiSourceData.xlsx')

    arr = df.values  # dataframe转换为矩阵
    arr = np.delete(arr, [0, 1, 2, 3, 4], axis=1)  # 删除无关紧要的列，留下11门成绩
    arr = score_standard(arr)  # 各门成绩Z标准化
    data_df = pd.DataFrame(arr)
    writer = pd.ExcelWriter('../Data/score_std.xlsx')
    data_df.to_excel(writer, 'page_1', float_format='%.5f')
    writer.save()  # 3对每门成绩进行z-score归一化，得到归一化的数据矩阵，保存为score_std.xlsx文件

    correlation_matrix = cor_matrix(arr, arr)  # 相关矩阵

    paint(correlation_matrix)  # 画混淆矩阵图

    data_df = pd.DataFrame(correlation_matrix)
    writer = pd.ExcelWriter('../Data/correlation_matrix.xlsx')
    data_df.to_excel(writer, 'page_1', float_format='%.5f')
    writer.save()  # 4计算出106x106的相关矩阵，将矩阵保存为correlation_matrix.xlsx文件。

    # 5根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵
    similar_index = find_similar(correlation_matrix)
    # 保存为txt文件
    output = open('../Data/similar_data.txt', 'w', encoding='gbk')
    for i in range(len(similar_index)):
        for j in range(3):
            output.write(str(similar_index[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下
        output.write('\n')  # 写完一行立马换行
    output.close()
