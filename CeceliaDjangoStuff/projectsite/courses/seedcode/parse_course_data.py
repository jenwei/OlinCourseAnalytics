import csv
from Student import *
from Course import *
from Course_Offering import *
from Graduating_Class import *
from Major import *
from Professor import *

def make_semesters_dict(start_year, end_year):
    """
    Maps the semester titles to numbers, for easier use in determining the order of semesters.
    The dictionary looks like this: 
        {'0203FA': 0, '0203SP': 1, '0304FA': 2, ... , '1314SP': 23}
    The start_year and end_year determine the beginning and end points of the dictionary.
    """
    start = start_year - 2000
    end = end_year - 2000
    semesters = {}
    for i in range((end - start)):
        temp_start = str(start + i)
        temp_end = str(start + i + 1)
        if len(temp_start) == 1:
            temp_start = '0' + temp_start
        if len(temp_end) == 1:
            temp_end = '0' + temp_end
        sem_fa = temp_start + temp_end + 'FA'
        sem_sp = temp_start + temp_end + 'SP' 
        semesters[sem_fa] = i * 2
        semesters[sem_sp] = i * 2 + 1
    return semesters


def get_course_data(filename):
    """
    Parses all of the course data from the specified filname and returns a list of 3 dictionarires: students,
    courses, and professors from which the data can be accessed and used. 
    This method assumes that the data is in a csv format and has the following column headings in this specific
    order:
        'Academic Status Code'
        'Degree Grant Year'
        'Student ID Number'
        'AcadYr_Session'
        'Gender Code'
        'Session Classification Code'
        'Session Major 1 Description'
        'Concentration 1 Description'
        'Course Work Course Number'
        'Section Number'
        'Course Work Course Title'
        'Section Title (Actual)'
        'Faculty Full Name (Last, First)'
    """
    students = {}       # key = id, value = Student
    courses = {}        # key = course_number, value = Course
    professors = {}     # key = name, value = Professor
    semester_list_per_student = {}
    validation_courses = {}

    # Setting the min and max years we're looking at, to set up the semesters dict
    # the min and max years will not necessarily be 2002 and 2014, this is just the minimum range
    min_year = 2002
    max_year = 2014

    with open(filename,'rU') as f:
        contents = csv.reader(f)
        matrix = list()
        for row in contents:
            academic_status = row[0].strip()
            grad_year = row[1].strip()
            stud_id = row[2].strip()
            course_semester = row[3].strip()
            gender = row[4].strip()
            student_semester_str = row[5].strip() # year when student took course (eg FF, FR, SO, ..)
            major = row[6].strip()
            concentration = row[7].strip()
            course_number = row[8].strip()
            section_no = row[9].strip()
            course_title = row[10].strip()
            section_title = row[11].strip()
            professor_name = row[12].strip()

            # Get rid of the header row with column titles
            if academic_status == 'Academic Status Code':
                continue

            # list of courses we don't want to include in our model, for various reasons listed below
            non_included_courses = [
                'ENGR3520A',    # Project that went along with FOCS one year
                'OIE1000',      # OIE
                'OIP1000',      # The Olin Internship Practicum
                'AHSE11BA',     # Babson Cross Registration
                'BAB5001',      # Babson Cross Registration
                'BAB1001',      # Babson Cross Registration
                'ENGR1510',     # Introductory Programming (no equivalent down the line)
                'CD1097',       # Curriculum Development Activity
                'E! CAP SPR',   # Entrepreneurship CapstoneSpring Pre-registration
                'SEM 401',      # Seminars
                'SEM 301',
                'SEM 302',
                'AHSE2141',     # Disregard AHS part of Engineering for Humanity
                'AHSE CAP SPR', # AHS CapstoneSpring Pre-registration
                'SCI10WE',      # Wellesley Cross Registration
                'ENGR3425',     # Analog VLSI didn't have an easy latter equivalent
                'ICB2',         # Lecture Component of ICB2, already accounted for in course numbers
                'ICB1',         # Lecture Component of ICB1, already accounted for in course numbers
                'MTH3130'       # Mathematical Analysis (2 cr) - 16 people - doesn't fit what came after well
            ]
            # Don't include the courses in the list above as well as lab classes and AHS Cap Pre-reg
            if ' L' in course_number or course_number in non_included_courses or course_title == 'AHS CapstoneSpring Pre-registration':
                continue

            
            """ Combine the course_semester and year into one meaningful variable that describes
                what the student's standing is at the time they take a course offering by semester
                number (from 0 to 7) """

            # Sometimes the freshman first semester is labeled as 'TF', change it to 'FF', which is more frequently used
            if student_semester_str == 'TF': student_semester_str = 'FF'
            
            student_semester_no = 0     # 'FF'

            if student_semester_str == 'FR':
                student_semester_no = 1
            elif student_semester_str == 'SO':
                student_semester_no = 2
            elif student_semester_str == 'JR':
                student_semester_no = 4
            elif student_semester_str == 'SR':
                student_semester_no = 6

            if 'SP' in course_semester: student_semester_no += 1


            
            """ Cleaning course data by setting equivalent course information """

            # AHS vs. AHSE problem, change everything to AHSE
            if 'AHS' in course_number and 'AHSE' not in course_number:
                course_number = course_number[:3] + 'E' + course_number[3:]

            # Entried in classes_to_convert contain pairs of course #s (left) to convert to equivalent course #s (right)
            # The SECOND course # should be the one that you want the FIRST course # to become
            classes_to_convert = [
                ('FND2490', 'ENGR2250'),    # FND UOCD
                ('FND1310', 'MTH1110'),     # FND Calculus - 2006
                ('FND1312', 'MTH1110'),     # FND Calculus - 2007
                ('FND2510', 'ENGR2410'),    # FND Sig Sys
                ('FND1510', 'ENGR1110'),    # FND Mod Con
                ('FND2610', 'AHSE1500'),    # FND FBE
                ('FND2240', 'SCI1410'),     # FND Mat Sci
                ('FND1210', 'SCI1111'),     # FND Physics side of Mod Sim (check on this, was called 'Physical Foundations ofEngineering I')
                ('FND1311', 'MTH2140'),     # FND Diff Eq
                ('FND1410', 'ENGR1200'),    # FND precursor to Design Nature
                ('FND1420', 'ENGR1121'),    # FND clocest thing we could get was Real World Measurements
                ('FND2350', 'MTH2130'),     # FND clocest thing is Prob Stat (Applied Mathematical Methods)
                ('FND2710', 'SCI1210'),     # FND Mod Bio
                ('AHS1110', 'AHSE1100'),    # AHS -> AHSE
                ('AHS1111', 'AHSE2131'),    # AHS -> AHSE
                ('AHS1140', 'AHSE2120'),    # AHS -> AHSE
                ('ELE1050', 'ENGR2510'),    # Software design (before it was Soft Des)
                ('ENG1510', 'ENGR2510'),    # Software design (before it was Soft Des)
                ('MTH3198', 'MTH4198'),     # Consolidating the 2 OSS in Mathematics
                ('ISR1300', 'MTH0098'),     # IS in Mathematics
                ('ISR1100', 'AHSE0198'),    # IS inArts Humanities Social Science
                ('AHSE3198', 'AHSE0198'),   # IS inArts Humanities Social Science
                ('AHSE1198', 'AHSE0198'),   # IS inArts Humanities Social Science
                ('SCI3098', 'SCI0098'),     # IS in theSciences
                ('SCI1098', 'SCI0098'),     # IS in theSciences
                ('ENGR3098', 'ENGR0098'),   # IS in Engineering
                ('ISR1500', 'ENGR0098'),    # IS/Research inComputing, Electrical orSystems -> IS in Engineering
                ('ISR2900', 'ENGR0098'),    # IS & ResearchTechnical Concepts -> IS in Engineering
                ('ISR1200', 'SCI0098'),     # IS & Research:Physical Concepts -> IS in theSciences
                ('ISR1020', 'AHSE0198'),    # IS & ResearchMusical Concepts -> IS inArts Humanities Social Science
                ('ISR1030', 'ENGR0098'),    # IS/Research inDesign Concepts -> IS in Engineering
                ('ISR1900', 'ENGR0098'),    # IS & ResearchTechnical Concepts -> IS in Engineering
                ('SCI1410A', 'SCI1410'),    # Mat Sci
                ('ELE2715', 'SCI2320'),     # Applied Organic Chemistry -> Organic Chemistry with Lab
                ('SCI1110', 'SCI1130'),     # Mechanics
                ('MEC1915', 'ENGR2320'),    # Mech Solids
                ('ENGR3320', 'ENGR2320'),   # Mech Solids
                ('SCI2220', 'ENGR2620'),    # Biomechanics
                ('SCI3110', 'SCI2130'),     # Modern Physics
                ('ENGR3812', 'SCI3120'),    # Solid State Physics
                ('SCI1121A', 'SCI1121'),    # E&M
                ('SCI1120', 'SCI1121'),     # E&M
                ('ENGR3290', 'ENGR4290'),   # ADE
                ('ENGR1120', 'ENGR1121'),   # Real World Measurements
                ('ENGR3380', 'ENGR3260'),   # DFM
                ('ENGR3340', 'ENGR2340'),   # Dynamics
                ('MEC2910', 'ENGR2350'),    # Thermodynamics
                ('ENGR3350', 'ENGR2350'),   # Thermodynamics
                ('MTH2310', 'MTH2110'),     # Discrete 
                ('ECE2910', 'ENGR2420'),    # Circuits
                ('MTH3140', 'ENGR3140'),    # Error control codes
                ('MTH1097', 'MTH0097'),     # Undergraduate Research inMathematics
                ('SCI1097', 'SCI0097'),     # Undergraduate Research in theSciences
                ('ENGR1097', 'ENGR0097'),   # Undergraduate Research inEngineering
                ('AHSE1197', 'AHSE0197'),   # Undergraduate Research inArts, Humanities, Social Science
                ('MTH1000', 'MTH1110'),     # Calculus
                ('MEC1000', 'ENGR1330'),    # Fundamentals of Machine ShopOperations
                ('AHSE1120', 'AHSE1100'),   # History of Tech
                ('AHSE3500', 'AHSE3599'),   # Entrepreneurship: Real TimeCase Study -> Special Topics in Business andEntrepreneurship
                ('AHSE1599', 'AHSE1500'),   # Entrepreneurship FoundationTopic -> FBE
                ('AHSE1140', 'AHSE1145'),   # Anthropology Foundation
                ('AHSE2140', 'AHSE1145'),   # Anthropology Foundation
                ('ENGR3430', 'ENGR3426'),   # Digital VLSI -> Mixed Analog-Digital VLSI I
                ('AHSE1135', 'AHSE1130'),   # Seeing and Hearing
                ('ELE1010', 'AHSE2131'),    # Responsive Drawing and VisualThinking
                ('MTH2150', 'MTH2130'),     # Applied Mathematical Methods -> Prob Stat
                ('AHSE3100', 'AHSE3199'),   # Leadership and Ethics
                ('ENGR1199A', 'ENGR1199'),  # Energy Systems in Urban Design
                ('ENGR3299A', 'ENGR3270'),  # Real Products, Real Markets
                ('ENGR3699', 'ENGR3630'),   # Transport in Biological Systems
                ('SCI2099B', 'SCI2099'),    # Special Topics: Art of Approximation
                ('SCI2199', 'ENGR3355'),    # Renewable Energy
                ('SCI3199', 'SCI2145'),     # High Energy Astrophysics
                ('MTH3199A', 'MTH3160'),    # Intro to Complex Variables
                ('ELE1025', 'AHSE1122'),    # Wired Ensemble
                ('ELE1020', 'AHSE1122')     # Wired Ensemble
            ]

            equivalent_courses = {} # keys = course #, values = equivalent course #
            
            # convert the list above to a dictionary
            for old, current in classes_to_convert:
                equivalent_courses[old] = current

            # Do the actual conversion of the course #s
            if course_number in equivalent_courses:
                course_number = equivalent_courses[course_number]
            
            
            """ SPECIAL MANIPULATIONS """

            # Digital Signal Processing used to be a Speical Topics
            if course_number == 'ENGR3499B' and 'Digital Signal Processing' in section_title:
                course_number = 'ENGR3415'
                course_title = 'Digital Signal Processing'
                section_title = ''

            # Preferred title for AHSE1102
            elif course_number == 'AHSE1102':
                course_title = 'Arts and Humanities: Self-Explored in Art and Philosp'

            # Foundation Topic in Physics
            elif course_number == 'SCI1199':
                # Phys of Conserv Laws: Energy Foc by Mechtenberg, Abigail 
                if course_title in 'Phys of Conserv Laws: Energy Foc' or 'Phys of Conserv Laws: Energy Foc' in course_title:
                    course_number = 'SCI1199A'
                # Phys of Conserv Laws: Waves
                else:
                    course_number = 'SCI1199B'

            # Linearity 1 and 2
            elif course_number == 'MTH2188':
                # Linearity 1's equivalent is Linear Algebra and Differential Equations for our purposes
                if section_title in 'Linearity 1' or 'Linearity 1' in section_title:
                    course_number = 'MTH2188A'
                # Linearity 2's equivalent is Vector Calculus for our purposes
                else:
                    course_number = 'MTH1120'

            # Two courses with ENGR3345
            elif course_number == 'ENGR3345':
                # Mechanical and Aerospace Systems
                if course_title in 'Mechanical and Aerospace Systems' or 'Mechanical and Aerospace Systems' in section_title:
                    course_number = 'ENGR3345A'
                # Dynamic Systems
                else:
                    course_number = 'ENGR3345B'

            # Some of the 'Heroes for the RenaissanceEngineer: Leonardo, Nabokov,Bach and Borodin' classes are misnumbered
            elif course_number == 'AHSE1145':
                if 'RenaissanceEngineer' in course_title:
                    course_number = 'AHSE2120'

            # Modern Physics had a previous number (same as Quantum Physics, oops!)
            elif course_number == 'SCI2130':
                # Modern Physics
                if course_title == 'Modern Physics':
                    course_number = 'SCI2130A'
                # Quantum Physics
                else:
                    course_number = 'SCI2130B'

            # Mod Con was previously called 'Engineering of Compartment Systems'
            elif course_number == 'ENGR1110':
                course_title = 'Modeling and Control'

            # Arts, Humanities, Social ScienceFoundation Topic
            # There were multiple courses with the same number but a different course, this corrects for that
            # creating new course numbers for courses that have a different subject but the same course number
            elif course_number == 'AHSE1199':
                # Art Since 1945: Movmt Theme Cntx
                if 'Art Since 1945' in section_title:
                    course_number = 'AHSE1199A'
                # Creative Writing Workshop
                elif 'Creative Wr' in section_title:
                    course_number = 'AHSE1199B'
                # How Supreme Court Shapes Amer
                elif 'How Supreme Court' in section_title:
                    course_number = 'AHSE1199C'
                # Islam and the West: Politic/Cult
                elif 'Islam' in section_title:
                    course_number = 'AHSE1199D'
                # Media Revolution:Activism & Tech
                elif 'Media Revolution' in section_title:
                    course_number = 'AHSE1199E'
                # Globalzatn: Culture Econ Politic
                elif 'Globalzatn' in section_title:
                    course_number = 'AHSE1199F'
                # Robots, Mutants & Monsters: Envi
                elif 'Robots, Mutants' in section_title:
                    course_number = 'AHSE1199G'
                # The Play's the Thing:Shakespeare
                elif 'Shakespeare' in section_title:
                    course_number = 'AHSE1199H'
                # Anthropology
                elif 'Human Connection' in section_title:
                    course_number = 'AHSE1145'
                # Identity from the Mind adn Brain
                elif 'Identity' in section_title:
                    course_number = 'AHSE1155'
                # Environment and Health
                elif 'Heath and the Urban' in section_title:
                    course_number = 'ELE1090'

            title_changes = [
                ('AHSE1100', 'History of Technology:A Cultural & Contextual Approach'),
                ('ENGR4190', 'Senior Capstone Program inEngineering (SCOPE)'),
                ('ENGR3426', 'Mixed Analog-Digital VLSI I'),
                ('ENGR2510', 'Software Design'),
                ('SCI2320', 'Applied Organic Chemistry'),
                ('SCI1111', 'Modeling and Simulation of thePhysical World'),
                ('MTH2140', 'Differential Equations'),
                ('MTH1110', 'Calculus'),
                ('AHSE0198', 'Independent Study in Arts, Humanities, Social Science'),
                ('SCI1121', 'Electricity and Magnetism'),
                ('MTH2130', 'Probability and Statistics'),
                ('AHSE1500', 'Foundations of Business andEntrepreneurship'),
                ('AHSE1130', 'Seeing and Hearing:Communicating with Photographs,Video and Sound'),
                ('ENGR2420', 'Intro Microelectronic Circuits'),
                ('AHSE1122', 'The Wired Ensemble -Instruments, Voices, Players'),
                ('SCI0098', 'Independent Study inScience'),
                ('SCI1410', 'Materials Science and SolidState Chemistry with lab'),
                ('ENGR1200', 'Design Nature'),
                ('ENGR0098', 'Independent Study in Engineering'),
                ('ENGR1121', 'Real World Measurements')
            ]

            for course_no, final_title in title_changes:
                if course_number == course_no:
                    course_title = final_title

            # Removing the X on the end of course numbers (For an IS)
            if course_number.endswith('X'):
                course_number = course_number[:-1]

            # Breaking Linearity and 2006's math blocks into their respective math courses 
            # MTH2188A ['Special Topics in Mathematics', 'Linearity 1']
            # FND1320  Mathematical Foundations ofEngineering II:  Linear Algebra and Vector Calculus
            """
            if course_number == 'MTH2188A' or course_number == 'FND1320':
                num_iterations = 2
                if course_number == 'MTH2188A':
                    course_numbers = ['MTH2120', 'MTH2140']
                    course_titles = ['Linear Algebra', 'Differential Equations']
                else:
                    course_numbers = ['MTH1120', 'MTH2120']
                    course_titles = ['Vector Calculus', 'Linear Algebra']
            else:
                num_iterations = 1

            """
            num_iterations =1 
            # Used to determine the number of people in each course for the 1314SP semester
            # Does not do anything for parsing the course data
            if course_semester == '1314SP':
                if course_number not in validation_courses:
                    validation_courses[course_number] = [course_number, course_title, section_title, professor_name, 1]
                else:
                    validation_courses[course_number][4] += 1

            # If a course number had more than one course assciated with it, the number of iterations below
            # will be two

            # This section puts the course information into our defined objects
            for i in range(num_iterations):
                if num_iterations == 2:
                    course_number = course_numbers[i]
                    course_title = course_titles[i]
                    section_title = ''

                courses[course_number] = courses.get(course_number, Course(course_title, section_title, course_number))
                course = courses[course_number]
                course.total_number_of_students += 1
                professors[professor_name] = professors.get(professor_name, Professor(professor_name))
                course_offering = Course_Offering(course_semester, student_semester_no, section_no, course)
                course_offering.set_professor(professors[professor_name])
                course_offering.enrollment += 1


            # Add student to the list of students we'll return
            if stud_id not in students:
                #(self, ID, gender, graduating_class, major, academic_status)
                new_student = Student(stud_id, gender, grad_year, major, academic_status, concentration)
                students[stud_id] = new_student

            # add the course to the student's list of courses they've taken
            students[stud_id].add_course_offering(course_offering)

            # build up the list of all semesters that the student took courses in 
            if stud_id in semester_list_per_student:
                if course_semester not in semester_list_per_student[stud_id]:
                    semester_list_per_student[stud_id].append(course_semester)
            else:
                semester_list_per_student[stud_id] = [course_semester]

            # Set the students' major
            if students[stud_id].major == 'Undeclared' and major != 'Undeclared':
                students[stud_id].major = major

            students[stud_id].major_history[student_semester_no] = major

            # Setting the min and max years based on the course_semester data
            if int(course_semester[:2]) < (min_year - 2000):
                min_year = 2000 + int(course_semester[:2])
            elif int(course_semester[2:4]) > (max_year - 2000): 
                max_year = 2000 + int(course_semester[2:4])

    semesters = make_semesters_dict(min_year, max_year)

    for s in students:
        students[s].set_first_semester(semester_list_per_student[s], semesters)
        students[s].set_final_semester()
        students[s].set_major_history()

    # To get the Course data for Sp 2014

    # for c1 in validation_courses:
    #     # course ids
    #     print validation_courses[c1][0]
    # for c2 in validation_courses:
    #     # course title
    #     output = validation_courses[c2][1]
    #     if len(validation_courses[c2][2]) > 0:
    #         output += ": " + validation_courses[c2][2]
    #     print output
    # for c3 in validation_courses:
    #     # prof
    #     print validation_courses[c3][3]
    # for c4 in validation_courses:
    #     # number of students
    #     print validation_courses[c4][4]

    return [students, courses, professors]

if __name__=="__main__":
    get_course_data('course_enrollments_2002-2014spring_anonymized.csv')



