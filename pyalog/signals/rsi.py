#__metaclass__ = type
import sys

sys.path.append("pyalgotrade-develop")
from signals import baseSignal
from signals.trend import TrendRatio
from factor.dated_datas import  dated_data
from pyalgotrade.technical.rsi import RSI
from pyalgotrade import plotter
'''
class baseSignal:
    def __init__(self,strategy,feed, instrument):
        self.strategy = strategy
        self.instrument = instrument
        self.prices = feed[instrument].getPriceDataSeries()
        self.vol = feed[instrument].getVolumeDataSeries()
        #self.plot_init(True)
        pass
    def long_signal(self):
        pass
    def short_signal(self):
        pass
    def is_long(self):
        pass
    def is_short(self):
        pass


    def plot_init(self, plot):
        if plot:  # plot:
            self.plt = plotter.StrategyPlotter(self.strategy, True, True, True)
            self.plt.getOrCreateSubplot("vol").addDataSeries("vol", self.vol)
        pass


    def plot_show(self):
        self.plt.plot()
        pass
'''
class rsi_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,period):
        super(rsi_signal, self).__init__(strategy, feed, instrument)
        self.rsi= RSI(feed[instrument].getCloseDataSeries(), period)
        self.vol=feed[instrument].getVolumeDataSeries()
        self.trend = TrendRatio(self.prices, period)
        self.plot_init(True)

    def long_signal(self):
        # if cross.cross_above(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:
        #    return True
        if  self.rsi[-1] <= 20: # and self.slow__trend.trend_current_ratio() >=0:
            return True
        return False
        pass


    def short_signal(self):
        # if cross.cross_below(self.fast_ma, self.slow_ma) :#and self.__trend.trend_current_ratio() >=0:

        if self.rsi[-1] > 80:  # and self.macd.getSignal()[-1] < 0:
            # if (self.macd.getHistogram()[-1] < 0 and self.macd.getHistogram()[-2] >= 0 )or self.slow__trend.trend_current_ratio() < 0:
            return True
        return False
        pass


    def save(self):
        inst = {}
        inst['names'] = []
        names = inst['names']
        inst['datas'] = []
        datas = inst['datas']
        names.append('rsi')
        rsi = self.rsi
        rsi_dated_data = dated_data(rsi.getDateTimes(), rsi.getValues())
        datas.append(rsi_dated_data.save())
        return inst

    def plot_init(self, plot):
        if plot:  # plot:
            super(rsi_signal, self).plot_init(plot)
            self.plt.getOrCreateSubplot("rsi").addDataSeries("rsi", self.rsi)
        pass

    def plot_show(self):
        self.plt.plot()
        pass