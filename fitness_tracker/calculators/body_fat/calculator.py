import math

class Calculator:
  def __init__(self, gender, age, weight, height, neck, waist, units):
    self.gender = gender
    self.age = age
    self.weight = weight
    self.height = height
    self.neck = neck
    self.waist = waist
    self.units = units
    
    # Jackson & Pollard Ideal Body Fat Percentages
    self.ideal_fat_women = {20: "17.7%", 25: "18.4%", 30: "19.3%",
                            35: "21.5%", 40: "22.2%", 45: "22.9%",
                            50: "25.2%", 55: "26.3%"}

    self.ideal_fat_men = {20: "8.5%", 25: "10.5%", 30: "12.7%",
                          35: "13.7%", 40: "15.3%", 45: "16.4%",
                          50: "18.9%", 55: "20.9%"}
    
    # The American Council on Exercise Body Fat Categorization
    self.categorization_women = {"10-13%": "Essential Fat", "14-20%": "Athletes",
                                 "21-24%": "Fitness", "25-31%": "Average", "32+%": "Obese"}

    self.categorization_men = {"2-5%": "Essential Fat", "6-13%": "Athletes",
                               "14-17%": "Fitness", "18-25%": "Average", "25+%": "Obese"}

    self.calculate()

  def calculate(self):
    # Body fat percentage (BFP) for males
    if self.units == "inches":    
      # U.S. Navy Method
      # U.S. customary system (USC), inches
      usc_bfp = 86.010*math.log10(self.waist-self.neck)-70.041*math.log10(height)+36.76
       
      # BMI Method
      BMI_male_usc = 703*(self.weight/self.height**2)
      bmi_bfp = 1.20*BMI_male_usc+0.23*self.age-16.2
    else:
      # U.S. Navy Method
      # International System of Units, centimeters:
      si_bfp = 495/(1.0324-0.19077*math.log10(self.waist-self.neck)+0.15456*math.log10(self.height))-450
  
      # BMI Method
      BMI_male_si = self.weight/self.height**2
      bmi_bfp = 1.20*BMI_male_si+0.23*self.age-16.2
