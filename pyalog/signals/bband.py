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
from factor.dated_datas import *
from signals import baseSignal
import pandas as pd
class bband_signal(baseSignal,object):
    def __init__(self,strategy,feed, instrument, **kwargs):
        '''
        :param strategy:
        :param feed:
        :param instrument:
        :param bBandsPeriod: ##
        :param kwargs:
from signals import baseSignal
         std:
        '''
        super(bband_signal, self).__init__(strategy, feed, instrument)
        self.set_member('period',20,kwargs)
        self.set_member('std', 2, kwargs)
        self.__position = None#remove later
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), self.period, self.std)
        self.__trend = TrendRatio(self.prices,20)
        self.plot_init(True)
    def list_info(self,name, list,times):
        sys.stdout.write(name+":")
        for i in range(-1,-1-times,-1):
            sys.stdout.write(str(list[i]))
            sys.stdout.write(" ")
        sys.stdout.write("\n")
        pass
    def getBollingerBands(self):
        return self.__bbands
    def trend_long(self,ma):
        if  ma[-5] is  None:
            return  False

        if (ma[-1] -ma[-5])/ma[-5] > 0.0 :
            return True
        print "trend no long", (ma[-1] - ma[-5]) / ma[-5]
        return False
    def long_signal(self):
        #long signal is acceptable but need and trend
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        ma = self.getBollingerBands().getMiddleBand()
        low = self.__bbands.getLowerBand()
        high = self.__bbands.getUpperBand()
        if lower is None:
            return False
        check_point= False
        # example of acces datatimes
        #if self.prices.getDateTimes()[-1] :
        #    print self.prices[-1]
        if cross.cross_above(self.prices, self.__bbands.getLowerBand()) :
            #if self.trend_long(self.__bbands.getUpperBand()) :
            #if self.trend_long(ma):
            check_point = True
            '''
         ### remove failling edge
        if len(low) >5  and low[-5]!= None and check_point == True:
            check_point = False
            #print "bband long debug:",self.prices[-1],(low[-1] - low[-5])/low[-5]*100 , low[-5],low[-1]
            if (low[-1] - low[-5])/low[-5] >= -0.03:
                check_point = True
                pass

            '''
        if check_point == True:
            check_point = False
            if self.trend_long(self.__bbands.getUpperBand()) :
                check_point = True

        return check_point
    def trend_short(self,ma):

        if  ma[-5] is  None:
            return  False
        if (ma[-1] -ma[-5])/ma[-5] < -0.02 :
            return True
        return False
    def short_signal(self):
        # is trend is not long ... it is fail to generate this signal
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        prices = self.prices
        ma = self.getBollingerBands().getMiddleBand()
        if upper is None:
            return False
        # if bars[self.__instrument].getClose() > upper:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()):
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or treand_check(prices) <= -1:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or  self.__trend.trend_current() == 'down':
        #if cross.cross_below(self.prices, self.__bbands.getUpperBand()) :#or self.trend_short(ma) :
        if cross.cross_above(self.prices, self.__bbands.getUpperBand()):  # or self.trend_short(ma) :
            return True
        if self.trend_short(self.__bbands.getLowerBand()):  # or self.trend_short(ma) :
            return True
        return False

    def long(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        ma=  self.getBollingerBands().getMiddleBand()
        low = self.__bbands.getLowerBand()
        high=self.__bbands.getUpperBand()
        if lower is None:
            return False
        check_condition = False
        if cross.cross_above(self.prices, self.__bbands.getLowerBand()) :#and self.__trend.trend_current_ratio() >=0:
        #if  cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and self.__trend.trend_current() != 'down':
        #if  cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and trend_ratio(ma) >-1:
        #if cross.cross_above(self.__prices, self.__bbands.getLowerBand()) and prices[-1] - prices[-3] > 0:
        #if cross.cross_above(self.__prices, self.__bbands.getLowerBand()) :#and prices[-1] - prices[-5] > 0:
        #if bars[self.__instrument].getClose() < lower:
            #if cross.cross_above(self.__prices,self.__bbands.getLowerBand() ):
            #if self.getBollingerBands().getMiddleBand()[-1-1] and   (self.getBollingerBands().getMiddleBand()[-1] -  self.getBollingerBands().getMiddleBand()[-1-1] ) > 0 :# add trade
            #print ("ma",ma[-1],ma[-2],ma[-3])
            #print ("low",low[-1],low[-2],low[-3])
            #print ("high",high[-1],high[-2],high[-3])
            #print ("price",prices[-1],prices[-2],prices[-3])
            #print bars.getDateTime()
            #self.list_info("ma",ma,5)
            #self.list_info("low", low, 5)
            #self.list_info("high", high, 5)
            #self.list_info("price", self.prices, 5)
            check_condition = True
        if (check_condition == False):
                return False

        ### remove failling edge
        print "bband long debug:",(lower[-1] - lower[-5])/lower[-5] , lower[-5],lower[-1]
        if (lower[-1] - lower[-5])/lower[-5] >= -0.02:
            check_condition = True
        return check_condition
        pass
    def short(self,bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]

        prices = self.prices
        if upper is None:
            return False
        # if bars[self.__instrument].getClose() > upper:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()):
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or treand_check(prices) <= -1:
        # if cross.cross_below(self.__prices, self.__bbands.getUpperBand()) or  self.__trend.trend_current() == 'down':
        if cross.cross_below(self.prices, self.__bbands.getUpperBand()) or self.__trend.trend_current_ratio() < 0:
            return True
        return False

    def plot_init(self, plot):
        if plot:  # plot:
            super(bband_signal, self).plot_init(plot)
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("upper",
                                                                           self.getBollingerBands().getUpperBand())
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("middle",
                                                                           self.getBollingerBands().getMiddleBand())
            self.plt.getInstrumentSubplot(self.instrument).addDataSeries("lower",
                                                                           self.getBollingerBands().getLowerBand())
            self.plt.getOrCreateSubplot("trend").addDataSeries("trend", self.__trend.getTrend())

        pass

    def save(self):
        inst = {}
        '''
         inst['names'] = []
         names = inst['names']
         inst['datas'] = []
         datas= inst['datas']

        '''

        data_pd = pd.DataFrame()
        up = self.getBollingerBands().getUpperBand()
        mid = self.getBollingerBands().getMiddleBand()
        low = self.getBollingerBands().getLowerBand()

        data_pd['up'] = up.getValues()
        #names.append('up')
        data_pd['low'] = low.getValues()
        #names.append('up')
        data_pd['mid'] = mid.getValues()
        #names.append('mid')
        data_pd['price'] = self.prices.getValues()
        #names.append('price')
        data_pd.index = up.getDateTimes()

        '''
        up_dated_data= dated_data(up.getDateTimes(),up.getValues())
        datas.append(up_dated_data.save())
        names.append('middle')
        mid = self.getBollingerBands().getMiddleBand()
        mid_dated_data= dated_data(mid.getDateTimes(),mid.getValues())
        datas.append(mid_dated_data.save())
        names.append('lower')
        low = self.getBollingerBands().getLowerBand()
        low_dated_data= dated_data(low.getDateTimes(),low.getValues())
        datas.append(low_dated_data.save())
        price_dated_data= dated_data(self.prices.getDateTimes(),self.prices.getValues())
        datas.append(price_dated_data.save())
        names.append('price')
        '''
        inst['bband']=data_pd

        #inst['vol'] = dated_data(self.vol.getDateTimes(),self.vol.getValues()).save_dataframe()
        data_pd= pd.DataFrame()
        data_pd['vol']= self.vol.getValues()
        data_pd.index= self.vol.getDateTimes()
        inst['vol'] = data_pd
        return inst
        #return data_pd

    def plot_show(self):
        self.plt.plot()
        pass

'''

note:
for 1102, it is bad.
long signal : occur when failing :, signal may start before price rise, long term recover signal
short signal:acceptable ,short team long.

'''