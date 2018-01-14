__metaclass__ = type
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
from pyalgotrade.technical import macd
from trend import *
from factor.dated_datas import *
from signals import baseSignal


class macd_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,**kwargs):
        '''

        :param strategy:
        :param feed:
        :param instrument:
        :param fast_period:
        :param slow_period:
        :param signal_period:
        :param kwargs:
        signal_period
        fast_period
        slow_period
        '''
        super(macd_signal, self).__init__(strategy, feed, instrument)
        self.set_member('fast_period',12,kwargs)
        self.set_member('slow_period', 26,kwargs)
        self.set_member('signal_period', 9, kwargs)
        self.macd= macd.MACD(feed[instrument].getCloseDataSeries(), self.fast_period,self.slow_period,self.signal_period)
        #self.__strategy= strategy
        #self.__instrument = instrument
        #self.__prices = feed[instrument].getPriceDataSeries()
        self.vol=feed[instrument].getVolumeDataSeries()
        self.fast__trend = TrendRatio(self.prices, self.fast_period)
        self.slow__trend = TrendRatio(self.prices, self.slow_period)

        self.plot_init(True)

    def long(self,bars):
        #if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        #    return True
        if self.macd.getHistogram()[-1]> 0 and self.macd.getHistogram()[-2] <=0 and \
                        self.macd.getSignal()[-1] > 0 and self.slow__trend.trend_current_ratio() >=0:
            return True
        return False
        pass
    def short(self,bars):
        #if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:

        if self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0:#  and self.macd.getSignal()[-1] < 0:
        #if (self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0 )or self.slow__trend.trend_current_ratio() < 0:

            return True
        return False
        pass
    def long_signal(self):
        #if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        #    return True
        if self.macd.getHistogram()[-1]> 0 and self.macd.getHistogram()[-2] <=0 and \
                        self.macd.getSignal()[-1] > 0 :#and self.slow__trend.trend_current_ratio() >=0:
            return True
        return False
        pass
    def short_signal(self):
        #if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        if len(self.macd.getHistogram()) <2 :
            return False
        if self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0:#  and self.macd.getSignal()[-1] < 0:
        #if (self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0 )or self.slow__trend.trend_current_ratio() < 0:

            return True
        return False
        pass

    def plot_init(self, plot):
        if plot:  # plot:
            super(macd_signal, self).plot_init(plot)
            #self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            #self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("fast_ma", self.fast_ma)
            #self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("slow_ma",
            #                                                               self.slow_ma)
            self.plt.getOrCreateSubplot("macd").addDataSeries("signal", self.macd.getSignal())
            self.plt.getOrCreateSubplot("macd").addDataSeries("getHistogram", self.macd.getHistogram())
            #self.plt.getOrCreateSubplot("macd").addDataSeries("fast_trend", self.fast__trend.getTrend())
            self.plt.getOrCreateSubplot("macd").addDataSeries("slow_period", self.slow__trend.getTrend())
            #self.plt.getOrCreateSubplot("vol").addDataSeries("vol", self.vol)
        pass


    def plot_show(self):
        self.plt.plot()
        pass


    def save(self):
        inst = {}

        data_pd= pd.DataFrame()
        data_pd['hist']= self.macd.getHistogram().getValues()
        data_pd.index= self.macd.getHistogram().getDateTimes()
        data_pd['signal']= self.macd.getSignal().getValues()
        inst['macd']= data_pd

        data_pd= pd.DataFrame()
        data_pd['vol']= self.vol.getValues()
        data_pd.index= self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd= pd.DataFrame()
        data_pd['prices']= self.prices.getValues()
        data_pd.index= self.prices.getDateTimes()
        inst['prices']=data_pd


        return inst
