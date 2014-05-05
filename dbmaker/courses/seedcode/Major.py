class Major:

  def __init__(self, name, concentration, requirements):
    self.name = name
    self.concentration = concentration
    self.requirements = requirements

  def __str__(self):
    return self.name + " - " + self.concentration