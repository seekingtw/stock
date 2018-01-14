from pyalgotrade import plotter
import pandas as pd
class baseSignal:
    def __init__(self,strategy,feed, instrument):
        self.strategy = strategy
        self.instrument = instrument
        self.prices = feed[instrument].getPriceDataSeries()
        self.vol = feed[instrument].getVolumeDataSeries()
        #self.plot_init(True)
        pass
    def long_signal(self):
        pass
    def short_signal(self):
        pass
    def is_long(self):
        pass
    def is_short(self):
        pass
    def plot_init(self, plot):
        if plot:  # plot:
            self.plt = plotter.StrategyPlotter(self.strategy, True, True, True)
            self.plt.getOrCreateSubplot("vol").addDataSeries("vol", self.vol)
        pass

    def plot_show(self):
        self.plt.plot()
        pass
    def set_member(self,paramter,default,dict_args,member = None):
        if paramter in dict_args:
            if member == None:
                member=paramter
            self.__dict__[member] = dict_args[paramter]
        else:
            self.__dict__[member]=default

    def save(self):
        inst = {}

        data_pd = pd.DataFrame()
        data_pd['vol'] = self.vol.getValues()
        data_pd.index = self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd = pd.DataFrame()
        data_pd['prices'] = self.prices.getValues()
        data_pd.index = self.prices.getDateTimes()
        inst['prices'] = data_pd
        return inst

def hello():
    print "hello"
    pass
