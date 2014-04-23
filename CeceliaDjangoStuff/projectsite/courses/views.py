from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import RequestContext, loader
from courses.models import Course

def index(request):
	all_courses_list = Course.objects.all()
	context = {'all_courses_list':all_courses_list}
	return render(request, 'courses/index.jade', context)
	

	#render(request, template url, context -> a thing that maps template variable names to python objects, like the actual list with courses in it)
	#render returns an HttpResponse, which is returned by the index view (which is, in the MVC framework, a controller)
	#return HttpResponse(str(all_courses_list[0]))
	#template = loader.get_template('courses/index.html')
	#context = RequestContext(request, {
	#	'all_courses_list':all_courses_list,
	#	})
	#response_output = ', '.join([c.coursetitle for c in all_courses_list])
	#return HttpResponse(template.reader(context))


def course(request, course_id):
	course = Course.objects.get(pk=course_id)
	coursetitle = 'Software Design'
	courseid = 'ENGR1111'
	popularity = '68'
	requirement = {'General': False, 'ECE': True, 'EC': True, 'ME': False, 'RE': False, 'BE': False}
	description = "Software Design is a programming course taught in Python. Through this course, students will be taught about: supporting tools such as Linux, Git, Spyder, etc., interfacing with external software packages, software engineering skills, and beyond! "
	coursesearch = ['Software Design', 'Real World Measurements', 'Happiness']
	context = {'coursetitle': coursetitle , 'courseid': courseid, 'popularity': popularity, 'requirement': requirement, 'description': description, 'coursesearch': coursesearch } 
	return render(request, 'courses/course.jade', context)

def compare(request):
	return render(request, 'courses/compare.jade')

def split(request):
	return render(request, 'courses/split.jade')

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
