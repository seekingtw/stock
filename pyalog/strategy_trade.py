import sys
sys.path.append("pyalgotrade-develop")

from pyalgotrade import strategy
import trade_report
from trade_report import trade_report
from factor.mdd import mdd
import datetime

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

        self.mdd_obj = mdd()
        # for example usage of sd
        #self.__asset =dataseries.SequenceDataSeries(365*10)

        pass
    def crate_report (self,prefix='',postfix=''):
        self.report = trade_report(prefix+str(self.__instrument)+postfix)
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
                    shares = int(self.getBroker().getEquity()*0.9 / bars[self.__instrument].getPrice())
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
        self.mdd_obj.update_by_position(self.getBroker().getEquity() ,self.__position)
        #        self.__asset.appendWithDateTime(bars.getDateTime(),self.getBroker().getEquity()+100000)

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
from  signals.bband import *
from  signals.kd import *
from  signals.ma import *
from signals.rsi import rsi_signal
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

def run(feed,instrument,signal,signal_parameter,signal_name,output_prefix,output_postfix,plot = False):
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana)
    strat.attach_strategy(signal(strat,feed,instrument,**signal_parameter))

    output_postfix = signal_name
    strat.crate_report(output_prefix,output_postfix)
    strat.run()
    print ("drawback check")
    strat.get_mdds()
    strat.check()
    strat.save()
    strat.mdd_obj.view()


    #list1=  strat.get_mdds()
    #print list1
    if plot : strat.plot()
    pass

def opt_gen_list():
    #read fine
    #gen opt_list
    pass
def run_optimize(feed,instrument):
    opt_list = opt_gen_list()

    #opt_run()
    for each in range(opt_list):
        print each," loop in ",len(opt_list)," loops"
        (signal,signal_parameter,signal_name,output_prefix,output_postfix) = opt_list[each]
        run(feed,instrument,signal,signal_parameter,signal_name,output_prefix,output_postfix)


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
    instrument='1301'
    #instrument='1303'
    output_prefix="report-"
    #output_postfix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    output_postfix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M-")
    #strat.attach_strategy(DMA_signal(strat,feed,instrument,20,60))
    #strat.attach_strategy(macd_signal(strat,feed,instrument,12,26,9))
    #strat.attach_strategy(trend_signal(strat,feed,instrument,20))
    #strat.attach_strategy(kd_signal(strat,feed,instrument,9,3))
    #strat.attach_strategy(bband_signal(strat,feed,instrument,20))
    #strat.attach_strategy(rsi_signal(strat,feed,instrument,10))
    csvfile="tw50_test/"+instrument+'.csv'
    feed = googlefeed.Feed()
    feed.addBarsFromCSV(instrument, csvfile)
    '''
    signal_name = 'bband'
    signal_parameter= {'period':20,'std':2}

    signal_name = 'rsi'
    signal_parameter = {'period': 5}
    '''
    signal_name = 'kd'
    signal_parameter = {'fast_period': 10, 'slow_period': 3}
    '''
    signal_name = 'macd'
    signal_parameter = {'fast_period': 12, 'slow_period': 26, 'signal_period': 9}
    signal_name = 'dma'
    signal_parameter = {'fast_period': 5, 'slow_period': 20}
    signal_name = 'trend'
    signal_parameter = { 'period': 5}
    '''

#singal_parameter= {'slow_period':20,'fast_period':5}
    #feed.addBarsFromCSV(instrument,"2030.csv")
    strategy_dict={'dma':DMA_signal,
                   'macd':macd_signal,
                   'trend':trend_signal,
                   'kd':kd_signal,
                   'bband':bband_signal,
                   'rsi':rsi_signal}
    signal= strategy_dict[signal_name]
    #feed.setBarFilter(DateRangeFilter(       datetime.strptime("2015-11-1","%Y-%m-%d"),         datetime.strptime("2016-2-1","%Y-%m-%d")))
    #execfile('bband_strategy.py',checknamespace)
    '''
    for i in range(3,22+1):
        csvfile = "tw50_test/" + instrument + '.csv'
        feed = googlefeed.Feed()
        feed.addBarsFromCSV(instrument, csvfile)
        signal_parameter['period'] = i
        output_prefix= "result/"+signal_name+"/p"+str(i)+"-"
        run(feed, instrument, signal, signal_parameter, signal_name, output_prefix, output_postfix)
    '''

    run(feed, instrument,signal,signal_parameter,signal_name,output_prefix,output_postfix,plot= True)

    '''
    section_ana = section_analyzer()
    strat = StrategyManager(feed, instrument,section_ana)
    strat.attach_strategy(signal(strat,feed,instrument,**signal_parameter))
    output_postfix = signal_name
    strat.crate_report(output_prefix,output_postfix)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    maxdrawdown = drawdown.DrawDown()
    strat.attachAnalyzer(maxdrawdown)

    #retAnalyzer = returns.Returns()
    #strat.attachAnalyzer(retAnalyzer)
    #sharpeRatioAnalyzer = sharpe.SharpeRatio()
    #strat.attachAnalyzer(sharpeRatioAnalyzer)
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
    #list1=  strat.get_mdds()
    #print list1
    strat.plot()
    '''



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
