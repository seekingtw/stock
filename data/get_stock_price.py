import requests
import pandas as pd
import pprint

import datetime 
from datetime import timedelta
import calendar


time_format_api = "%Y/%m/%d"
time_format_string = "%Y%m%d"

def taiwan_year_to_year(tw_year):
        dates = tw_year.split('/')
        dates[0] = str(int(dates[0])+1911)
        return '/'.join(dates)
    
def string_to_datetime(string_date,request=False):
    datetime_format = time_format_api if request else time_format_string
    return datetime.datetime.strptime(string_date,datetime_format )

def datetime_to_string(date):
    return date.strftime(time_format_string)

def get_stock_price_monthly(stock_id,date,end=None):
    print("get",stock_id, "from",date)
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, str(stock_id))
    r=requests.get(url)
    data = r.json()
    def process_datetime(all_data):
        all_data[0] = string_to_datetime(taiwan_year_to_year(all_data[0]),True)
        return all_data
    
    data['data']= list(map(process_datetime,data['data']))

    if end:
        dt_end = string_to_datetime(end)
        data['data']=list(filter(lambda in_data:  in_data[0]<= dt_end,data['data']))
    return data     

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.datetime(year,month,day,0,0)
    
def get_stock_price(stock_id, from_date, to_date=None):
    date_from =string_to_datetime(from_date)
    if to_date:
        date_to = string_to_datetime(to_date)
    else:
        date_to = datetime.datetime.now()
    date_check = date_from
    prices= {'data':[]}
    while date_check<= date_to:
        price_data = get_stock_price_monthly(stock_id, datetime_to_string(date_check),datetime_to_string(date_to))
        prices['data'].extend(price_data['data'])
        if 'fields' not in prices:
            prices['fields'] = price_data['fields']
        date_check = add_months(date_check,1)
    return prices

def get_price_report(stock_id, from_date, to_date=None):
    prices_dict = get_stock_price(stock_id, from_date,to_date)
    df = pd.DataFrame({ e[0]: e[1:] for e in prices_dict['data']}, index=prices_dict['fields'][1:])
    df = df.transpose()
    return df
    #print(df)



if  __name__ == "__main__":
	df = get_price_report(2330,'20180101','20180312')
	print(df.describe())
	print(df)

