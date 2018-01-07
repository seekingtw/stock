import sys
sys.path.append("pyalgotrade-develop")

from pyalgotrade import strategy
import trade_report
from trade_report import trade_report
from factor.mdd import mdd
import datetime

class StrategyManager(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument,section_analyzer,prefix='',postfix='', **kwargs):
        ''' '''
        super(StrategyManager, self).__init__(feed)
        self.__position = None
        self.strategys= []
        self.__instrument = instrument
        self.analyzers= []

        #self.strategys.append(MA_Stragtegy(feed,instrument,5))
        self.section_analyzer = section_analyzer
        self.report = trade_report(prefix+str(instrument)+postfix)
        self.mdd_obj = mdd()

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
        self.section_analyzer.analyze()
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
        price = bars[self.__instrument].getPrice()
        for strategy in self.strategys:
            #handle signal
            # judge signal

            if self.__position is None:

                #if strategy.long(bars):
                if strategy.long_signal():
                    shares = int(1000 / bars[self.__instrument].getPrice())
                    #shares = int(self.getBroker().getEquity() / bars[self.__instrument].getPrice())
                    self.__position = self.enterLong(self.__instrument, shares, True)
                    self.section_analyzer.item(bars.getDateTime(), "long", self.getBroker().getEquity(),
                                               self.walkaround_share(shares), price, shares)
                    pass
            #elif not self.__position.exitActive() and strategy.short(bars):
            elif not self.__position.exitActive() and strategy.short_signal() :
                self.__position.exitMarket()
                self.section_analyzer.item(bars.getDateTime(), "long_exit", self.getBroker().getEquity(), 0, price, 0)
        pass

        ''' for analyze, notice that currently position is position'''
        self.mdd_obj.update_by_position(price ,self.__position)

    def get_mdds(self):
        return self.mdd_obj.get_drawdowns()
    pass

    def save(self):
        self.report.add('max drawdown', self.mdd_obj.save())
        self.report.add('trade', self.section_analyzer.save())
        for each in self.strategys:
            self.report.add('trend',each.save())
        self.report.save()


from pyalgotrade.barfeed import googlefeed

from factor.trades import section_analyzer
#from bband import *
#from signal.bband2 import *
from signals.macd import *
from  signals.bband2 import *
from  signals.kd import *
from  signals.ma import *
from signals.rsi import rsi_signal
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades


def main(plot):
    test_string=""
    #code = compile(test_string, 'user_strategy.py', 'exec')
    #exec(code)
    checknamespace={}
    #execfile('user_strategy.py', checknamespace)
    #execfile('bband_strategy.py',checknamespace)
    #user_strategy = b
    instrument = '1102'
    #instrument='1102'
    #instrument='1301'
    #instrument='1303'
    output_prefix="report-"
    #output_postfix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    output_prefix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M-")

    csvfile="tw50_test/"+instrument+'.csv'
    feed = googlefeed.Feed()
    #feed.addBarsFromCSV(instrument,"2030.csv")

    #feed.setBarFilter(DateRangeFilter(       datetime.strptime("2015-11-1","%Y-%m-%d"),         datetime.strptime("2016-2-1","%Y-%m-%d")))
    feed.addBarsFromCSV(instrument, csvfile)
    #execfile('bband_strategy.py',checknamespace)
    #StrategyManager= checknamespace['BBands']
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana,output_prefix)
    #strat.attach_strategy(DMA_signal(strat,feed,instrument,20,60))
    #strat.attach_strategy(macd_signal(strat,feed,instrument,12,26,9))
    #strat.attach_strategy(trend_signal(strat,feed,instrument,20))
    #strat.attach_strategy(kd_signal(strat,feed,instrument,9,3))
    #strat.attach_strategy(bband_signal(strat,feed,instrument,20))
    strat.attach_strategy(rsi_signal(strat,feed,instrument,10))
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
    #drawDownAnalyzer.getMaxDrawDown2(strat, feed)
    strat.run()
    #print "Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05)
    #drawDownAnalyzer = drawdown.DrawDown()
    #strat.attachAnalyzer(drawDownAnalyzer)
    #tradesAnalyzer = trades.Trades()
    #strat.attachAnalyzer(tradesAnalyzer)
    #section_ana.show()
    print ("drawback check")
    strat.check()
    strat.save()
    #report = trade_report.load('1234.pickle')
    #report.view()


    #list1=  strat.get_mdds()
    #print list1
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
    #for each in strat.get_mdds:

    pass


if __name__ == "__main__":
    main(True)
