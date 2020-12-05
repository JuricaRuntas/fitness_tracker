import math

class OneRepMaxCalculator:
  def __init__(self, weight, repetitions):
    self.weight = int(weight)
    self.repetitions = int(repetitions)
    self.percentages = self.calculate()

  def calculate(self):
    one_rep_max = self.weight*(36/(37-self.repetitions)) # Brzycki formula 
    percentages = [int(one_rep_max*50/100), int(one_rep_max*60/100),
                            int(one_rep_max*70/100), int(one_rep_max*80/100),
                            int(one_rep_max*90/100), int(one_rep_max),
                            int(one_rep_max*102/100)]

    for percentage in percentages:
      index = percentages.index(percentage)
      # round number to next nearest ten if last digit is greater than 6
      if int(str(percentage)[-1]) > 6: percentage = math.ceil(percentage/10.0)*10
      # round number to previous nearest ten if last digit is smaller than 4
      elif int(str(percentage)[-1]) < 4: percentage = math.floor(percentage/10.0)*10
      # if digit is 4, 5 or 6, round last digit to 5
      else: percentage = int(str(percentage)[:-1]+str(5))
      percentages[index] = percentage
    
    return percentages

  def results(self):
    return self.percentages
