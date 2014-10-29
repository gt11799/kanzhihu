#!user/bin/env python
# _*_ coding=utf8 _*_

'''
take data from zhihu.login_time, plot the frequency of login_time
'''

import MySQLdb
import matplotlib.pyplot as plt
import numpy as np
import StringIO
from time import ctime

import sae.const

class PlotZhihu(object):
    
    def __init__(self):
        self.db = MySQLdb.connect(host=sae.const.MYSQL_HOST, port=int(sae.const.MYSQL_PORT), user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, charset='utf8')
        self.cursor = self.db.cursor()
        
        self.cursor.execute("select name from login_time")
        self.names_all = set([name[0] for name in self.cursor])
        
    def get_names(self):
        return self.names_all
       
    def search_time(self, name):
        self.name = name
        
        sql = "select login_time from login_time where name='%s'" %self.name.encode('utf8')
        try:
            self.cursor.execute(sql)
        except:
            pass
        self.time = set([int(item[0]) for item in self.cursor]) #remove the repeated data
        self.hours = []
        for item in self.time:
            date = ctime(item / 1000)  #there are three zero in the tail
            hour_and_minute = date.split(" ")[3] #get the time
            hour = hour_and_minute.split(":")[0] #get the number of hour 
            self.hours.append(int(hour))

        return self.hours  #for test, the information is self.hours
        
    def plot(self):
        
        fig = plt.figure(dpi=50)
        x = range(24)
        y = [self.hours.count(hour) for hour in x]
            
        ax = fig.add_subplot(111, frameon=False)
        plt.fill(x, y, 'r')
        ax.set_ylim(0, max(y) * 1.3)
        ax.set_xlim(0, 24)
        
        ax.axes.get_yaxis().set_visible(False)
        
        
        buf = StringIO.StringIO()
        fig.savefig(buf, format='png', transparent=True)
        return buf
        
