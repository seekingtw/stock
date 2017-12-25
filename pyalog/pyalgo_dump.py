# coding=utf-8
import sys
sys.path.append("pyalgotrade-develop")
import pickle
from datetime import *
import pandas as pd
import matplotlib.pyplot as pyplot
from pyalgotrade import dataseries
class tradereport:
    def __init__(self,name):
        self.timestamp=datetime.now()
        self.name=name
    def save(self):
        pickle.dump(self, open(self.name+".pickle","wb"))

    '''pandas csv data'''
    def data(self,data):
        self.data=data
    
    def profilio(self,profilio):
        self.profilio= profilio

    def record(self,record):
        self.record=record

    def get_algo_report(filename):
        return pickle.load(open(filename,"rb"))

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

    pass
