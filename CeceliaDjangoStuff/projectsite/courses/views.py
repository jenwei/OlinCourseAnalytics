from django.shortcuts import render
from django.http import HttpResponse #, HttpRequest
from django.template import RequestContext, loader
from courses.models import Course #, Metrics

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

def course(request):
#def course(request):
	"""for the course page - need to change this so nothing is hard-coded"""
	#specificCourse = request.POST.get()
	#course = Course.objects.get(pk=course_id)
	#course = Course.objects.filter(coursetitle = 'Software Design')
	coursetitle = 'Software Design'
	courseid = 'ENGR1111'
	popularity = '100'
	requirement = {'General': False, 'ECE': True, 'EC': True, 'ME': False, 'RE': False, 'BE': False}
	description = "Software Design is a programming course taught in Python. Through this course, students will be taught about: supporting tools such as Linux, Git, Spyder, etc., interfacing with external software packages, software engineering skills, and beyond! "
	#courseS	
	coursesearch = ['Software Design', 'Real World Measurements', 'Happiness']
	context = {'coursetitle': coursetitle , 'courseid': courseid, 'popularity': popularity, 'requirement': requirement, 'description': description, 'coursesearch': coursesearch } 
	return render(request, 'courses/course.jade', context)

#def singleCourseSearch(request):
#	""" for the individual course search page """
	#searched_course = request.POST.get("NAME_OF_INPUT")
	#
#	return render(request,'courses/course.jade',searched_course)

def compare(request):
	""" for the comparator page - need to check to see if a third course exists
	also need to account for the actual model	
	"""
	compare_course_1 = request.POST.get("cc0")
	compare_course_2 = request.POST.get("cc1")
	compare_courses = []
	cc1 = Course.objects.filter(coursemajor = compare_course_1) | Course.objects.filter(courseID = compare_course_1)
	cc2 = Course.objects.filter(coursemajor = compare_course_2) | Course.objects.filter(courseID = compare_course_2)
	compare_courses.append(cc1)
	compare_courses.append(cc2)
	return render(request, 'courses/compare.jade',{"courses": compare_courses})



def split(request):
	""" CAN DELETE THIS """
	return render(request, 'courses/split.jade')

def doSearch(request):
	""" for the advanced search page """
	
	majors_wanted = request.POST.getlist("majorsplit[]")
	colors_wanted = request.POST.getlist("colorsplit[]")
	#years_wanted = HttpRequest.getlist.GET("yearsplit")
	courses = []
	#print majors_wanted
	if len(majors_wanted) != 0:
		for major in majors_wanted:
			mmm = Course.objects.filter(coursemajor = major)
		for mm in mmm:
			if mmm not in courses:
				courses.append(mmm)
	if len(colors_wanted) != 0:
		for color in colors_wanted:
			c = Course.objects.filter(courseID = color)
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
	return render(request, 'courses/split.jade', {"courses": courses})


"""
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