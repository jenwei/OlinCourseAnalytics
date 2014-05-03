from django.shortcuts import render
from django.http import HttpResponse #, HttpRequest
from django.template import RequestContext, loader
from courses.models import Course, Datapoint, Student

def index(request):
	all_courses_list = Course.objects.all()
	context = {'all_courses_list':all_courses_list}
	return render(request, 'courses/index.jade', context)
	
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


def mainpage(request):
	return render(request, 'courses/mainpage.jade')

def courseSearch(request):
	""" for the individual course search page """
	c_id = request.GET[course_id]
	#searched_course = Course.objects.get(pk=c_id)
	searched_dp = Datapoint.objects.filter(courseid = c_id)
	#searched_student = ??
	#not sure how to get to coursesearch from main 
	return render(request,'courses/mainpage.jade',{'course':searched_dp})
	

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

def compare(request):
	""" for the comparator page"""
	context = {'compare0':request.GET['cc0'], 'compare1':request.GET['cc1'], 'compare2':request.GET['cc2']}
	cc0 = context['compare0']
	cc1 = context['compare1']
	cc2 = context['compare2']
	if cc0:
		cc0 = Course.objects.filter(coursemajor = compare_course_0) |Course.objects.filter(courseID = compare_course_0)
		compare_courses.append(cc0)
	#else:
		#return error
	if cc1:
		cc1 = Course.objects.filter(coursemajor = compare_course_1) | Course.objects.filter(courseID = compare_course_1)
		compare_courses.append(cc1)
	#else:
		#return error 
	if cc2:
		cc2 = Course.objects.filter(coursemajor = compare_course_2) | Course.objects.filter(courseID = compare_course_2)
		compare_courses.append(cc2)
	#else:
		#return error
	
	return render(request, 'courses/mainpage.jade', {'compare_courses': compare_courses})

def doSearch(request):
	""" for the advanced search page """
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
			c = Course.objects.filter(id = color)
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

#def singleCourseSearch(request):
#	""" for the individual course search page """
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
