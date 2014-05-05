from django.shortcuts import render
from django.http import HttpResponse #, HttpRequest
from django.template import RequestContext, loader
from courses.models import Course, Datapoint, Student

#METRICS ARE TESTED 
#TODO reconfigure the metrics functions to search Courses or Students instead of datapoint
#TODO implement the error checks	
#TODO add more comments & write nicer docstrings
coursetitledict = {'ENGR3220': 'Human Factors & Interaction Design', 'ENGR3499B': 'Special Topics in Electrical & Computer Engineering', 'ENGR3499C': 'Special Topics in Electrical & Computer Engineering', 'MTH0097': 'Undergraduate Research in Mathematics', 'ENGR2340': 'Dynamics', 'ENGR3599': 'Special Topics in Computing', 'MTH0098': 'Independent Study in Mathematics', 'ENGR4290': 'Affordable Design and Entrepreneurship', 'SUST2201': 'Introduction to Sustainability', 'ENGR3830': 'Phase Transformations in Ceramic and Metallic Systems', 'MTH2160': 'Introduction to Mathematical Modeling', 'AHSE1101': 'History and Society', 'AHSE1100': 'History of Technology:A Cultural & Contextual Approach', 'AHSE1102': 'Arts and Humanities: Self-Explored in Art and Philosophy', 'AHSE1105': 'Arts, Humanities, Social ScienceFoundation with Rhetoric', 'MTH2188A': 'Special Topics in Mathematics', 'ENGR4190': 'Senior Capstone Program inEngineering (SCOPE)', 'ENGR3427': 'Mixed Analog-Digital VLSI II', 'ENGR3426': 'Mixed Analog-Digital VLSI I', 'ENGR3420': 'Introduction to Analog andDigital Communication', 'SCI3120': 'Solid State Physics', 'AHSE1199C': 'Arts, Humanities, Social ScienceFoundation Topic', 'ENGR4198': 'Olin Self Study in Engineering', 'ENGR4199': 'Alternative Capstone inEngineering', 'AHSE0197': 'Research Projects inArts Humanities Social Science', 'ENGR3710': 'Systems', 'SCI4198': 'Olin Self Study in Science', 'MTH2199': 'Special Topics in Mathematics', 'ENGR3330': 'Mechanical Design', 'ENGR2510': 'Software Design', 'ENGR3335': 'Mechanical Vibrations', 'ENGR3525': 'Software Systems', 'ENGR2199': 'Special Topics in Engineering', 'ENGR3199': 'Special Topics in Engineering', 'ENGR3210': 'Sustainable Design', 'SCI2199A': 'Special Topics in Physics', 'ENGR0098': 'Independent Study in Engineering', 'SCI2320': 'Applied Organic Chemistry', 'AHSE4590': 'Entrepreneurship Capstone', 'SCI1210': 'Principles of Modern Biologywith Lab', 'ENGR3299': 'Special Topics in DesignEngineering', 'MTH3160': 'Special Topics in Mathematics', 'AHSE4598': 'Olin Self Study in Business andEntrepreneurship', 'SCI2399': 'Special Topics in Chemistry', 'SCI1111': 'Modeling and Simulation of the Physical World', 'SCI0097': 'Undergraduate Research in theSciences', 'AHSE3199A': 'Special Topics in Arts,Humanities and Social Sciences', 'ENGR3450': 'Semiconductor Devices', 'ENGR2210': 'Principles of Engineering', 'ENGR3415': 'Digital Signal Processing', 'SCI2145': 'Special Topics in Physics', 'SCI2140': 'Relativity', 'MTH3150': 'Numerical Methods andScientific Computing', 'AHSE2199C': 'Special Topics in Arts,Humanities and Social Sciences', 'ENGR1330': 'Fundamentals of MachineShop Operations', 'FND1320': 'Mathematical Foundations ofEngineering II:  Linear Algebraand Vector Calculus', 'SCI2214': 'Microbial Diversity', 'AHSE3599': 'Special Topics in Business andEntrepreneurship', 'ENGR2620': 'Biomechanics', 'MTH3170': 'Nonlinear Dynamics and Chaos', 'AHSE3190': 'Arts Humanities Social SciencesCapstone Preparatory Workshop', 'AHSE1199G': 'Arts, Humanities, Social ScienceFoundation Topic', 'AHSE3510': 'New Technology Ventures', 'ENGR3620': 'Cellular Bioengineering', 'AHSE3199': 'Special Topics in Arts,Humanities and Social Sciences', 'ENGR2299': 'Special Topics in DesignEngineering', 'SCI3320': 'Organic Chemistry II with Lab', 'SCI2099A': 'Special Topics in Science', 'ENGR3355': 'Renewable Energy', 'SCI2099': 'Special Topics in Science', 'ENGR3600': 'Topics in Bioengineering', 'ENGR2199B': 'Special Topics in Engineering', 'ENGR2410': 'Signals & Systems', 'MTH1111': 'Modeling and Simulation of thePhysical World', 'MTH1110': 'Calculus', 'AHSE1150': 'What is I?', 'AHSE1155': 'Arts, Humanities, Social ScienceFoundation Topic', 'ENGR3610': 'Biomedical Materials', 'AHSE0198': 'Independent Study in Arts, Humanities, Social Science', 'AWAY1000': 'Study Away Program', 'AHSE2199': 'Special Topics in Arts,Humanities and Social Science', 'AHSE2112': 'Six Books that Changed the World', 'AHSE2110': 'The Stuff of History: Ancient,Revolutionary & ContemporaryMaterials Technologies', 'AHSE2114': 'Science Fiction and HistoricalContext', 'AHSE4199': 'Special Topics in Arts,Humanities and Social Science', 'AHSE3130': 'Advanced Digital Photography', 'ENGR2599': 'Special Topics in Computing', 'SCI3210': 'Human Molecular Genetics in theAge of Genomics', 'ENGR3140': 'Error Control Codes', 'AHSE4198': 'Olin Self Study in Arts,Humanities, Social Science', 'ENGR3499': 'Special Topics in Electrical &Computer Engineering', 'AHSE1145': 'Anthropology: Culture,Knowledge & Creativity', 'ISR4198': 'Olin Self Study', 'FND1220': 'Physical Foundations ofEngineering II', 'MTH2120': 'Linear Algebra', 'ENGR3540': 'Computational Modeling', 'ENGR3370': 'Controls', 'ENGR3270': 'Special Topics in DesignEngineering', 'AHSE2120': 'Heroes for the RenaissanceEngineer: Leonardo, Nabokov,Bach and Borodin', 'SCI1199B': 'Foundation Topic in Physics', 'MTH4198': 'Olin Self Study in Mathematics', 'ENGR3310': 'Transport Phenomena', 'ENGR3499A': 'Special Topics in Electrical &Computer Engineering', 'ENGR2330': 'Introduction to MechanicalPrototyping', 'SCI2130B': 'Quantum Physics', 'ENGR3399': 'Special Topics in MechanicalEngineering', 'SCI1310': 'Introduction to Chemistrywith Lab', 'MTH3120': 'Partial Differential Equations', 'SCI1121': 'Electricity and Magnetism', 'MTH2130': 'Probability and Statistics', 'ENGR3392': 'Robotics 2', 'SCI2299': 'Special Topics in BiologicalSciences', 'ENGR3390': 'Robotics', 'AHSE1500': 'Foundations of Business andEntrepreneurship', 'AHSE1130': 'Seeing and Hearing:Communicating with Photographs,Video and Sound', 'ENGR2599A': 'Special Topics in Computing', 'AHSE0597': 'Undergraduate Research inBusiness and Entrepreneurship', 'MTH2140': 'Differential Equations', 'AHSE0598': 'Independent Study in Business &Entrepreneurship', 'ENGR3410': 'Computer Architecture', 'AHSE2199B': 'Special Topics in Arts,Humanities and Social Sciences', 'AHSE2199A': 'Special Topics in Arts,Humanities and Social Science', 'AHSE2131': 'Responsive Drawing andVisual Thinking', 'AHSE2130': 'The Intersection of Art andScience', 'ENGR3899A': 'Special Topics in MaterialsScience', 'ENGR2250': 'User Oriented CollaborativeDesign', 'ENGR2420': 'Intro Microelectronic Circuits', 'SCI2210': 'Immunology', 'ELE2710': 'Physics of Living Organisms', 'ENGR3260': 'Design for Manufacturing', 'MTH3199': 'Special Topics in Mathematics', 'ENGR2320': 'Mechanics of Solids andStructures', 'FND2410': 'Foundations of EngineeringProject III', 'FND2411': 'Sophomore Design ProjectPreparation', 'ENGR3630': 'Special Topics in Bioengineering', 'AHSE4190': 'Arts Humanities Social SciencesCapstone', 'ENGR1199': 'Special Topics in Engineering', 'SUST3301': 'Sustainability Synthesis', 'SCI2130A': 'Modern Physics', 'ENGR3810': 'Structural Biomaterials', 'ENGR1110': 'Modeling and Control', 'SCI2110': 'Biological Physics', 'AHSE1122': 'The Wired Ensemble -Instruments, Voices, Players', 'ENGR0097': 'Undergraduate Research inEngineering', 'ENGR3199A': 'Special Topics in Engineering', 'AHSE1199F': 'Arts, Humanities, Social ScienceFoundation Topic', 'ENGR3199B': 'Special Topics in Engineering', 'ENGR3520': 'Foundations of Computer Science', 'ENGR3599A': 'Special Topics in Computing', 'ENGR3250': 'Product Design and Development', 'SCI0098': 'Independent Study inScience', 'ENGR2141': 'Engineering for Humanity', 'ISR0097': 'Undergraduate Research - General', 'ENGR3820': 'Failure Analysis and Prevention', 'AHSE0112': 'The Olin ConductorlessOrchestra', 'ISR0098': 'Independent Study', 'SCI1410': 'Materials Science and SolidState Chemistry with lab', 'AHSE1199A': 'Arts, Humanities, Social ScienceFoundation Topic', 'MTH2110': 'Discrete Math', 'ENGR1200': 'Design Nature', 'ENGR2350': 'Thermodynamics', 'ENGR3899': 'Special Topics in MaterialsScience', 'ENGR2699': 'Special Topics in Bioengineering', 'ENGR2199C': 'Special Topics in Engineering', 'ELE1090': 'Environment and Health', 'ENGR3699A': 'Special Topics in BioEngineering', 'MTH2199A': 'Special Topics in Mathematics', 'MTH2199B': 'Special Topics in Mathematics', 'MTH2199C': 'Special Topics in Mathematics', 'ENGR3345B': 'Dynamic Systems', 'ENGR3345A': 'Mechanical and Aerospace Systems', 'ENGR1121': 'Real World Measurements', 'AHSE1110': 'History of TechnologyFoundation: Technology, Societyand the Environment', 'AHSE1111': 'Responsive Drawing and VisualThinking', 'AHSE1199D': 'Arts, Humanities, Social ScienceFoundation Topic', 'AHSE1199E': 'Arts, Humanities, Social ScienceFoundation Topic', 'MTH1120': 'Vector Calculus', 'ENGR3530': 'Synchronization', 'ENGR3240': 'Distributed Engineering Design', 'AHSE1199B': 'Arts, Humanities, Social ScienceFoundation Topic', 'AHSE1199': 'Arts, Humanities, Social ScienceFoundation Topic', 'SCI3130': 'Advanced Classical Mechanics', 'SCI1130': 'Physics: Mechanics', 'AHSE1199H': 'Arts, Humanities, Social ScienceFoundation Topic', 'ENGR2199A': 'Special Topics in Engineering'}

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
	c_ID = request.GET.get('coursesearch', 'error')
	if coursetitledict.get(c_ID, "error")=="error":
		return render(request, "courses/mainpage.jade", {"error":"true"})
	searched_course = Course.objects.get(name = c_ID)
	#print searched_course
	ratio = MFRatio(searched_course)
	#print ratio
	pop = popularityOfCourse(searched_course)
	return render(request,'courses/mainpage.jade',{'coursetitle': coursetitledict[str(searched_course)], 'courseID':searched_course,'males':ratio["males"], 'females': ratio["females"],'popularityME':pop["ME"], 'popularityECE':pop["ECE"], 'popularityEConcentration':pop["EConcentration"], 'popularityUndeclared':pop["Undeclared"]})



