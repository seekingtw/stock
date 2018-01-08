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
from trend import *
from factor.dated_datas import *
from signals import baseSignal


class macd_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,signal_period,**kwargs):
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
        self.set_member('fast_period',5,kwargs)
        self.set_member('slow_period', 20,kwargs)
        self.set_member('short_signal', 3, kwargs)
        self.macd= macd.MACD(feed[instrument].getCloseDataSeries(), fast_period,slow_period,signal_period)
        #self.__strategy= strategy
        #self.__instrument = instrument
        #self.__prices = feed[instrument].getPriceDataSeries()
        self.vol=feed[instrument].getVolumeDataSeries()
        self.fast__trend = TrendRatio(self.prices, fast_period)
        self.slow__trend = TrendRatio(self.prices, slow_period)

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
        inst['names'] = []
        names = inst['names']
        inst['datas'] = []
        datas = inst['datas']
        names.append('singal')
        signal = self.macd.getSignal()
        signal_dated_data = dated_data(signal.getDateTimes(), signal.getValues())
        datas.append(signal_dated_data.save())
        names.append('hist')
        hist = self.macd.getHistogram()
        hist_dated_data = dated_data(hist.getDateTimes(), hist.getValues())
        datas.append(hist_dated_data.save())
        inst['vol'] = dated_data(self.vol.getDateTimes(),self.vol.getValues()).save()

        return inst
