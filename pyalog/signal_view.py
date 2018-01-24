import pandas as pd
import datetime
from pylab import *
import pickle

def struct(dict_data,level =0):
    keys = dict_data.keys()

    for each in keys:
        if type(dict_data[each]) == dict:
            print "\t"*level+each
            struct(dict_data[each],level+1)
        else:
            print "\t"*level+each," : ",type(dict_data[each])
class Cursor(object):
    def __init__(self, axes):
        self.lys =[]
        self.ax = axes[0]
        self.lx = axes[0].axhline(color='k')  # the horiz line
        for ax in axes:
            self.lys.append(ax.axvline(color='k'))  # the vert line

        # text location in axes coords
        self.txt = axes[0].text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        for each in self.lys:
            each.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()

def check_signal(inputfile='sp20-1303bband.pickle'):
#    inputfile='sp20-1102bband.pickle'
#    inputfile='sp20-1301bband.pickle'
    inst=pickle.load(open(inputfile))
    struct(inst)

    strategy_name= 'bband'
    for each in inst['trend']:
        if each != 'vol' and each != 'prices':
            strategy_name = each
    p = plt.subplot(1, 1, 1)
    inst['trend'][strategy_name].plot(ax=p)

    long_signal = {'date': [], 'data': []}
    short_signal = {'date': [], 'data': []}
    inst['trade']['type']

    for i in range(len(inst['trade']['datetime'])):
        if inst['trade']['type'][i] == 'long':
            long_signal['date'].append(inst['trade']['datetime'][i])
            long_signal['data'].append(inst['trade']['price'][i])
        if inst['trade']['type'][i] == 'long_exit':
            short_signal['date'].append(inst['trade']['datetime'][i])
            short_signal['data'].append(inst['trade']['price'][i])

    # print long_signal
    # print short_signal
    p.scatter(long_signal['date'], long_signal['data'], color='r')
    p.scatter(short_signal['date'],short_signal['data'],color='g')
    plt.grid(True)
    plt.show()


def check_rsi(inputfile='sp20-1303bband.pickle'):
#    inputfile='sp20-1102bband.pickle'
#    inputfile='sp20-1301bband.pickle'
    inst=pickle.load(open(inputfile))
    struct(inst)


    strategy_name= 'bband'
    for each in inst['trend']:
        if each != 'vol' and each != 'prices':
            strategy_name = each
    p = plt.subplot(2, 1, 2)
    inst['trend'][strategy_name].plot(ax=p)

    datapd = inst['trend'][strategy_name]


    #datapd=datapd.fillna(0)
    datapd2=datapd.dropna()
    #print datapd



    print datapd2.describe()



    p.grid(True)
    p = plt.subplot(2, 1, 1)
    long_signal = {'date': [], 'data': []}
    short_signal = {'date': [], 'data': []}
    inst['trade']['type']

    for i in range(len(inst['trade']['datetime'])):
        if inst['trade']['type'][i] == 'long':
            long_signal['date'].append(inst['trade']['datetime'][i])
            long_signal['data'].append(inst['trade']['price'][i])
        if inst['trade']['type'][i] == 'long_exit':
            short_signal['date'].append(inst['trade']['datetime'][i])
            short_signal['data'].append(inst['trade']['price'][i])

    # print long_signal
    # print short_signal

    #p.plot(inst['trade']['datetime'],inst['trade']['price'])
    inst['trend']['prices'].plot(ax=p)
    p.scatter(long_signal['date'], long_signal['data'], color='r')
    p.scatter(short_signal['date'],short_signal['data'],color='g')


    allaxes = gcf().get_axes()

    cursor = Cursor(allaxes)
    # cursor = SnaptoCursor(ax, t, s)
    plt.connect('motion_notify_event', cursor.mouse_move)
    plt.grid(True)
    plt.show()


def check_kd(inputfile='sp20-1303bband.pickle'):
#    inputfile='sp20-1102bband.pickle'
#    inputfile='sp20-1301bband.pickle'
    inst=pickle.load(open(inputfile))
    struct(inst)

    strategy_name= 'bband'
    for each in inst['trend']:
        if each != 'vol' and each != 'prices':
            strategy_name = each
    p = plt.subplot(2, 1, 2)
    inst['trend'][strategy_name].plot(ax=p)


    p.grid(True)
    p = plt.subplot(2, 1, 1)
    long_signal = {'date': [], 'data': []}
    short_signal = {'date': [], 'data': []}
    inst['trade']['type']

    for i in range(len(inst['trade']['datetime'])):
        if inst['trade']['type'][i] == 'long':
            long_signal['date'].append(inst['trade']['datetime'][i])
            long_signal['data'].append(inst['trade']['price'][i])
        if inst['trade']['type'][i] == 'long_exit':
            short_signal['date'].append(inst['trade']['datetime'][i])
            short_signal['data'].append(inst['trade']['price'][i])

    # print long_signal
    # print short_signal

    #p.plot(inst['trade']['datetime'],inst['trade']['price'])
    inst['trend']['prices'].plot(ax=p)
    p.scatter(long_signal['date'], long_signal['data'], color='r')
    p.scatter(short_signal['date'],short_signal['data'],color='g')
    plt.grid(True)
    plt.show()


'''

import matplotlib.pyplot as pyplot
def result_plot(series):
    values = []
    #for dateTime in series.getDateTimes():
    #    values.append(series.getValue(dateTime))
    fig, axes = pyplot.subplots(nrows=1, sharex=True, squeeze=False)
    pyplot.plot(series.getDateTimes(), series.getValues())
    #fig.autofmt_xdate()
    #plt.legend(subPlot.getAllSeries().keys(), shadow=True, loc="best")
# Don't scale the Y axis
    #plt.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    pyplot.show()
    pass
'''
if __name__ == "__main__":
    #check_rsi('result/kd/sp5-1303kd.pickle')
    #check_rsi('result/macd/sp5-1303macd.pickle')
    #check_rsi('result/dma/sp5-1303dma.pickle')
    #check_rsi('result/trend/sp5-1303trend.pickle')

    check_rsi('result/roc/sp5-1303roc.pickle')
