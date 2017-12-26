# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:26:42 2017

@author: housesu
"""
import pandas as pd

class section_analyzer:
    def __init__(self):
        self.datetimes = [] # to numpy?
        self.type = []      # 1 (long) -1(long exit) 2 (short) -2 (short exit)
        self.profilio=[]
        self.profit=[]      #diff of profilio
        self.position = []
        pass
    def item(self, datetime, type,profilio,position):
        self.datetimes.append(datetime)
        self.type.append(  type)
        self.profilio.append( profilio)
        self.position.append(position)
        pass
    def  analyze(self):
        previous_profilio = 0
        for i in range(len(self.profilio)):
            if previous_profilio == 0:
                self.profit.append( 0)
                previous_profilio = self.profilio[i]
                continue
            self.profit.append( self.profilio[i] - previous_profilio)
            previous_profilio= self.profilio[i]
        pass

    def show(self):
        if len(self.profit) == 0: self.analyze()
        print len(self.profilio)
        for i in range(len(self.profilio)):
            #print i
            #print ( self.datetimes[i])
            #print self.type[i]
            #print self.profilio[i]
            #print (self.profit[i] )
            print (i, self.datetimes[i], self.type[i],
                   self.profilio[i],self.profit[i],self.position[i])

        pass
