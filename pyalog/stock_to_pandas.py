# -*- coding: utf-8 -*-

from twstock import Stock
import pandas 
import re

def stock_to_andas(stock):
    pd_stock=None
    #stock=Stock(stock_id)
    fields = ['date','capacity','turnover','open','high','low','close','change','transaction']
    dict_info={}
    for each in fields:
        #print(each)
        re_result= re.match(r'_',each)
        #print (re_result)
        if re_result==None:
            # setup dict_info
            cmd="dict_info['"+each+"']=stock."+each
            #print(cmd)
            exec(cmd)
    pd_stock=pandas.DataFrame()
    for each in dict_info:
        pd_stock[each]=pandas.Series(dict_info[each])
    return pd_stock

def stock_to_csv(stock,csv_file_name):
    pd_stock=twstock2pandas(stock)
    pd_stock.to_csv(csv_file_name,index=False)
    pass

def stock_to_yahooCSV(stock,csv_file_name):
    pd_stock=twstock2pandas(stock)
    yahoo_cols=['Date','Open','High','Low','Close','Volume','Adj Close']
    pd_stock_yahoo=pandas.DataFrame()
    pd_stock_yahoo['Date']=pd_stock.date
    pd_stock_yahoo['Open']=pd_stock.open
    pd_stock_yahoo['High']=pd_stock.high
    pd_stock_yahoo['Low']=pd_stock.low
    pd_stock_yahoo['Close']=pd_stock.close
    pd_stock_yahoo['Volume']=pd_stock.capacity
    pd_stock_yahoo['Adj Close']=pd_stock.close
    pd_stock_yahoo.to_csv(csv_file_name,index=False)
    
def stock_to_googleCSV(stock,csv_file_name):
    pd_stock=twstock2pandas(stock)
    yahoo_cols=['DATE','CLOSE','HIGH','LOW','OPEN','VOLUME']
    pd_stock_yahoo=pandas.DataFrame()
    pd_stock_yahoo['DATE']=pd_stock.date
    pd_stock_yahoo['OPEN']=pd_stock.open
    pd_stock_yahoo['HIGH']=pd_stock.high
    pd_stock_yahoo['LOW']=pd_stock.low
    pd_stock_yahoo['CLOSE']=pd_stock.close
    pd_stock_yahoo['VOLUME']=pd_stock.capacity
    pd_stock_yahoo.to_csv(csv_file_name,index=False)
    
if __name__ == "__main__":
    #stock=Stock(stock_id)
    stock=Stock('2618')
    stock.fetch_from(2010,1)
    twstock2googleCSV(stock,'2618.csv')
