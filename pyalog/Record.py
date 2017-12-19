# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:26:42 2017

@author: housesu
"""
import pandas as pd

class Record:
    def __init__ (self):
        print "init"
        self.data = pd.DataFrame()
        pass
    
    """args: list"""
    def _record(self,df_line):
        #record=pd.DataFrame()
        self.data=self.data.append(df_line)
        #print self.data
        #self.data.head()         
    
    def record(self,*hashes):
        #record=pd.DataFrame()
        #self.data=self.data.append(df_line)
        
        new_list=[]
        new_index=[]
  
        for each in hashes:
            #print each
            keys=each.keys()
            vals=each.values()
            new_list.extend(vals)
            new_index.extend(keys)
        new_df= pd.DataFrame([new_list],columns=new_index)
        self._record(new_df)
        
    def record_order(self,datetime, type='long',shares=1,price=0):
        self.record({'type':type},{"share":shares},{"price":price},{"date":datetime})
    
    def show(self):
        print self.data
    def save(self,name="record.csv"):
        self.data.to_csv(name)
    pass

if __name__ == "__main__":
    print "test"
    df=Record()
    #new_df= pd.DataFrame([[1,4,5,],[2,5,6]])
    #df.record(new_df)
    df.record({'a':4},{'b':6,'c':9})
    
    