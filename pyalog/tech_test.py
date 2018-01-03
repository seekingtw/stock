import sys
#sys.path.append("pyalgotrade-develop")
from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import quandl
from pyalgotrade.technical import bollinger
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade import broker as basebroker
from pyalgotrade import plotter
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from trend import *
class baseSignal:
    def __init__(self):
        pass
    def long_signal(self):
        pass
    def short_signal(self):
        pass
    def is_long(self):
        pass
    def is_short(self):
        pass
'''
def treand_check(list):
    if len(list) > 20:
        max_pre = max(list[-1-19:-1+5-19])
        max_now = max(list[-5:])
        if max_pre == None or max_now == None:
            return -1
        print ("max now ", max_now," max prev" , max_pre," ratio ",(max_now-max_pre)/max_pre)
        if (max_now - max_pre)/max_pre  >0.05:
            return 1
        elif  (max_now - max_pre)/max_pre  <0:
            return -1
        elif  (max_now - max_pre)/max_pre  <-0.05:
            return -2
        else :
            return 0
    else:
        return 0

'''


class BBand_strategy(baseSignal):
    def __init__(self, strategy,feed, instrument, bBandsPeriod):
        self.__instrument = instrument
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__position = None#remove later
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)
        #self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 1)
        self.__strategy= strategy
        self.__trend = TrendRatio(self.__prices,20)
        self.plot_init(True)
    def getBollingerBands(self):
        return self.__bbands

    def onOrderUpdated(self, order):
        if order.isBuy():
            orderType = "Buy"
        else:
            orderType = "Sell"
        self.info("%s order %d updated - Status: %s" % (
            orderType, order.getId(), basebroker.Order.State.toString(order.getState())
        ))
        #self.info("%d positions, %d values" %(self.__position.getShares() ,self.getBroker().getEquity()) )
    import sys
    def list_info(self,name, list,times):
        sys.stdout.write(name+":")
        for i in range(-1,-1-times,-1):
            sys.stdout.write(str(list[i]))
            sys.stdout.write(" ")
        sys.stdout.write("\n")
        pass
    def long(self, bars):
        global list_info
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        ma=  self.getBollingerBands().getMiddleBand()
        low = self.__bbands.getLowerBand()
        high=self.__bbands.getUpperBand()
        prices=self.__prices
        if lower is None:
            return False
        if cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and self.__trend.trend_current_ratio() >=0:
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
            self.list_info("price", prices, 5)
            return True
        return False
        # Check if we have to exit the position.

    def long2(self, bars):
        global list_info
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        ma=  self.getBollingerBands().getMiddleBand()
        low = self.__bbands.getLowerBand()
        high=self.__bbands.getUpperBand()
        prices=self.__prices
        if lower is None:
            return False
        if cross.cross_above(self.__prices, ma) and self.__trend.trend_current_ratio() >=0:
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
            self.list_info("price", prices, 5)
            return True
        return False
        # Check if we have to exit the position.

    def short(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        prices = self.__prices
        if upper is None:
            return False
        #if bars[self.__instrument].getClose() > upper:
        #if cross.cross_below(self.__prices, self.__bbands.getUpperBand()):
        #if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or treand_check(prices) <= -1:
        #if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or  self.__trend.trend_current() == 'down':
        if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or self.__trend.trend_current_ratio() < 0 :
            return True
        return False


    def plot_init(self, plot):
        if plot:  # plot:
            self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("upper", self.getBollingerBands().getUpperBand())
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("middle",
                                                                           self.getBollingerBands().getMiddleBand())
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("lower", self.getBollingerBands().getLowerBand())
            self.plt.getOrCreateSubplot("trend").addDataSeries("tend", self.__trend.getTrend())
        pass


    def plot_show(self):
        self.plt.plot()
        pass

'''
    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and bar.getClose() < lower:
            sharesToBuy = int(self.getBroker().getCash(False) / bar.getClose())
            self.info("Placing buy market order for %s shares" % sharesToBuy)
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > upper:
            self.info("Placing sell market order for %s shares" % shares)
            self.marketOrder(self.__instrument, -1*shares)
'''



