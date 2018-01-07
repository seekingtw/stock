from pyalgotrade import plotter
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

def hello():
    print "hello"
    pass
