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
from pyalgotrade.technical import atr
from factor.dated_datas import *
from signals import baseSignal
import pandas as pd
class atr_signal(baseSignal,object):
    def __init__(self, strategy, feed, instrument, **kwargs):

        super(atr_signal, self).__init__(strategy, feed, instrument)
        self.set_member('period',20,kwargs)
        self.atr= atr.ATR(feed[instrument],self.period)
        self.plot_init(True)
        pass

    def plot_init(self, plot):
        if plot:  # plot:
            super(atr_signal, self).plot_init(plot)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("atr",
                                                                         self.atr)
        pass

    def long(self,bars):
        if self.atr[-1] >0.5:
            return True
        return False
        pass

    def short(self,bars):

        if self.atr[-1] < 0.0:

            return True
        return False
        pass

    def long_signal(self):
        if self.atr[-1] >0.0:
            return True
        return False
        pass

    def short_signal(self):

        if self.atr[-1] < 0.0:

            return True
        return False



    def plot_init(self, plot):
        if plot:  # plot:
            super(atr_signal, self).plot_init(plot)
           # self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getOrCreateSubplot("atr").addDataSeries("atr", self.atr)


        pass
    def save(self):
        inst = {}

        data_pd = pd.DataFrame()
        data_pd['atr'] = self.atr.getValues()
        data_pd.index = self.atr.getDateTimes()
        inst['atr'] = data_pd

        # inst['vol'] = dated_data(self.vol.getDateTimes(),self.vol.getValues()).save_dataframe()
        data_pd = pd.DataFrame()
        data_pd['vol'] = self.vol.getValues()
        data_pd.index = self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd = pd.DataFrame()
        data_pd['prices'] = self.prices.getValues()
        data_pd.index = self.prices.getDateTimes()
        inst['prices'] = data_pd
        return inst
        # return data_pd

    def plot_show(self):
        self.plt.plot()
        pass