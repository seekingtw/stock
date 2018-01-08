# coding=utf-8
import sys
sys.path.append("pyalgotrade-develop")
import pickle
from datetime import *
import matplotlib.pyplot as pyplot
from factor.trades import section_analyzer

from factor.mdd import mdd
from factor.dated_datas import dated_data
'''


'''
class trade_report:
    def __init__(self,name):
        self.timestamp=datetime.now()
        self.name=name
        self.infos = {}
    def save(self):
        pickle.dump(self.infos, open(self.name+".pickle","wb"))

    def add(self,name,val):
        self.infos[name] = val

    def view(self):
        for each in self.infos:
            if each == 'max drawdown':
                inst = mdd.load(self.infos['max drawdown'])
                inst.view()
            elif each == 'trade':
                inst = section_analyzer.load(self.infos['trade'])
                inst.view()
            elif each == 'trend':
                inst = self.infos['trend']
                for i,each in enumerate(inst['datas']):
                    datas =dated_data(each['dates'],each['datas'])
                    datas.view(inst['names'][i],i+1==len(inst['names']))
                    #self.plot_each(datas,inst['datas'][-1])
                    #print each
                #for each in inst['names']:
                #    print each
                datas =dated_data(inst['vol']['dates'],inst['vol']['datas'])
                datas.view('vol', True)



    '''pandas csv data'''
    def data(self,data):
        self.data=data
    
    def profilio(self,profilio):
        self.profilio= profilio

    def record(self,record):
        self.record=record

    def get_report(filename):
        return pickle.load(open(filename,"rb"))
    @staticmethod

    def plot_each(series,end = 0):
        values = []
        # for dateTime in series.getDateTimes():
        #    values.append(series.getValue(dateTime))
        pyplot.plot(series.getDateTimes(), series.getValues())
        if end == series:
            #pyplot.show()
            pass
    @staticmethod
    def result_plot(series):
        values = []
        # for dateTime in series.getDateTimes():
        #    values.append(series.getValue(dateTime))
        fig, axes = pyplot.subplots(nrows=1, sharex=True, squeeze=False)
        pyplot.plot(series.getDateTimes(), series.getValues())
        # fig.autofmt_xdate()
        # plt.legend(subPlot.getAllSeries().keys(), shadow=True, loc="best")
        # Don't scale the Y axis
        # plt.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        pyplot.show()

    @staticmethod
    def load(filename):
        inst = trade_report('report')
        inst.infos = pickle.load(open(filename, "rb"))
        return inst

    pass


if __name__ == "__main__" :
    ''' test input
    test_obj=algo_report("test")
    test_pd=pd.DataFrame([[1,4,5],[3,2,4]],columns=["a","b","d"])
    test_pd2=test_pd.append(pd.DataFrame([[1,4,5],[3,2,4]],columns=["a","b","d"]))
    test_obj.data(test_pd)
    test_obj.profilio(test_pd2)

    test_obj.save()
    '''
    ''' test input
    a= algo_report.get_algo_report('test.pickle')
    print (a) 
    print (a.__dict__)
    print (a)
    print (a.data)
    '''
    report = trade_report.load('2018-01-08-22:02-1102.pickle')
    report.view()

    pass
