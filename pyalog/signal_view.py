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
if __name__ == "__main__":
    check_rsi('result/kd/sp5-1303kd.pickle')