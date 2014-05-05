class Course: 
  
  def __init__(self, title, section_title, course_number, total_number_of_students = 0):
    self.title = title
    self.section_title = section_title
    self.course_number = course_number
    self.total_number_of_students = total_number_of_students

  def __str__(self):
    return self.course_number + ' : ' + self.title + ' - ' + self.section_title

