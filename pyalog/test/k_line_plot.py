# -*- coding: utf-8 -*-
import numpy as np
#import tushare as ts
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import pandas as pd

data= pd.read_csv("../tw50_test/1102.csv")

#exit(0)
#data = ts.get_k_data('399300', index=True, start='2017-01-01', end='2017-06-31')
#sma_10 = talib.SMA(np.array(data['close']), 10)
#sma_30 = talib.SMA(np.array(data['close']), 30)

fig = plt.figure(figsize=(24, 8))
ax = fig.add_subplot(1, 1, 1)
#ax.set_xticks(range(0, len(data['Date']), 10))
#ax.set_xticklabels(data['Date'][::10])
#ax.plot(sma_10, label='10 日均线')
#ax.plot(sma_30, label='30 日均线')
ax.legend(loc='upper left')

mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'], data['Low'],colorup='r',colordown='green',width=1)
                     #width=0.5, colorup='r', colordown='g',)
                     #alpha=0.6)
plt.grid()
plt.show()
'''
note:
https://zhuanlan.zhihu.com/p/28584048 Matplotlib 蜡烛图教程
https://zhuanlan.zhihu.com/p/24282861
https://zhuanlan.zhihu.com/p/29519040
http://www.bigdatafinance.tw/index.php/393-python-3，＝＝＝ read
you can learn [資料分析&機器學習]
'''