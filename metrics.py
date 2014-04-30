# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 13:46:18 2014

@author: ldavis
"""

import csv
from OrganizeData import *
from Professor import *
from parse_course_data import *
from moreParseData import *

class Course:
    def __init__(self,courseID,data):
        self.ID = courseID
        self.name = courses[courseID]
        newdata = filter(FilterCourseID(self.ID),data)
        self.popularity = self.Popularity(newdata)
        self.avgsem = self.AverageSemester(newdata)
        self.majorsplit = self.MajorSplit(newdata)
        self.teachsplit = self.TeachSplit(newdata)
        self.gendsplit = self.GendSplit(newdata)
        
    def Popularity(self,data):
        stumatch = []
        taken = []
        for instance in data:
            if instance.stuID not in stumatch:
                stumatch.append(instance.stuID)
            if instance.course == self.ID and instance.stuID not in taken:
                taken.append(instance.stuID)
        popularity = float(len(taken))/float(len(stumatch))
        return popularity
        
    def AverageSemester(self,data):
        total = 0
        counter = 0
        for instance in data:
            if instance.course == self.ID:
                total += instance.stsem
                counter += 1
        avgsem = float(total)/float(counter)
        return avgsem
        
    def MajorSplit(self,data):
        majorlist = []
        newdata = []
        splitdict = dict()
        for instance in data:
            if instance.course == self.ID:
                stulist.append(instance.major)
            if instance.stuMaj not in majorlist:
                majorlist.append(instance.major)
        for major in majorlist:
            counter = 0
            for item in newdata:
                if item == major:
                    counter += 1
            splitdict[major] = counter/len(data)
        return splitdict
        
    def TeachSplit(self,data):
        splitdict = dict()
        proflist = []
        newdata = []
        for instance in data:
            if instance.course == self.ID:
                newdata.append(instance.prof)
                if instance.prof not in proflist:
                    proflist.append(instance.prof)
        for professor in proflist:
            counter = 0
            for item in newdata:
                if item == professor:
                    counter += 1
            splitdict[professor] = counter/len(data)
        return splitdict
    
    def GendSplit(self,data):
        fcount = 0
        mcount = 0
        for instance in data:
            if instance.course == self.ID and instance.stuGen == 'F':
                fcount += 1
            elif instance.course == self.ID and instance.stuGen == 'M':
                mcount += 1
        return fcount/mcount
    
def CourseList(clsem='all',stsem='all',major='all',teach='all',gend='all'):      
    courselist = []    
    data = createDataPoints()
    for instance in data:
        #use boolean values of or statements to establish if the data fits the request criteria
        clsemmatch = (clsem == 'all' or clsem == float(instance.gradYear) + (float(instance.stuSem)/2.0) - 4)
        stsemmatch = (stsem == 'all' or stsem == instance.stuSem)
        majormatch = (major == 'all' or major == instance.stuMaj)
        gendmatch = (gend == 'all' or gend == instance.stuGen)
        teachmatch = (teach == 'all' or teach == instance.prof)
        #condense the match values into one
        match = (clsemmatch and stsemmatch and majormatch and gendmatch and teachmatch)
        if not match:
            del instance
    for n in xrange(len(courses)):
        courselist.append(Course(n,data))
    return courselist
    
def FilterCourseID(courseID):
    return lambda datum: datum.course == courseID