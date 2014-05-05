from django.shortcuts import render
from django.http import HttpResponse #, HttpRequest
from django.template import RequestContext, loader
from courses.models import Course, Datapoint, Student

#METRICS ARE TESTED 
#TODO reconfigure the metrics functions to search Courses or Students instead of datapoint
#TODO implement the error checks	
#TODO add more comments & write nicer docstrings

def index(request):
	all_courses_list = Course.objects.all()

	context = {'all_courses_list':all_courses_list}#, error:None}
	return render(request, 'courses/index.jade', context)

def mainpage(request):
	return render(request, 'courses/mainpage.jade')

def team(request):
	return render(request, 'courses/team.jade')

def project(request):
	return render(request, 'courses/project.jade')

def MFRatio(course):
	""" takes in specified course and parses it - calculating the # of males and # of females
output: ratio of male:female """
	m = course.student_set.filter(stugen = "M").count()
	f = course.student_set.filter(stugen = "F").count()
	total = m+f
	males = float(m)/total * 100
	females = float(f)/total * 100
	return {'males':males, 'females':females}


def majorDistribution():
	""" does not take in any inputs and counts the number of students in each major
output: # of students in each major """
	MEtotal = Student.objects.filter(stumaj = "Mechanical Engineering").count()
	ECEtotal = Student.objects.filter(stumaj = "Electr'l & Computer Engr").count()
	Concentrationtotal = Student.objects.filter(stumaj = "Engineering").count()
	Undeclaredtotal = Student.objects.filter(stumaj = "Undeclared").count()
	return {'ME':MEtotal,'ECE':ECEtotal,'EConcentration':Concentrationtotal,'Undeclared':Undeclaredtotal}
	
def coursePopularityByMajor(course):
	""" takes in specified course and calculates # of students of each major who take it
output: # of students mapped to their designated majors """
	course = Course.objects.filter(id = course)
	MEcount = course.student_set.filter(stumaj = "Mechanical Engineering").count()
	ECEcount = course.student_set.filter(stumaj = "Electr'l & Computer Engr").count()	
	Concentrationcount = course.student_set.filter(stumaj = "Engineering").count()	
	Undeclaredcount = course.student_set.filter(stumaj = "Undeclared").count()	
	return {'ME':MEcount,'ECE':ECEcount,'EConcentration':Concentrationcount,'Undeclared':Undeclaredcount}

def popularityOfCourse(course):
	""" takes in course popularity by major and the overall major distribution
output: popularity proportions """
	#print "HERE I AM"
	#course = course.objects.filter(id = course.id)
	#print course
	MEpop = float(course.student_set.filter(stumaj = "Mechanical Engineering").count()) / Student.objects.filter(stumaj = "Mechanical Engineering").count() * 100
	#print "ME"
	#print MEpop
	ECEpop = float(course.student_set.filter(stumaj = "Electr'l & Computer Engr").count()) / Student.objects.filter(stumaj = "Electr'l & Computer Engr").count() * 100
	Concentrationpop = float(course.student_set.filter(stumaj = "Engineering").count()) / Student.objects.filter(stumaj = "Engineering").count() * 100
	Undeclaredpop = float(course.student_set.filter(stumaj = "Undeclared").count()) / Student.objects.filter(stumaj = "Undeclared").count() * 100
	return {'ME':MEpop,'ECE':ECEpop,'EConcentration':Concentrationpop,'Undeclared':Undeclaredpop}

def courseSearch(request):
	""" for the individual course search page """
	#TODO swap C_ID with C_Name if/when it exists
	c_ID = request.GET['coursesearch']
	#print c_ID
	searched_course = Course.objects.get(name = c_ID)
	#print searched_course
	ratio = MFRatio(searched_course)
	#print ratio
	pop = popularityOfCourse(searched_course)
	#print pop
	return render(request,'courses/mainpage.jade',{'courseID':searched_course,'males':ratio["males"], 'females': ratio["females"],'popularityME':pop["ME"], 'popularityECE':pop["ECE"], 'popularityEConcentration':pop["EConcentration"], 'popularityUndeclared':pop["Undeclared"]})

#ANYTHING ABOVE THIS POINT SHOULD WORK/HAS BEEN CHECKED----------------------------
	
def advanceSearch(request):
	""" for the advanced search page - replaces the original split function & references splitside.jade """
	majors_wanted = request.GET.getlist("majorsplit")
	colors_wanted = request.GET.getlist("colorsplit")
	#years_wanted = HttpRequest.getlist.GET("yearsplit")
	courses = []
	#print majors_wanted
	if len(majors_wanted) != 0:
		for major in majors_wanted:
			if major == "all":
				specifiedMajor = Course.student_set.all()
			else:
				specifiedMajor = Course.student_set.filter(stumaj = major)
		for m in specifiedMajors:
			if m not in courses:
				courses.append(m)
	if len(colors_wanted) != 0:
		choices = Course.objects.all()
		for course in choices:
			for color in colors_wanted:
				print color
				if color in course.name:
					if course not in courses:
						print course
						courses.append(course)	
	print courses
	return render(request, 'courses/mainpage.jade', {"courses": courses})

#HERE IS THE REAL COMPARE FUNCTION!
def compare(request):
	error = 'NONE'
	compare_courses = []
	""" for the comparator page"""

	if request.GET['cc0']:
		compare_course_0 = request.GET['cc0']
		cc0 = Datapoint.objects.filter(courseid = compare_course_0) | Datapoint.objects.filter(course = compare_course_0)
		compare_courses.append(cc0)
	#else:
		#return error
		error = 'INCOMPLETE'
	if request.GET['cc1']:
		compare_course_1 = request.GET['cc1']
		cc1 = Datapoint.objects.filter(courseid = compare_course_1) | Datapoint.objects.filter(course = compare_course_1)
		compare_courses.append(cc1)
	#else:
		#return error
		if error == 'INCOMPLETE':
			error = 'INCOMPLETE1' 
		else:
			#error = 'INCOMPLETE'
			error = 'EMPTY'
