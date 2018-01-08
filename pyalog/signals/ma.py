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
class DMA_signal(baseSignal,object):
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
        super(DMA_signal, self).__init__(strategy, feed, instrument)
        self.fast_ma= ma.SMA(feed[instrument].getCloseDataSeries(), fast_period)
        self.fast_period = fast_period

        self.slow_ma = ma.SMA(feed[instrument].getCloseDataSeries(), slow_period)
        self.slow_period = slow_period
        #self.__strategy= strategy
        #self.__instrument = instrument
        #self.__prices = feed[instrument].getPriceDataSeries()
        self.fast__trend = TrendRatio(self.prices, fast_period)
        self.slow__trend = TrendRatio(self.prices, slow_period)

        self.plot_init(True)

    def long_signal(self):
        if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
            return True
        return False
        pass
    def short_signal(self):
        if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
            return True
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
            super(DMA_signal, self).plot_init(plot)
            #self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("fast_ma", self.fast_ma)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("slow_ma",
                                                                           self.slow_ma)
            self.plt.getOrCreateSubplot("trend").addDataSeries("fast", self.fast__trend.getTrend())
            self.plt.getOrCreateSubplot("trend").addDataSeries("slow", self.slow__trend.getTrend())

        pass
    def save(self):
        inst = {}
        inst['names'] = []
        names = inst['names']
        inst['datas'] = []
        datas = inst['datas']
        names.append('fast_ma')
        fast_ma = self.fast_ma
        fast_ma_dated_data = dated_data(fast_ma.getDateTimes(), fast_ma.getValues())
        datas.append(fast_ma_dated_data.save())
        names.append('slow_ma')
        slow_ma = self.slow_ma
        slow_ma_dated_data = dated_data(slow_ma.getDateTimes(), slow_ma.getValues())
        datas.append(slow_ma_dated_data.save())
        price_dated_data= dated_data(self.prices.getDateTimes(),self.prices.getValues())
        datas.append(price_dated_data.save())
        names.append('price')
        inst['vol'] = dated_data(self.vol.getDateTimes(),self.vol.getValues()).save()

        return inst

    def plot_show(self):
        self.plt.plot()
        pass
