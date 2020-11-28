# -*- coding: utf-8 -*-
"""
Created on 2020-11-18

@author: 李运辰
"""

import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def count_fre(time_list,second=1):
    '''
    统计弹幕出现时间的频数（按指定second划分）
    输入：出现时间的列表，划分的秒数
    输出：频数分布
    '''
    f = lambda x:(x//second)*second 
    time_list = time_list.apply(f) # 按照second将时间进行划分
    counter = dict(Counter(time_list)) # 统计各时间段出现的频数
    counter = sorted(counter.items(),key=lambda d:d[0]) # 按照字典的key排序
    return dict(counter)

if __name__ == '__main__': 
    # 读取数据
    dms = pd.read_csv('年轻人不讲武德.csv')
    times = dms['出现时间']
    fres = count_fre(times)
    x = list(fres.keys()) # x轴，弹幕出现时间
    y = list(fres.values()) # y轴，弹幕的数量
    
    # 绘制分布图
    plt.title('弹幕频数分布') 
    plt.xlabel('播放时间（秒）')
    plt.ylabel('弹幕评论频数（个）')
    plt.grid()
    plt.plot(x,y)
    
    # 标红高潮部分
    flag = False
    start = 0 # 开始位置
    end = 0   # 结束位置
    level = np.percentile(y,90)
    for i in range(len(y)):
        if flag == False and y[i] >= level:
            flag = True
            start = i-1 if i-1 >= 0 else 0 # 避免低于0
        if flag == True and y[i] < level:
            flag = False
            end = i+1
            end = i+1 if i+1 <= len(x) else len(x) # 避免超过最大值
            plt.plot(x[start:end],y[start:end],color='red') # 标红
            pos_y = max(y[start:end]) # 高潮
            pos_x = y[start:end].index(pos_y)+start # 找到高潮对应的点
            pos_x = x[pos_x] # 找到高潮对应的时间（秒）
            m,s = divmod(pos_x,60) 
            text = '%02d:%02d'%(m,s) # 转为mm:ss的格式
            plt.text(pos_x+1,pos_y,text)