#TODO: MOD COURSES.JS IF 3rd (CC2) IS WANTED 
	#if request.GET['cc2']:
	#	compare_course_2 = request.GET['cc2']
	#	cc2 = Datapoint.objects.filter(coursemajor = compare_course_2) | Datapoint.objects.filter(courseID = compare_course_2)
	#	compare_courses.append(cc2)
	#else:
	#	if error == 'INCOMPLETE1':	
	#		error = 'EMPTY'

	return render(request, 'courses/mainpage.jade', {'compare_courses': compare_courses,'error':error})

"""

NOTES:

#for the compare function
	#context = {'compare0':request.GET['cc0'], 'compare1':request.GET['cc1'], 'compare2':request.GET['cc2']}
	#compare_course_0 = context['compare0']
	#compare_course_1 = context['compare1']
	#compare_course_2 = context['compare2']

def course_simple(request):
#def course(request):
	#the dummy course search page
	#specificCourse = request.POST.get()
	#course = Course.objects.get(pk=course_id)
	#course = Course.objects.filter(coursetitle = 'Software Design')
	coursetitle = 'Software Design'
	courseid = 'ENGR1111'
	popularity = '100'
	requirement = {'General': False, 'ECE': True, 'EC': True, 'ME': False, 'RE': False, 'BE': False}
	description = "Software Design is a programming course taught in Python. Through this course, students will be taught about: supporting tools such as Linux, Git, Spyder, etc., interfacing with external software packages, software engineering skills, and beyond! "
	#courseSearch	
	coursesearch = ['Software Design', 'Real World Measurements', 'Happiness']
	context = {'coursetitle': coursetitle , 'courseid': courseid, 'popularity': popularity, 'requirement': requirement, 'description': description, 'coursesearch': coursesearch } 
	return render(request, 'courses/mainpage.jade', context)

#def courseMajorPopularity(totals,courseTotals):
	#takes in total counts of numbers of items per major exist overall &  numberof items per major exist for a certain course, calculates popularity as a proportions, and stores it away in a dictionary output: dictionary mapping popularities to respective majors for a certain class
#	for key in totals:
#		popularity[key] = courseTotals[key]/totals[key]
#	return popularity

#def majorTotalCount():
	 does not take in any inputs, searches datapoint for counts of items of specific majors output: dictionary of number of items per major based on stumaj mapped to majors 
#	MEtotal = Datapoint.objects.filter(stumaj = "Mechanical Engineering").count()
#	ECEtotal = Datapoint.objects.filter(stumaj = "Electr'l & Computer Engr").count()
#	Concentrationtotal = Datapoint.objects.filter(stumaj = "Engineering").count()
#	Undeclaredtotal = Datapoint.objects.filter(stumaj = "Undeclared").count()
#	return {'ME':MEtotal,'ECE':ECEtotal,'EConcentration':Concentrationtotal,'Undeclared':Undeclaredtotal}

#def courseMajorCount(info):
#	takes in information checks the popularity under various hardcoded conditions
#output: popularity as a percentage
##not sure what is exactly stored in stumaj - #TODO change the checks below
#	ME = Datapoint.objects.filter(courseid = info).filter(stumaj = "Mechanical Engineering").count()
#	ECE = Datapoint.objects.filter(courseid = info).filter(stumaj = "Electr'l & Computer Engr").count()	
#	Concentration = Datapoint.objects.filter(courseid = info).filter(stumaj = "Engineering").count()	
#	Undeclared = Datapoint.objects.filter(courseid = info).filter(stumaj = "Undeclared").count()	
#	return {'ME':ME,'ECE':ECE,'EConcentration':Concentration,'Undeclared':Undeclared}


#commented code from def index:	
	#word{object_list.count|pluralize}
	#render(request, template url, context -> a thing that maps template variable names to python objects, like the actual list with courses in it)
	#render returns an HttpResponse, which is returned by the index view (which is, in the MVC framework, a controller)
	#return HttpResponse(str(all_courses_list[0]))
	#template = loader.get_template('courses/index.html')
	#context = RequestContext(request, {
	#	'all_courses_list':all_courses_list,
	#	})
	#response_output = ', '.join([c.coursetitle for c in all_courses_list])
	#return HttpResponse(template.reader(context))


#def singleCourseSearch(request):
#	for the individual course search page 
	#searched_course = request.GET.get("NAME_OF_INPUT")
	#
#	return render(request,'courses/course.jade',searched_course)


#SPLIT IS UNDER doSEARCH
#def split(request):git 
#	context={'allmajorsplit': request.GET.getlist['majorsplit'], #'allcolorsplit':request.GET.getlist['colorsplit']}
#	return render(request, 'courses/mainpage.jade', context)

def course(request, course_id):
	if int(len(Course.objects.all()))>=int(course_id):
		#get the course that has the given course id
		course = Course.objects.get(pk=course_id) 
		#create dictionary that maps the coursetitle variable from the course template to the proper variable, as defined above
		context = {'coursetitle': course.coursetitle, 'courseid': 'ENGR1111'}#create dictionary that maps the coursetitle variable from the course template to the proper variable, as defined above
	else:
		context = {}
	return render(request, 'courses/course.html', context)
    #return HttpResponse("You are looking at something AWESOME. just pretend ok...")
"""
