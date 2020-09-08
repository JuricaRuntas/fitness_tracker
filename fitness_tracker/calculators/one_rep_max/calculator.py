import numpy as np
import math

class Calculator:
  def __init__(self, weight, repetitions):
    self.weight = int(weight)
    self.repetitions = int(repetitions)
    self.calculate()

  def calculate(self):
    one_rep_max = self.weight*(36/(37-self.repetitions)) # Brzycki formula 
    self.percentages = np.array([int(one_rep_max*50/100), int(one_rep_max*60/100),
                            int(one_rep_max*70/100), int(one_rep_max*80/100),
                            int(one_rep_max*90/100), int(one_rep_max),
                            int(one_rep_max*102/100)])

    for x in self.percentages:
      index = np.where(self.percentages==x)
      # round number to next nearest ten if last digit is greater than 6
      if int(str(x)[-1]) > 6: x = math.ceil(x/10.0)*10
      # round number to previous nearest ten if last digit is smaller than 4
      elif int(str(x)[-1]) < 4: x = math.floor(x/10.0)*10
      # if digit is 4, 5 or 6, round last digit to 5
      else: x = int(str(x)[:-1]+str(5))
      self.percentages[index] = x
    
    return self.percentages

  def results(self):
    return self.percentages
