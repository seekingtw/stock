# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:26:42 2017

@author: housesu
"""
import pandas as pd
import pickle
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
                previous_profilio = self.profilio[i]
                previous_price = self.price[i]
                continue
            self.profit.append( self.profilio[i] - previous_profilio)
            previous_profilio= self.profilio[i]
            self.price_diff.append(self.price[i] - previous_price)
            previous_price= self.price[i]
        pass
    def save(self,name ):
        pickle.dump(self, open(name + "_section_ana.pickle", "wb"))
    def drawback_check(self ):
        print ("i, date, type,price, diff_price")
        for i,each in enumerate (self.price_diff):
            if each < 0 and self.type[i] == "long_exit":
                print (i-1, self.datetimes[i-1], self.type[i-1],self.price[i-1])
                print (i, self.datetimes[i],self.type[i],self.price[i])

    def show(self):
        if len(self.profit) == 0: self.analyze()
        print len(self.profilio)
        print ("i , date, type,profilio,profit,position,price,share, diff_price")
        for i in range(len(self.profilio)):
            #print i
            #print ( self.datetimes[i])
            #print self.type[i]
            #print self.profilio[i]
            #print (self.profit[i] )
            print (i, self.datetimes[i], self.type[i],
                   self.profilio[i],self.profit[i],self.position[i],
                   self.price[i],self.share[i], self.price_diff[i])

        pass
