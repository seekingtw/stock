
__metaclass__ = type
import sys

sys.path.append("pyalgotrade-develop")
from pyalgotrade import dataseries
from pyalgotrade.technical import ma
from pyalgotrade import plotter
from  factor.dated_datas  import dated_data
import pandas as pd

def average(list):
    try:
        sum(list)
    except:
        return None
    return sum(list)/float(len(list))

def trend_ratio(list,period=20, interval= 5,div=4):
    val = None
    if len(list) > period:
        time_internal = period/div
        avg_prev = average(list[-1-period:-1-(period*(div-1)/div)])
        avg_now = average(list[-1-period/div:])
        if  avg_prev == None:
            val =  None
        else:
            ratio = lambda now,prev: (now-prev)/prev*100/interval
            val = ratio(avg_now, avg_prev)
        #print ("avg now ", avg_now," avg prev" , avg_prev," ratio ",ratio(avg_now,avg_prev))


    else:
        val =  None
    #print ("avg now ", avg_now, " avg prev", avg_prev, " ratio ", val)

    return val


class TrendRatio(object):
    def __init__(self,dataSeries, period, div=4,interval=5):
        self.ma= ma.SMA(dataSeries, period)
        self.period = period
        self.div=div
        self.interval =interval
        dataSeries.getNewValueEvent().subscribe(self.__onNewValue)
        self.trend_data = dataseries.SequenceDataSeries()

    def __onNewValue(self, dataSeries, dateTime, value):
        trend_val = None

        if value is not None:
            try :
                if self.ma[-1-self.period] is not None:
                    trend_val = trend_ratio(self.ma,self.period,self.interval,self.div)
            except:
                trend_val = None
                pass
        #if trend_val == None :
        #    trend_val = -100
        self.trend_data.appendWithDateTime(dateTime, trend_val)
    def getTrend(self):
        return self.trend_data


    def plot_init(self, strategy,plot=True):
        self.__strategy = strategy

        if plot:  # plot:
            self.plt = plotter.StrategyPlotter(self.__strategy, True, True, True)
            self.plt.getOrCreateSubplot("trend").addDataSeries("trend", self.trend_data)
        pass


    def plot_show(self):
        self.plt.plot()
        pass

    def trend_type(self,date):
        pass
    def trend_current(self, up_scale=1, down_scale=-1):

        if self.trend_data[-1] > up_scale:
            return 'up'
        if self.trend_data[-1]  < down_scale:
            return 'down'
        if self.trend_data[-1] <= up_scale and self.trend_data[-1] >= down_scale:
            return 'normal'

    def trend_current_ratio(self, up_scale=1, down_scale=-1):

        return  self.trend_data[-1]

from signals import baseSignal
class trend_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument,**kwargs):
        '''

        :param strategy:
        :param feed:
        :param instrument:
        :param period:
        :param kwargs:
         period
        '''
        #super(trend_signal,self).__init__(strategy,feed,instrument)
        #self.__strategy= strategy
        #self.__instrument = instrument
        #self.__prices = feed[instrument].getPriceDataSeries()
        #super(trend_signal, self).__init__(strategy, feed, instrument)
        #print type(trend_signal)
        self.set_member('period',20,kwargs)
        super(trend_signal,self).__init__(strategy, feed, instrument)
        self.trend = TrendRatio(self.prices, self.period)
        self.plot_init(True)

    def long(self,bars):
        if self.trend.trend_current_ratio() >0.0:
            return True
        return False
        pass

    def short(self,bars):

        if self.trend.trend_current_ratio() < 0:

            return True
        return False
        pass

    def long_signal(self):
        if self.trend.trend_current_ratio() >0.0:
            return True
        return False
        pass

    def short_signal(self):

        if self.trend.trend_current_ratio() < 0:

            return True
        return False
        pass
    def save(self):
        inst = {}
        '''
        inst['names'] = []
        names = inst['names']
        inst['datas'] = []
        datas = inst['datas']
        names.append('moment')
        trend = self.trend
        trend_dated_data = dated_data(trend.getDateTimes(), trend.getValues())
        datas.append(trend_dated_data.save())
        '''

        data_pd= pd.DataFrame()
        data_pd['trend']= self.trend.getTrend().getValues()
        data_pd.index= self.trend.getTrend().getDateTimes()
        inst['trend']= data_pd

        data_pd= pd.DataFrame()
        data_pd['vol']= self.vol.getValues()
        data_pd.index= self.vol.getDateTimes()
        inst['vol'] = data_pd
        data_pd= pd.DataFrame()
        data_pd['prices']= self.prices.getValues()
        data_pd.index= self.prices.getDateTimes()
        inst['prices'] = data_pd
        return inst

    def plot_init(self, plot):
        if plot:  # plot:
            super(trend_signal,self).plot_init(plot)
            #self.plt = plotter.StrategyPlotter(self.strategy, True, True, True)
            # self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("fast_ma", self.fast_ma)
            # self.plt.getInstrumentSubplot(self.__instrument).addDataSeries("slow_ma",
            #                                                               self.slow_ma)

            self.plt.getOrCreateSubplot("macd").addDataSeries("trend", self.trend.getTrend())

        pass


    def plot_show(self):
        self.plt.plot()
        pass
