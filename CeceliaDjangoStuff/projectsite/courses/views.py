from django.shortcuts import render
from django.http import HttpResponse #, HttpRequest
from django.template import RequestContext, loader
from courses.models import Course, Datapoint, Student

#METRICS ARE TESTED 
#TODO reconfigure the metrics functions to search Courses or Students instead of datapoint
#TODO implement the error checks	
#TODO add more comments & write nicer docstrings
def MFRatio(info):
	""" takes in specified information and parses it - calculating the # of males and # of females
output: ratio of male:female """
	m = 0
	f = 0
	#males = Datapoint.objects.filter(stugen = "M").count()
	for item in info:
		if item.stugen == 'M':
			m += 1
		if item.stugen == 'F':
			f += 1
	return {'males':m, 'females':f}

def courseMajorPopularity(totals,courseTotals):
	""" takes in total counts of # of items per major exist overall & # of items per major exist for a certain course, calculates popularity as a proportions, and stores it away in a dictionary
output: dictionary mapping popularities to respective majors for a certain class """
	for key in totals:
		popularity[key] = courseTotals[key]/totals[key]
	return popularity

def majorTotalCount():
	""" does not take in any inputs, searches datapoint for counts of items of specific majors
output: dictionary of # of items per major based on stumaj mapped to majors """
	MEtotal = Datapoint.objects.filter(stumaj = "ME").count()
	ECEtotal = Datapoint.objects.filter(stumaj = "ECE").count()
	ECtotal = Datapoint.objects.filter(stumaj = "EC").count()
	EBtotal = Datapoint.objects.filter(stumaj = "EB").count()
	ERtotal = Datapoint.objects.filter(stumaj = "ER").count()
	EOtotal = Datapoint.objects.filter(stumaj = "EO").count()
	return {'ME':MEtotal,'ECE':ECEtotal,'EC':ECtotal,'EB':EBtotal,'ER':ERtotal,'EO':EOtotal}

def courseMajorCount(info):
	""" takes in information checks the popularity under various hardcoded conditions
output: popularity as a percentage """
#not sure what is exactly stored in stumaj - #TODO change the checks below
	ME = Datapoint.objects.filter(courseid = info).filter(stumaj = "ME").count()
	ECE = Datapoint.objects.filter(courseid = info).filter(stumaj = "ECE").count()	
	EC = Datapoint.objects.filter(courseid = info).filter(stumaj = "EC").count()	
	EB = Datapoint.objects.filter(courseid = info).filter(stumaj = "EB").count()	
	ER = Datapoint.objects.filter(courseid = info).filter(stumaj = "ER").count()	
	EO = Datapoint.objects.filter(courseid = info).exclude(stumaj = "ME").exclude(stumaj = "ECE").exclude(stumaj = "EC").exclude(stumaj = "EB").exclude(stumaj = "ER").count()	#since EO (probably) does not exist as a stumaj, filter out all other specified majors and count what is leftover

#	for item in info:
#		if item.stumaj == 'ME': 
#			MEtotal += 1
#		elif item.stumaj == 'ECE': 
#			ECEtotal += 1
#		elif item.stumaj == 'EC': 
#			ECtotal += 1
#		elif item.stumaj == 'EB': 
#			EBtotal += 1
#		elif item.stumaj == 'ER': 
#			ERtotal += 1
#		else:
#			EOtotal += 1
#	return {'ME':MEtotal,'ECE':ECEtotal,'EC':ECtotal,'EB':EBtotal,'ER':ERtotal,'EO',EOtotal}

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

def courseSearch(request):
	""" for the individual course search page """
	c_id = request.GET[course_id]
	#searched_course = Course.objects.get(pk=c_id)
	#searched_student = ??
	#not sure how to get to coursesearch from main 
	ratio = MFRatio(searched_dp)
	majortotal = majorTotalCount() #returns dictionary of majors and their counts
	majortotals_course = courseMajorCount(c_id) #returns dictionary of majors and their counts for a specific course
	majorPopularity = courseMajorPopularity(majortotal,majortotals_course)
	generalPopularity = Datapoint.objects.filter(courseid = info).count() / Datapoint.objects.all()
	return render(request,'courses/mainpage.jade',{'ratio':ratio,'majortotal':majortotal,'majorpopularity':majorPopularity,'overallpopularity':generalPopularity})

def course_simple(request):
#def course(request):
	""" for the dummy course search page """
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

#HERE IS THE REAL COMPARE FUNCTION IS!
def compare(request):
	error = 'NONE'
	compare_courses = []
	""" for the comparator page"""
	#context = {'compare0':request.GET['cc0'], 'compare1':request.GET['cc1'], 'compare2':request.GET['cc2']}
	#compare_course_0 = context['compare0']
	#compare_course_1 = context['compare1']
	#compare_course_2 = context['compare2']
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

def doSearch(request):
	""" for the advanced search page - replaces the original split function """
	majors_wanted = request.GET.getlist("majorsplit")
	colors_wanted = request.GET.getlist("colorsplit")
	#years_wanted = HttpRequest.getlist.GET("yearsplit")
	courses = []
	#print majors_wanted
	if len(majors_wanted) != 0:
		for major in majors_wanted:
			mmm = Datapoint.objects.filter(stumaj = major)
		for mm in mmm:
			if mmm not in courses:
				courses.append(mmm)
	if len(colors_wanted) != 0:
		for color in colors_wanted:
			c = Datapoint.objects.filter(courseID = color)
		for cc in c:
			if c not in courses:
				courses.append(c)
	"""
	if len(years_wanted) != 0:
		for year in years_wanted:
			c = Course.objects.filter("year" = year)
			for yy in y:
				if y not in courses:
					courses.append(y)
	"""
	return render(request, 'courses/mainpage.jade', {"courses": courses})

"""

NOTES:

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
#def split(request):
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
