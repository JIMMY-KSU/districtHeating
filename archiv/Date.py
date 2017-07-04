# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 14:17:01 2017

@author: jpelda
"""

from datetime import datetime

class Date():
    def __init__(self, dateValues):
        self.date = datetime(dateValues['year'], dateValues['month'], dateValues['day'], dateValues['hour'], dateValues['minute'])
        
    def getTime(self):
        
        return self.date.time()
    
    def getWeekday(self):
        
        return self.date.weekday()