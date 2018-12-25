# -*- coding: utf-8 -*-
"""

data from 
https://github.com/Asoul/tsec
to
google format
"""

import pandas as pd
import numpy as np
import re
import sys
import datetime
month_map = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def date_tw_to_west(tw):
    m = re.match("(?P<year>\d+)/(?P<mon>\d+)/(?P<date>\d+)", tw)
    #print (m.groups())
    if not m: return ""
    year = int ( m.group('year') )+1911
    month = int (m.group('mon'))
    date = int(m.group('date'))
    #print(year,month,date)
    da= datetime.datetime(year, month, date)
    return "%d-%s-%d" %(date,month_map[month-1],year)


def clean_non(df):
    #ret = df.apply(lambda x : np.nan if x =='--' else x)
    def t(x):
        print(x,type(x))
        if x == "--": return np.nan
        else : return x
    #ret = df.apply(t)
    
    #ret = ret.dropna()
    a = df[df.Open=='--']
    #print(a.index)
    ret = df.drop(a.index)
    return ret

#print(sys.argv)

def data_to_google(datacsv, output_file="output.csv"):
    output="output.csv"
    if output_file:output = output_file
    df = pd.read_csv(datacsv)
    df.iloc[:,0] = df.iloc[:,0].apply(date_tw_to_west)
    df.columns = ['Date','Volume','amount','Open','High','Low','Close','diff','trade_cnt']
    google_col = ['Date','Open','High','Low','Close','Volume']
    df = df.drop(set(df.columns) - set(google_col), axis =1) 
    df = clean_non(df)
    df = df[-1:0:-1]
    df.to_csv(output,index=False)

if __name__ == "__main__":
    if len(sys.argv) <2: 
        print("input file needed")
    data_to_google(sys.argv[1],sys.argv[2])
