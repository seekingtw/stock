# -*- coding: utf-8 -*-
'''
create by Jianhao Su
'''
import sys
sys.path.append("pyalgotrade-develop")

from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from Record import *


class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.record = Record()

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # If a position was not opened, check if we should enter a long position.
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                cur_price= bars[self.__instrument].getPrice()
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
               # self.record.record({'type':"long"},{"share":shares},{"price":cur_price})
                self.record.record_order(bars.getDateTime(),"long",shares,cur_price)
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.record.record({"date":bars.getDateTime()},{"type":"exit"})
            self.__position.exitMarket()
            
#import sma_crossover
from pyalgotrade import plotter
from pyalgotrade.tools import googlefinance
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.barfeed import googlefeed


def main(plot):

    smaPeriod = 5
    '''
    #Download the bars.
    instrument = 'aapl'
    feed = googlefinance.download_daily_bars('aapl',2010,'2030.csv')
    feed = googlefinance.build_feed([instrument],2015,2016,'aapl.csv')
    '''
    # Get from local file
    instrument = '2030'
    feed = googlefeed.Feed()
    feed.addBarsFromCSV(instrument,"2030.csv")


    strat = SMACrossOver(feed, instrument, smaPeriod)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strat, True, False, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())

    strat.run()
    print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    strat.record.save()
    if plot:
        plt.plot()
 


if __name__ == "__main__":
    main(True)
    
