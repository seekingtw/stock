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
class baseStrategy:
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


class BBand_strategy(baseStrategy):
    def __init__(self, strategy,feed, instrument, bBandsPeriod):
        self.__instrument = instrument
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__position = None#remove later
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)
        self.__strategy= strategy
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


    def long(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if lower is None:
            return False
        if bars[self.__instrument].getClose() < lower:
            return True
        return False
        # Check if we have to exit the position.


    def short(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        if upper is None:
            return False
        if bars[self.__instrument].getClose() > upper:
            return True
        return False


    def plot_init(self, plot):
        if plot:  # plot:
            self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("upper", self.getBollingerBands().getUpperBand())
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("middle",
                                                                           self.getBollingerBands().getMiddleBand())
            self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("lower", self.getBollingerBands().getLowerBand())
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
