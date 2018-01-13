#__metaclass__ = type
import sys

sys.path.append("pyalgotrade-develop")
from signals import baseSignal
from signals.trend import TrendRatio
from factor.dated_datas import  dated_data
from pyalgotrade.technical.rsi import RSI
from pyalgotrade import plotter
import pandas as pd

class rsi_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,**kwargs):
        '''
        :param strategy:
        :param feed:
        :param instrument:
        #:param period:
        period
        '''
        super(rsi_signal, self).__init__(strategy, feed, instrument)
        self.set_member('period',20,kwargs)
        self.rsi= RSI(feed[instrument].getCloseDataSeries(), self.period)
        self.vol=feed[instrument].getVolumeDataSeries()
        self.trend = TrendRatio(self.prices, self.period)
        self.plot_init(True)

    def long_signal(self):
        # if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        #    return True
        if len(self.rsi) <= 2 or self.rsi[-2] == None:
            return False
        if  self.rsi[-1] > 20 and  self.rsi[-2] <= 20: # and self.slow__trend.trend_current_ratio() >=0:
            return True
        return False
        pass


    def short_signal(self):
        # if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        if len(self.rsi) <= 2 or self.rsi[-2] == None:
            return False
        if self.rsi[-1] <= 80 and self.rsi[-2] > 80:  # and self.macd.getSignal()[-1] < 0:
            # if (self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0 )or self.slow__trend.trend_current_ratio() < 0:
            return True
        return False
        pass


    def save(self):
        inst = {}

        data_pd = pd.DataFrame()
        data_pd['rsi']= self.rsi.getValues()
        data_pd.index = self.rsi.getDateTimes()
        inst['rsi'] = data_pd
        #inst['vol'] = dated_data(self.vol.getDateTimes(),self.vol.getValues()).save()

        data_pd= pd.DataFrame()
        data_pd['vol']= self.vol.getValues()
        data_pd.index= self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd= pd.DataFrame()
        data_pd['prices']= self.prices.getValues()
        data_pd.index= self.prices.getDateTimes()
        inst['prices'] = data_pd
        return inst

    def plot_init(self, plot):
        if plot:  # plot:
            super(rsi_signal, self).plot_init(plot)
            self.plt.getOrCreateSubplot("rsi").addDataSeries("rsi", self.rsi)
        pass

    def plot_show(self):
        self.plt.plot()
        pass

'''
the same thing of 'reserve trend ' , when trend is change. it may fail.
'''