class Graduating_Class:

  # requirements is a list of Courses 
  def __init__(self, requirements, grad_year):
    self.requirements = requirements
    self.grad_year = grad_year

  def __str__(self):
    grad_class_str = grad_year + ": "
    for requirement in range(len(self.requirements)):
      grad_class_str += str(requirement) + " ,"