#from pyalgotrade import dataseries
import matplotlib.pyplot as pyplot
import pandas as pd
class dated_data:
    def __init__(self,dates,datas):
        self.dates = dates
        self.datas = datas

    def save(self ,name='data' ):
        inst = {}
        pd_data= pd.DataFrame()
        pd[name] = self.datas
        pd.index= self.dates
        '''
            inst['dates'] = self.dates
        inst['datas'] = self.datas
        '''

        return inst

    @staticmethod
    def load(inst):
        return dated_data(inst['dates'],inst['datas'])
    '''
    def view(self):
        values = []
        # for dateTime in series.getDateTimes():
        #    values.append(series.getValue(dateTime))
        fig, axes = pyplot.subplots(nrows=1, sharex=True, squeeze=False)
        pyplot.plot(self.dates, self.datas)
        fig.autofmt_xdate()
        # plt.legend(subPlot.getAllSeries().keys(), shadow=True, loc="best")
        # Don't scale the Y axis
        # plt.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        pyplot.show()

    '''

    def view(self,name,end = False):
        values = []
        # for dateTime in series.getDateTimes():
        #    values.append(series.getValue(dateTime))
        #fig, axes = pyplot.subplots(nrows=1, sharex=True, squeeze=False)
        fig=pyplot.gcf()
        pyplot.plot(self.dates, self.datas,label=name)
        fig.autofmt_xdate()
        pyplot.legend()
        # plt.legend(subPlot.getAllSeries().keys(), shadow=True, loc="best")
        # Don't scale the Y axis
        # plt.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
        if end == True:
            pyplot.show()
