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

