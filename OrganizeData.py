# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 14:30:15 2014

@author: cauerswald
"""
import csv
from Professor import *
from parse_course_data import *
from moreParseData import *

#creates lists of students, courses, and profs, so they can, in the future, be referred to and organized by their list index
#this just makes the numbers less weird and makes it easier to iterate through all students, courses, or profs
dataFileName = 'course_enrollments_2002-2014spring_anonymized.csv'
dataDictionaries = get_course_data(dataFileName)
studentsByNames = dataDictionaries[0]
coursesByNames = dataDictionaries[1]
professorsByNames = dataDictionaries[2]
students = [] #a list of all students IDS
courses = [] #a list of all courses by ID (the ID Sarah and Berit thought was most fitting, ususally the actual ID)
professors = [] #a list of all professor names in the format "Auerswald, Cecelia"

#creating above mentioned lists
for student in studentsByNames:
    students.append(student)

for course in coursesByNames:
    courses.append(course)

for prof in professorsByNames:
    professors.append(prof)


class DataPoint:
    def __init__(self, gradYear, stuID, stuGen, stuSem, stuMaj, courseID, profID):
        self.gradYear = gradYear
        self.stuID = stuID
        self.stuGen = stuGen
        self.stuSem = stuSem
        self.stuMaj = stuMaj
        self.course = courseID
        self.prof = profID

    def __str__(self):
        return "["+"Grad year:"+str(self.gradYear)+"\n Student ID: "+str(students[self.stuID])+"\n Gender: "+str(self.stuGen)+"\n Class taken in Semester #: "+str(self.stuSem)+"\n Major: "+str(self.stuMaj)+"\n Course ID: "+coursesByNames[courses[self.course]].title+" ("+str(courses[self.course])+")"+"\n Professor: "+str(professors[self.prof])+"]"



def createDataPoints():
    f= open(dataFileName, 'rU')
    fileContents = csv.reader(f)
    allData = []
    for row in fileContents:
        attrs = moreParseData(row)
        #order of attrs is: *means we don't care
        #academic status (graduated or not) *
        #graduation year
        #student id
        #gender
        #what number semester it is for the student (0= first semester freshman year, 8 is second semester senior year)
        #major 
        #concentration (this is not always filled) *
        #official olin course number (or equivalent, for analysis)
        #section number *
        #title of course
        #title of section *
        #name of professor
        if type(attrs)==list:
            gradYear = attrs[1]
            stuID = students.index(attrs[2].strip())
            stuGen = attrs[3]
            stuSem = attrs[4]
            stuMaj = attrs[5]
            courseID = courses.index(attrs[7].strip())
            profID = professors.index(attrs[11].strip())
            dp = DataPoint(gradYear, stuID, stuGen, stuSem, stuMaj, courseID, profID)
            allData.append(dp)
    return allData


            