#ANYTHING ABOVE THIS POINT SHOULD WORK/HAS BEEN CHECKED----------------------------
	
def advanceSearch(request):
	""" for the advanced search page - replaces the original split function & references splitside.jade """
	majors_wanted = request.GET.getlist("majorsplit")
	colors_wanted = request.GET.getlist("colorsplit")
	#years_wanted = HttpRequest.getlist.GET("yearsplit")
	courses = []
	#print majors_wanted
	if len(majors_wanted) != 0:
		allcourses = []
		for major in majors_wanted:
			#print "major"
			#print major
			if major != "all":
				allc = Student.objects.filter(stumaj = major).courses.all()
				for c in allco:
					if c.name not in allcourses:
						allcourses.append(c.name)

	return render(request, 'courses/mainpage.jade', {'courses': allcourses})
	'''
		for m in specifiedMajors:
			print m
			if m not in courses:
				courses.append(m)
	print "I AM HERE"
	if len(colors_wanted) != 0:
		choices = Course.objects.all()
		for course in choices:
			for color in colors_wanted:
				print "color"
				print color
				if color in course.name:
					if course not in courses:
						print course
						courses.append(course)	
	print courses
	'''
	return render(request, 'courses/mainpage.jade', {"courses": allcourses})
'''
def courseSearch(request):
	""" for the individual course search page """
	#TODO swap C_ID with C_Name if/when it exists
	c_ID = request.GET.get('coursesearch', "error");
	#print c_ID
	searched_course = Course.objects.get(name = c_ID)
	#print searched_course
	ratio = MFRatio(searched_course)
	#print ratio
	pop = popularityOfCourse(searched_course)
	return render(request,'courses/mainpage.jade',{'courseID':searched_course,'males':ratio["males"], 'females': ratio["females"],'popularityME':pop["ME"], 'popularityECE':pop["ECE"], 'popularityEConcentration':pop["EConcentration"], 'popularityUndeclared':pop["Undeclared"]})
'''
def MFRatio(course):
	""" takes in specified course and parses it - calculating the # of males and # of females
output: ratio of male:female """
	m = course.student_set.filter(stugen = "M").count()
	f = course.student_set.filter(stugen = "F").count()
	total = m+f
	males = float(m)/total * 100
	females = float(f)/total * 100
	return {'males':males, 'females':females}

