import sys
sys.path.append("pyalgotrade-develop")
from trade_strategy import MA_Stragtegy
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import dataseries
from Record import Record
from trade_report import trade_report

from analysis import section_analyzer
class StrategyManager(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,section_analyzer, **kwargs):
        ''' '''
        super(StrategyManager, self).__init__(feed)
        self.__position = None
        self.strategys= []
        self.__instrument = instrument
        self.strategys.append(MA_Stragtegy(feed,instrument,5))
        self.section_analyzer = section_analyzer

        pass
    def attach_strategy(self, strategy):
        self.strategys.append(strategy)
        pass

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        for strategy in self.strategys:
            #handle signal
            # judge signal
            if self.__position is None :
                if strategy.long(bars) :
                    shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                    #cur_price = bars[self.__instrument].getPrice()
                    # Enter a buy market order. The order is good till canceled.
                    self.__position = self.enterLong(self.__instrument, shares, True)
                    self.section_analyzer.item(bars.getDateTime(), "long",self.getBroker().getEquity(),self.__position.getShares())
                pass
            elif not self.__position.exitActive() and strategy.short(bars) :
                self.__position.exitMarket()
                self.section_analyzer.item(bars.getDateTime(), "long_exit", self.getBroker().getEquity(),self.__position.getShares())
            pass
        pass
        #record

from pyalgotrade.barfeed import googlefeed
from pyalgotrade import plotter
from analysis import section_analyzer
def main(plot):
    instrument = '2030'
    feed = googlefeed.Feed()
    feed.addBarsFromCSV(instrument,"2030.csv")
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana)

    plt = plotter.StrategyPlotter(strat, True, True, True)
    strat.run()
    #plt.plot()
    section_ana.show()
    pass

if __name__ == "__main__":
    main(True)