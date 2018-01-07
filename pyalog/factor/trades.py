# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:26:42 2017

@author: housesu
"""
import pandas as pd
import pickle
import numpy as np
'''
analyzer report
max/min/stdd
maxdraw down
compare information: needed a base like market generic benifit rate or bank ratio
sharp ratie
'''
'''
experience rates:
1. max rates
2. net profilio >lost*10
3. min trade num
4. win rate
5. avage win/avage lost > 1.5
'''
class section_analyzer:
    def __init__(self):
        self.datetimes = [] # to numpy?
        self.type = []      # 1 (long) -1(long exit) 2 (short) -2 (short exit)
        self.profilio=[]
        self.profit=[]      #diff of profilio
        self.position = []
        self.price = []
        self.share= []
        self.price_diff= []
        self.diff_rate =[]
        pass
    def item(self, datetime, type,profilio,position,price,share):
        self.datetimes.append(datetime)
        self.type.append(  type)
        self.profilio.append( profilio)
        self.position.append(position)
        self.price.append(price)
        self.share.append(share)
        pass
    def  analyze(self):
        previous_profilio = 0
        previous_price = 0
        for i in range(len(self.profilio)):
            if previous_profilio == 0:
                self.profit.append( 0)
                self.price_diff.append(0)
                self.diff_rate.append(0)
                previous_profilio = self.profilio[i]
                previous_price = self.price[i]
                continue
            self.profit.append( self.profilio[i] - previous_profilio)
            previous_profilio= self.profilio[i]
            self.price_diff.append(self.price[i] - previous_price)
            if self.type[i] == "long_exit":
                self.diff_rate.append(self.price_diff[i] / previous_price)
            else:
                self.diff_rate.append(0)
            previous_price= self.price[i]

        pass
        rates= []
        positive_rates=[]
        negtive_rates=[]
        max_rates= None
        min_rates=None
        for i in range(len(self.type)):
            if (self.type[i] == "long_exit"):
                rates.append(self.diff_rate[i])
                if self.diff_rate[i] > 0 :
                    positive_rates.append(self.diff_rate[i])
                else:
                    negtive_rates.append(self.diff_rate[i])
                if max_rates < self.diff_rate[i]:
                    max_rates = self.diff_rate[i]
                if min_rates>  self.diff_rate[i]:
                    min_rates =  self.diff_rate[i]
            pass
        print "trade num :",len(rates)
        print "rate mean: " ,np.mean(rates)
        print "rate std :" , np.std(rates)
        print "+ num:",len(positive_rates)
        print "+rate mean: ", np.mean(positive_rates)
        print "+rate std :", np.std(positive_rates)
        print "+max rate:",np.max(positive_rates)
        print "- num:",len(negtive_rates)
        print "-rate mean: ", np.mean(negtive_rates)
        print "-rate std :", np.std(negtive_rates)
        print "-min rate:", np.min(negtive_rates)
        print "rates:" ,rates
        #for each in self.diff_rate: print each

    #def save(self,name ):
    #    pickle.dump(self, open(name + "_section_ana.pickle", "wb"))
    def save(self):
        dump_inst= {}
        dump_inst['datetime'] =self.datetimes
        dump_inst['type'] = self.type
        dump_inst['prifilio'] = self.profilio
        dump_inst['profit'] = self.profit
        dump_inst['position'] = self.position
        dump_inst['price'] = self.price
        dump_inst['share'] = self.share
        dump_inst['price_diff'] = self.price_diff
        return dump_inst

    @staticmethod
    def load(dump_inst):
        se_report= section_analyzer()
        se_report.datetimes=dump_inst['datetime']
        se_report.type=dump_inst['type']
        se_report.profilio=dump_inst['prifilio']
        se_report.profit=dump_inst['profit']
        se_report.position= dump_inst['position']
        se_report.price=dump_inst['price']
        se_report.share=dump_inst['share']
        return se_report
        se_report.price_diff= dump_inst['price_diff']

    def drawback_check(self ):
        print ("i, date, type,price, diff_price,rate")
        for i,each in enumerate (self.price_diff):
            if each < 0 and self.type[i] == "long_exit":
                print (i-1, self.datetimes[i-1], self.type[i-1],self.price[i-1],self.price_diff[i-1],self.diff_rate[i-1])
                print (i, self.datetimes[i],self.type[i],self.price[i],self.price_diff[i],self.diff_rate[i])

    def show(self):
        if len(self.profit) == 0: self.analyze()
        print len(self.profilio)
        print ("i , date, type,profilio,profit,position,price,share, diff_price,rate")
        for i in range(len(self.profilio)):
            print (i, self.datetimes[i], self.type[i],
                   self.profilio[i],self.profit[i],self.position[i],
                   self.price[i],self.share[i], self.price_diff[i], self.diff_rate[i])
            pass
        pass


    def view(self):
        if len(self.profit) == 0: self.analyze()
        print len(self.profilio)
        print ("i , date, type,profilio,profit,position,price,share, diff_price")
        for i in range(len(self.profilio)):
            # print i
            # print ( self.datetimes[i])
            # print self.type[i]#
            # print self.profilio[i]
            # print (self.profit[i] )
            print (i, self.datetimes[i], self.type[i],
                   self.profilio[i],self.profit[i],self.position[i],
                   self.price[i],self.share[i], self.price_diff[i])
            pass
        pass
