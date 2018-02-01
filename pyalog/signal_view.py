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
    def __init__(self, axes,lines_2d):
        self.lys =[]
        self.lxs= []
        self.texts=[]
        #self.lx = axes[0].axhline(color='k')  # the horiz line
        for i,ax in enumerate(axes):
            self.lys.append(ax.axvline(x=lines_2d[i].get_xdata()[0],color='k'))  # the vert line
            self.lxs.append (ax.axhline(y=0.05,color='k')  )# the horiz line
            # cal text pos
            x_pos =lines_2d[i].get_xdata(orig=False)
            y_list=  lines_2d[i].get_ydata()
            #get first num
            first_num = 0
            while 1:
                if (str(lines_2d[i].get_ydata()[first_num])!= '--'):
                    #print "find ",lines_2d[i].get_ydata()[first_num]
                    break
                else:
                    first_num +=1

            y_pos_max = max(y_list[first_num:])
            y_pos_min= ymin=min(y_list[first_num:])
            self.texts.append(  ax.text(lines_2d[i].get_xdata()[0],y_pos_max*1.1,"data"))
            ymin= y_pos_min *0.8 if y_pos_min> 0 else y_pos_min *1.2
            ymax = y_pos_max * 1.3if y_pos_max > 0 else y_pos_max * 0.87
            ax.set_ylim(ymin=ymin,ymax=ymax)


        print self.lxs
        print self.lys
        print self.lxs[0],self.lxs[1]
        # text location in axes coords
        #self.txt = axes[0].text(0.7, 0.9, '', transform=ax.transAxes)

        self.lines= lines_2d
        #self.axes=axes


    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        #x_pos =self.lines.get_xdata(orig=False)
        #indx = np.searchsorted(x_pos, [x])[0]

        #self.lx.set_ydata(y)
        #print "=--------------"
        for i,each in enumerate(self.lys):
            x_pos =self.lines[i].get_xdata(orig=False)
            indx = np.searchsorted(x_pos, [x])[0]
            x_data=self.lines[i].get_xdata()[indx]
            self.lys[i].set_xdata(x_data)
            #print self.lines[i].get_ydata()[indx]
            #print self.lxs[i]
            y_data=self.lines[i].get_ydata()[indx]
            self.lxs[i].set_ydata(y_data)
            self.texts[i].set_text('x=%s y=%1.3f' % (x_data, y_data))
        #for i, each in enumerate(self.axes):
        #print "=--------------="
        #for i,each in enumerate(self.lxs):
        #    each.set_ydata(self.lines[i].get_ydata()[indx])
        #self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
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
    lines=[]


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

    # p.plot(inst['trade']['datetime'],inst['trade']['price'])
    aa = inst['trend']['prices'].plot(ax=p)
    lines.append(aa.get_lines()[0])

    # p.scatter(short_signal['date'],short_signal['data'],color='g')


# p.plot(inst['trade']['datetime'],inst['trade']['price'])
    p.scatter(long_signal['date'], long_signal['data'], color='r')
    p.scatter(short_signal['date'], short_signal['data'], color='g')
    plt.grid(True)

    strategy_name= 'bband'
    for each in inst['trend']:
        if each != 'vol' and each != 'prices':
            strategy_name = each

    p = plt.subplot(2, 1, 2)
    aa = inst['trend'][strategy_name].plot(ax=p)
    lines.append(aa.get_lines()[0])

    datapd = inst['trend'][strategy_name]
    #datapd=datapd.fillna(0)
    datapd2=datapd.dropna()
    #print datapd
    print datapd2.describe()
    p.grid(True)



    allaxes = gcf().get_axes()

    cursor = Cursor(allaxes,lines)
    # cursor = SnaptoCursor(ax, t, s)
    plt.connect('motion_notify_event', cursor.mouse_move)

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
    check_rsi('result/kd/sp5-1303kd.pickle')
    #check_rsi('result/macd/sp5-1303macd.pickle')
    #check_rsi('result/dma/sp5-1303dma.pickle')
    #check_rsi('result/trend/sp5-1303trend.pickle')

    #check_rsi('result/roc/sp5-1303roc.pickle')
