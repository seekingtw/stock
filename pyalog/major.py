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
from kd import *
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
import sma_crossover
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
   # strat.attach_strategy(kd_signal(strat,feed,instrument,9,3))
    strat.attach_strategy(bband_signal(strat,feed,instrument,20))
    '''
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    maxdrawdown = drawdown.DrawDown()
    strat.attachAnalyzer(maxdrawdown)
    '''
    #retAnalyzer = returns.Returns()
    #strat.attachAnalyzer(retAnalyzer)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    drawDownAnalyzer = drawdown.DrawDown()
    strat.attachAnalyzer(drawDownAnalyzer)
    tradesAnalyzer = trades.Trades()
    strat.attachAnalyzer(tradesAnalyzer)

    strat.run()
    #print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    #drawDownAnalyzer = drawdown.DrawDown()
    #strat.attachAnalyzer(drawDownAnalyzer)
    #tradesAnalyzer = trades.Trades()
    #strat.attachAnalyzer(tradesAnalyzer)
    #section_ana.show()

    print ("drawback check")
    strat.check()
    strat.plot()

    print "Final portfolio value: $%.2f" % strat.getResult()
    #print "Cumulative returns: %.2f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100)
    print "Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05))
    print "Max. drawdown: %.2f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100)
    print "Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration())

    print
    print "Total trades: %d" % (tradesAnalyzer.getCount())
    if tradesAnalyzer.getCount() > 0:
        profits = tradesAnalyzer.getAll()
        print "Avg. profit: $%2.f" % (profits.mean())
        print "Profits std. dev.: $%2.f" % (profits.std())
        print "Max. profit: $%2.f" % (profits.max())
        print "Min. profit: $%2.f" % (profits.min())
        #returns = tradesAnalyzer.getAllReturns()
        #print "Avg. return: %2.f %%" % (returns.mean() * 100)
        #print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
        #print "Max. return: %2.f %%" % (returns.max() * 100)
        #print "Min. return: %2.f %%" % (returns.min() * 100)

    print
    print "Profitable trades: %d" % (tradesAnalyzer.getProfitableCount())
    if tradesAnalyzer.getProfitableCount() > 0:
        profits = tradesAnalyzer.getProfits()
        print "Avg. profit: $%2.f" % (profits.mean())
        print "Profits std. dev.: $%2.f" % (profits.std())
        print "Max. profit: $%2.f" % (profits.max())
        print "Min. profit: $%2.f" % (profits.min())
        #returns = tradesAnalyzer.getPositiveReturns()
        #print "Avg. return: %2.f %%" % (returns.mean() * 100)
        #print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
        #print "Max. return: %2.f %%" % (returns.max() * 100)
        #print "Min. return: %2.f %%" % (returns.min() * 100)

    print
    print "Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount())
    if tradesAnalyzer.getUnprofitableCount() > 0:
        losses = tradesAnalyzer.getLosses()
        print "Avg. loss: $%2.f" % (losses.mean())
        print "Losses std. dev.: $%2.f" % (losses.std())
        print "Max. loss: $%2.f" % (losses.min())
        print "Min. loss: $%2.f" % (losses.max())
        #returns = tradesAnalyzer.getNegativeReturns()
        #print "Avg. return: %2.f %%" % (returns.mean() * 100)
        #print "Returns std. dev.: %2.f %%" % (returns.std() * 100)
        #print "Max. return: %2.f %%" % (returns.max() * 100)
        #print "Min. return: %2.f %%" % (returns.min() * 100)

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
