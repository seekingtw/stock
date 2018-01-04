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
from pyalgotrade.technical import bollinger
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

class bband_signal(baseSignal):
    def __init__(self,strategy,feed, instrument, bBandsPeriod):
        super(bband_signal, self).__init__(strategy, feed, instrument)
        self.__position = None#remove later
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)
        self.__trend = TrendRatio(self.prices,20)
        self.plot_init(True)
    def list_info(self,name, list,times):
        sys.stdout.write(name+":")
        for i in range(-1,-1-times,-1):
            sys.stdout.write(str(list[i]))
            sys.stdout.write(" ")
        sys.stdout.write("\n")
        pass
    def getBollingerBands(self):
        return self.__bbands

    def long(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        ma=  self.getBollingerBands().getMiddleBand()
        low = self.__bbands.getLowerBand()
        high=self.__bbands.getUpperBand()
        if lower is None:
            return False
        if cross.cross_above(self.prices, self.__bbands.getLowerBand()) and self.__trend.trend_current_ratio() >=0:
        #if  cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and self.__trend.trend_current() != 'down':
        #if  cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and trend_ratio(ma) >-1:
        #if cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and prices[-1] - prices[-3] > 0:
        #if cross.cross_above(self.__prices, self.__bbands.getLowerBand()) :#and prices[-1] - prices[-5] > 0:
        #if bars[self.__instrument].getClose() < lower:
            #if cross.cross_above(self.__prices,self.__bbands.getLowerBand() ):
            #if self.getBollingerBands().getMiddleBand()[-1-1] and   (self.getBollingerBands().getMiddleBand()[-1] -  self.getBollingerBands().getMiddleBand()[-1-1] ) > 0 :# add trade
            #print ("ma",ma[-1],ma[-2],ma[-3])
            #print ("low",low[-1],low[-2],low[-3])
            #print ("high",high[-1],high[-2],high[-3])
            #print ("price",prices[-1],prices[-2],prices[-3])
            print bars.getDateTime()
            self.list_info("ma",ma,5)
            self.list_info("low", low, 5)
            self.list_info("high", high, 5)
            self.list_info("price", self.prices, 5)
            return True
        return False
        pass
    def short(self,bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        prices = self.prices
        if upper is None:
            return False
        # if bars[self.__instrument].getClose() > upper:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()):
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or treand_check(prices) <= -1:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or  self.__trend.trend_current() == 'down':
        if cross.cross_below(self.prices, self.__bbands.getUpperBand()) or self.__trend.trend_current_ratio() < 0:
            return True
        return False

    def plot_init(self, plot):
        if plot:  # plot:
            super(bband_signal, self).plot_init(plot)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("upper",
                                                                           self.getBollingerBands().getUpperBand())
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("middle",
                                                                           self.getBollingerBands().getMiddleBand())
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("lower",
                                                                           self.getBollingerBands().getLowerBand())
           # self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)

        pass


    def plot_show(self):
        self.plt.plot()
        pass

