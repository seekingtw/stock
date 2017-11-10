# -*- coding: utf-8 -*-

from twstock import Stock
import pandas 
import re

def twstock2pandas(stock_id):
    pd_stock=None
    stock=Stock(stock_id)
    fields = ['date','capacity','turnover','open','high','low','close','change','transaction']
    dict_info={}
    for each in fields:
        #print(each)
        re_result= re.match(r'_',each)
        #print (re_result)
        if re_result==None:
            #dict_info[each]=stock.daa
            cmd="dict_info['"+each+"']=stock."+each
            #print(cmd)
            exec(cmd)
#print(dict_info)
    pd_stock=pandas.DataFrame()
    for each in dict_info:
        pd_stock[each]=pandas.Series(dict_info[each])
    return pd_stock

def twstock2csv(stock_id,csv_file_name):
    pd_stock=twstock2pandas(stock_id)
    pd_stock.to_csv(csv_file_name,index=False)
    pass

def twstock2yahooCSV(stock_id,csv_file_name):
    pd_stock=twstock2pandas(stock_id)
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
if __name__ == "__main__":
    twstock2yahooCSV('2618','2618.csv')