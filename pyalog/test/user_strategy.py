import sys
sys.path.append("pyalgotrade-develop")
from trade_strategy import MA_Stragtegy
from pyalgotrade import strategy


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
    def walkaround_share(self,share):
        return self.__position.getShares() -share

    def onBars(self, bars):
        for strategy in self.strategys:
            #handle signal
            # judge signal
            price = bars[self.__instrument].getPrice()
            if self.__position is None :
                if strategy.long(bars) :

                    shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                    #cur_price = bars[self.__instrument].getPrice()
                    # Enter a buy market order. The order is good till canceled.
                    self.__position = self.enterLong(self.__instrument, shares, True)
                    self.section_analyzer.item(bars.getDateTime(), "long",self.getBroker().getEquity(),
                        self.walkaround_share(shares), price,shares )
                pass
            elif not self.__position.exitActive() and strategy.short(bars) :
                self.__position.exitMarket()
                self.section_analyzer.item(bars.getDateTime(), "long_exit", self.getBroker().getEquity(),0,price,0)
            pass
        pass
        #record