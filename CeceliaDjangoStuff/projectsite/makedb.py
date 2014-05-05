# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 15:49:46 2014

@author: ldavis
"""

import csv
import sys
import sqlite3 as lite
from courses.seedcode.OrganizeData import *
from courses.seedcode.Professor import *
from courses.seedcode.parse_course_data import *
from courses.seedcode.moreParseData import *

def makedb():
    '''create the database needed for the django website'''
    #rip data points from Sarah/Berit's db using Cecelia's code    
    datapoints = createDataPoints()
    #initialize connection to db file    
    con = lite.connect('oca.db')
    #going to need these later
    stuarchive = []
    coursearchive = [] 
    with con:
        cur = con.cursor()
        #loop through all the datapoints to rip their attributes into a db
        dpid = 0
        for point in datapoints:
            #cur.execute() takes a tuple, so extract course attributes
            dpinsertable = (dpid, point.stuID, point.gradYear, point.stuSem, point.stuGen, point.stuMaj, point.course, point.prof)
            cur.execute("INSERT INTO Datapoints VALUES(?, ?, ?, ?, ?, ?, ?, ?)", dpinsertable)
            dpid += 1
            #determine if student is unique, then add to table if so
            if point.stuID not in stuarchive:
                stuinsertable = (point.stuID, point.gradYear, point.stuGen, point.stuMaj)
                cur.execute("INSERT INTO Students VALUES(?, ?, ?, ?)", stuinsertable)
                stuarchive.append(point.stuID)
            #similarly, add all unique courses to their own table
            if point.course not in coursearchive:
                courseinsertable = (point.course, courses[point.course])
                cur.execute("INSERT INTO Courses VALUES(?, ?)", courseinsertable)
                coursearchive.append(point.course)
        #with should autocommit, but I think I'll be careful
        con.commit()
        #move, girl, just back it up
        data = '\n'.join(con.iterdump())
        f = open('oca.sql', 'w')
        with f:
            f.write(data)
        #you can use 'cat oca.sql' from a terminal window to check and see if the database compiled correctly
        
