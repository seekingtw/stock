import sys
sys.path.append("pyalgotrade-develop")

from pyalgotrade import strategy
from trade_report import trade_report
from trade_report import trade_report

class StrategyManager(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,section_analyzer, **kwargs):
        ''' '''
        super(StrategyManager, self).__init__(feed)
        self.__position = None
        self.strategys= []
        self.__instrument = instrument
        self.analyzers= []

        #self.strategys.append(MA_Stragtegy(feed,instrument,5))
        self.section_analyzer = section_analyzer
        self.report = trade_report(str(instrument))

        pass
    def attach_strategy(self,strategy):
        self.strategys.append(strategy)
        pass
    def attach_analyzer(self,analyzer):
        self.analyzers.append(analyzer)
        pass

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("(%s)SELL at $%.2f" % (execInfo.getDateTime(), execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
    '''
    def onOrderUpdated(self, order):
        if order.isBuy():
            orderType = "Buy"
        else:
            orderType = "Sell"
        self.info("%s order %d updated - Status: %s" % (
            orderType, order.getId(), basebroker.Order.State.toString(order.getState())
        ))
    '''
    def check(self):
        self.section_analyzer.drawback_check()
    def save(self):
        for each in self.analyzers:
            each.save(str(self.__instrument))
    def plot(self):
        for each in self.strategys:
            each.plot_show()
    def walkaround_share(self, share):
        return self.__position.getShares() - share
    def onBars(self, bars):
        for strategy in self.strategys:
            #handle signal
            # judge signal
            price = bars[self.__instrument].getPrice()
            if self.__position is None:

                if strategy.long(bars):
                    shares = int(1000 / bars[self.__instrument].getPrice())
                    self.__position = self.enterLong(self.__instrument, shares, True)
                    self.section_analyzer.item(bars.getDateTime(), "long", self.getBroker().getEquity(),
                                               self.walkaround_share(shares), price, shares)
                    pass
            elif not self.__position.exitActive() and strategy.short(bars):
                self.__position.exitMarket()
                self.section_analyzer.item(bars.getDateTime(), "long_exit", self.getBroker().getEquity(), 0, price, 0)
        pass
    pass
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.barfeed import googlefeed
from analysis import section_analyzer
import sys

from analysis import section_analyzer
sys.path.append("signal")
#from bband import *
from bband2 import *
from ma import *
from macd import *
from trend import *
#from kd import *

def main(plot):
    test_string=""
    #code = compile(test_string, 'user_strategy.py', 'exec')
    #exec(code)
    checknamespace={}
    #execfile('user_strategy.py', checknamespace)
    #execfile('bband_strategy.py',checknamespace)
    #user_strategy = b
    instrument = '2030'
    feed = googlefeed.Feed()
    #feed.addBarsFromCSV(instrument,"2030.csv")
    feed.addBarsFromCSV(instrument,"tw50_test/1102.csv")
    #feed.setBarFilter(DateRangeFilter(       datetime.strptime("2015-11-1","%Y-%m-%d"),         datetime.strptime("2016-2-1","%Y-%m-%d")))
    #feed.addBarsFromCSV(instrument,"tw50_test/1102.csv")
    #feed.addBarsFromCSV(instrument,"tw50_test/1301.csv")
    #execfile('bband_strategy.py',checknamespace)
    #StrategyManager= checknamespace['BBands']
    bBandsPeriod = 40
    bBandsPeriod = 20
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana)
    #strat.attach_strategy(MA_Stragtegy(feed,instrument,5))
    #strat.attach_strategy(BBand_strategy(strat,feed,instrument,40))
    #strat.attach_strategy(bband2_signal(strat,feed,instrument,20))
    #strat.attach_strategy(DMA_signal(strat,feed,instrument,20,60))
    #strat.attach_strategy(macd_signal(strat,feed,instrument,12,26,9))
    #strat.attach_strategy(trend_signal(strat,feed,instrument,20))
    #strat.attach_strategy(kd_signal(strat,feed,instrument,9,3))
    strat.attach_strategy(bband_signal(strat,feed,instrument,20))

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    strat.run()
    print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    #section_ana.show()

    print ("drawback check")
    strat.check()
    strat.plot()

    '''
    execfile('user_strategy.py',checknamespace)
    StrategyManager= checknamespace['StrategyManager']
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana)

    plt = plotter.StrategyPlotter(strat, True, True, True)
    strat.run()
    #plt.plot()
    section_ana.show()
    '''
    pass

if __name__ == "__main__":
    main(True)
