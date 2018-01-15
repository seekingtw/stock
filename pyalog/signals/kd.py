__metaclass__ = type
import sys

sys.path.append("pyalgotrade-develop")
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import quandl
from pyalgotrade.technical import bollinger
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade import broker as basebroker
from pyalgotrade import plotter
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from pyalgotrade.technical import ma
from pyalgotrade.technical import stoch
from trend import *
from factor.dated_datas import *
from signals import baseSignal

class kd_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,**kwargs):
        '''

        :param strategy:
        :param feed:
        :param instrument:
        :param fast_period:
        :param slow_period:
        :param kwargs:
            fast_period
            slow_period
        '''
        self.set_member('fast_period',5,kwargs)
        self.set_member('slow_period', 20,kwargs)
        fast_period = self.fast_period
        slow_period = self.slow_period
        super(kd_signal, self).__init__(strategy, feed, instrument)
        self.fast_ma= ma.SMA(feed[instrument].getCloseDataSeries(), fast_period)
        self.fast_period = fast_period

        self.slow_ma = ma.SMA(feed[instrument].getCloseDataSeries(), slow_period)
        self.slow_period = slow_period
        self.fast__trend = TrendRatio(self.prices, fast_period)
        self.slow__trend = TrendRatio(self.prices, slow_period)
        self.kd = stoch.StochasticOscillator(feed[instrument],slow_period,fast_period,False,None)

        self.plot_init(True)

    def trend_long(self,ma):
        if  ma[-5] is  None:
            return  False

        if (ma[-1] -ma[-5])/ma[-5] > 0.00:
            return True
        print "trend no long", (ma[-1] - ma[-5]) / ma[-5]
        return False
    def trend_short(self,ma):
        if  ma[-5] is  None:
            return  False
        if (ma[-1] -ma[-5])/ma[-5] < -0.02 :
            return True
        return False

    def long_signal(self):
        if cross.cross_above(self.kd.getKD_k(), self.kd.getKD_d()) :#and self.__trend.trend_current_ratio() >=0:
            #if self.trend_long(self.fast_ma) and self.trend_long(self.slow_ma):
            '''adjust'''
            #if self.kd.getKD_d()[-1] > 30 :#and self.trend_long(self.slow_ma):
            return True
        return False
        pass
    def short_signal(self):
        if cross.cross_below(self.kd.getKD_k(), self.kd.getKD_d()) :#and self.__trend.trend_current_ratio() >=0:
                return True
        #if self.trend_short(self.slow_ma):
         #   return True
        ''' adjust'''
        #if self.kd.getKD_d()[-1] < 30  :
        #    return True
        #if self.trend_short(self.fast_ma)  :
        #    return True
        return False
        pass

    def long(self,bars):
        if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
            return True
        return False
        pass
    def short(self,bars):
        if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
            return True
        return False
        pass

    def plot_init(self, plot):
        if plot:  # plot:
            super(kd_signal, self).plot_init(plot)
           # self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("fast_ma", self.fast_ma)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("slow_ma",
                                                                           self.slow_ma)
            self.plt.getOrCreateSubplot("trend").addDataSeries("fast", self.fast__trend.getTrend())
            self.plt.getOrCreateSubplot("trend").addDataSeries("slow", self.slow__trend.getTrend())
            self.plt.getOrCreateSubplot("KD").addDataSeries("k", self.kd.getKD_k())
            self.plt.getOrCreateSubplot("KD").addDataSeries("d", self.kd.getKD_d())

        pass


    def plot_show(self):
        self.plt.plot()
        pass


    def save(self):
        inst = {}

        data_pd= pd.DataFrame()
        data_pd['k']= self.kd.getKD_k().getValues()
        data_pd.index= self.kd.getKD_k().getDateTimes()
        data_pd['d']= self.kd.getKD_d().getValues()
        inst['kd']= data_pd


        data_pd= pd.DataFrame()
        data_pd['vol']= self.vol.getValues()
        data_pd.index= self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd= pd.DataFrame()
        data_pd['prices']= self.prices.getValues()
        data_pd.index= self.prices.getDateTimes()
        inst['prices'] = data_pd
        return inst
    '''
    note : very fast response:
    fit for large range stock.
    don't use it on smooth failling.

    '''