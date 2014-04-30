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

def mainpage(request):
	return render(request, 'courses/mainpage.jade')

def course(request, course_id):
	course = Course.objects.get(pk=course_id)
	coursetitle = 'Software Design'
	courseid = 'ENGR1111'
	popularity = '68'
	requirement = {'General': False, 'ECE': True, 'EC': True, 'ME': False, 'RE': False, 'BE': False}
	description = "Lorem ipsum dolor sit amet, percipit voluptaria usu et. Cu postea scripserit est. Mei at consul euripidis theophrastus, ne ancillae delectus eum. Ad eros scribentur delicatissimi eos, te pro laudem iisque placerat, at fuisset commune postulant nec. Cu mea salutatus referrentur."
	coursesearch = ['Software Design', 'Real World Measurements', 'Happiness']
	context = {'coursetitle': coursetitle , 'courseid': courseid, 'popularity': popularity, 'requirement': requirement, 'description': description, 'coursesearch': coursesearch } 
	return render(request, 'courses/mainpage.jade', context)

def compare(request):
	context = {'compare0':request.GET['cc0'], 'compare1':request.GET['cc1']}
	return render(request, 'courses/mainpage.jade', context)

def split(request):
	context={'allmajorsplit': request.GET['majorsplit'], 'allcolorsplit':request.GET['colorsplit']}
	return render(request, 'courses/mainpage.jade', context)

def team(request):
	return render(request, 'courses/team.jade')

def project(request):
	return render(request, 'courses/project.jade')
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
