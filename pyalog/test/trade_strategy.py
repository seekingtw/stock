import sys
sys.path.append("pyalgotrade-develop")

from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross
from pyalgotrade import dataseries
from Record import Record
from trade_report import trade_report


'''base strage'''

class baseStrategy:
    def __init__(self):
        pass
    def long_signal(self):
        pass
    def short_signal(self):
        pass
    def is_long(self):
        pass
    def is_short(self):
        pass

from pyalgotrade.technical import ma

class MA_Stragtegy(baseStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        self.__instrument = instrument
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__position = None#remove later
        pass
    def long_signal(self,time):
        if cross.cross_above(self.__prices, self.__sma) > 0:
            return True
        else:
            return False
        pass
    def short_signal(self,time):
        if cross.cross_below(self.__prices, self.__sma) > 0:
            return True
        else:
            return False
        pass
    def is_long(self,time):
        if cross.cross_above(self.__prices, self.__sma) > 0:
            return True
        else:
            return False
        pass
        pass
    def is_short(self,time):
        if cross.cross_below(self.__prices, self.__sma) > 0:
            return True
        else:
            return False
        pass

    def long(self,bars):
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0:
                #shares = int(self.getBroker().getCash() * 0.9 / bars[self.__instrument].getPrice())
                cur_price = bars[self.__instrument].getPrice()
                # Enter a buy market order. The order is good till canceled.
                #self.__position = self.enterLong(self.__instrument, shares, True)
                return True
        return False
          # Check if we have to exit the position.

    def short(self,bars):
            if  cross.cross_below(self.__prices, self.__sma) > 0:
            #self.record.record({"date": bars.getDateTime()}, {"type": "exit"})
                #self.__position.exitMarket()
                return True
            return False