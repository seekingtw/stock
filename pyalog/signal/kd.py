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
from pyalgotrade.technical import stoch
from trend import *

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

class kd_signal(baseSignal):
    def __init__(self,strategy,feed, instrument,fast_period,slow_period):
        super(kd_signal, self).__init__(strategy, feed, instrument)
        self.fast_ma= ma.SMA(feed[instrument].getCloseDataSeries(), fast_period)
        self.fast_period = fast_period

        self.slow_ma = ma.SMA(feed[instrument].getCloseDataSeries(), slow_period)
        self.slow_period = slow_period
        self.fast__trend = TrendRatio(self.prices, fast_period)
        self.slow__trend = TrendRatio(self.prices, slow_period)
        self.kd = stoch.StochasticOscillator(feed[instrument],9,3,False,None)

        self.plot_init(True)

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