#HERE IS THE REAL COMPARE FUNCTION!
def compare(request):
	error = 'NONE'
	#compare_courses = []
	""" for the comparator page"""

	if request.GET['cc0']:
		compare_course_0 = request.GET['cc0']
		search0 = Course.objects.get(name = compare_course_0)
		print compare_course_0
		ratio = MFRatio(search0)
		print ratio
		#print cc0
		#compare_courses.append(cc0)
	else:
		#return error
		error = 'INCOMPLETE'
	if request.GET['cc1']:
		#compare_course_1 = request.GET['cc1']
		#compare1 = Course.objects.get(name = compare_course_1)
		#cc1 = compare1.objects.filter(name = compare_course1)
		#compare_courses.append(cc1)
		compare_course_1 = request.GET['cc1']
		search1 = Course.objects.get(name = compare_course_1)
		print compare_course_1
		ratio1 = MFRatio(search1)
		print ratio1
	else:
		#return error
		if error == 'INCOMPLETE':
			error = 'INCOMPLETE1' 
		else:
			#error = 'INCOMPLETE'
			error = 'EMPTY'
	print error	
	if error != 'NONE':
		return render(request, 'courses/mainpage.jade', {'compare_courses': error,'error':error})
	else:
		cc0stuCount = search0.student_set.all().count()
		cc1stuCount = search1.student_set.all().count()
		return render(request, 'courses/mainpage.jade',{'course_0':compare_course_0,'course_1': compare_course_1,'coursetitle0': coursetitledict['ENGR3240'], 'coursetitle1':coursetitledict['MTH1120'], 'maleratio':ratio['males'],'femaleratio':ratio['females'],'male1ratio':ratio1['males'],'female1ratio':ratio1['females'],'cc0stuCount': cc0stuCount, 'cc1stuCount':cc1stuCount})

#TODO: MOD COURSES.JS IF 3rd (CC2) IS WANTED 
	#if request.GET['cc2']:
	#	compare_course_2 = request.GET['cc2']
	#	cc2 = Datapoint.objects.filter(coursemajor = compare_course_2) | Datapoint.objects.filter(courseID = compare_course_2)
	#	compare_courses.append(cc2)
	#else:
	#	if error == 'INCOMPLETE1':	
	#		error = 'EMPTY'

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
