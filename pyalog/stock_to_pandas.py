# -*- coding: utf-8 -*-

import sys
sys.path.insert(0,"twstock-master")
from twstock import Stock
import pandas 
import re
import click
from datetime import *

def datetime_to_google_time(time):
    month_abbr = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
                  'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
                  'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    #year=time.strftime("%Y")
    return time.strftime("%d-%b-%y")
                  
def stock_to_pandas(stock):
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
    pd_stock=stock_to_pandas(stock)
    yahoo_cols=['DATE','CLOSE','HIGH','LOW','OPEN','VOLUME','Adj Close']
    pd_stock_yahoo=pandas.DataFrame()
    pd_stock_yahoo['DATE']=pd_stock.date
    pd_stock_yahoo['OPEN']=pd_stock.open
    pd_stock_yahoo['HIGH']=pd_stock.high
    pd_stock_yahoo['LOW']=pd_stock.low
    pd_stock_yahoo['CLOSE']=pd_stock.close
    pd_stock_yahoo['VOLUME']=pd_stock.capacity
    pd_stock_yahoo['Adj Close']=pd_stock.close
    pd_stock_yahoo.to_csv(csv_file_name,index=False)
    
def stock_to_googleCSV(stock,csv_file_name):
    pd_stock=stock_to_pandas(stock)
    yahoo_cols=['Date','Open','High','Low','Close','Volume']
    pd_stock_yahoo=pandas.DataFrame()
    pd_stock_yahoo['Date']=pd_stock.date.apply(lambda t:t.strftime("%d-%b-%y"))
    pd_stock_yahoo['Open']=pd_stock.open
    pd_stock_yahoo['High']=pd_stock.high
    pd_stock_yahoo['Low']=pd_stock.low
    pd_stock_yahoo['Close']=pd_stock.close
    pd_stock_yahoo['Volume']=pd_stock.capacity
    pd_stock_yahoo.to_csv(csv_file_name,index=False)

def run_item(twid ,start, end, csv):
    try:
        datetime_start= datetime.strptime(start,"%Y-%m-%d")
        datetime_end= datetime.strptime(end,"%Y-%m-%d")
        if csv=="":
            csv=twid+".csv"
        print("twid: {}".format(twid))
        print("csv : {}".format(csv))
        #print(start)
        print("start_time: {}".format(datetime_start))
        #print(end)
        print("end_time(disable now): {}".format(datetime_end))
        fetch(twid,csv,datetime_start,datetime_end)
    except:
        print("run_item except")
    else:
        print("run_item done")

@click.command()
@click.option('--twid', default='2330', help='tw stock id')
@click.option('--csv', default='', help='csv output')
@click.option('--start', default='2010-01-01', help='start date')
@click.option('--end', default='2017-01-01', help='end date')
@click.option('--input_config', default='', help='input_config[line content : twid,start,end,csv#comment]')
def run(twid, csv, start, end,input_config):
    if input_config == '':
        run_item(twid,start,end,csv)
    else:
        with open(input_config,"r") as f:
            twid='2330'
            csv=''
            start='2010-01-01'
            end='2017-01-01'
            line=f.readline()
            while line :
                #print(line)
                texts=line.split('#')
                strs=texts[0].split(",")
                for i in range(len(strs)):
                    string=strs[i].strip()
                    if i == 0 : twid=string
                    if i == 1 and string!= '':start= string
                    if i == 2 and string!= '':end =string
                    if i==3 and string!= '':csv=string
                run_item(twid,start,end,csv)
                #print(twid,start,end,csv)
                line=f.readline()

def fetch(twid='2330',csv="",start_time=None,end_time=datetime.now()):
    if start_time == None:
        start_time=datetime.strptime(start,"2010-1-1")
   
    if csv=="":
        csv=twid+".csv"
    
    stock=Stock(twid)
    stock.fetch_from(int(start_time.strftime("%Y")),int(start_time.strftime("%m")))
    stock_to_googleCSV(stock,csv)

if __name__ == "__main__":
    #stock=Stock(stock_id)
    run()
    #run_item('2317', '2010-1-1' ,'2017-12-1' ,'2317.csv')

