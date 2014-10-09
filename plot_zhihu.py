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
        self.hour = []
        for item in self.time:
            date = ctime(item / 1000)  #there are three zero in the tail
            hour_and_minute = date.split(" ")[3] #get the time
            hour = hour_and_minute.split(":")[0] #get the number of hour 
            self.hour.append(int(hour))

        return self.hour  #for test, the information is self.hour
        
    def plot(self):
        
        fig = plt.figure()
        try:
            y = np.array(self.hour)
            plt.hist(y)
        except:
            buf = StringIO.StringIO()
            return buf
        
        
        buf = StringIO.StringIO()
        fig.savefig(buf, format='png', transparent=True)
        return buf
        