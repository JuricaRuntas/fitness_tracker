from .body_fat_formulas import *

class Calculator:
  def __init__(self, gender, age, weight, height, neck, waist, units, hip=None):
    self.gender = gender
    self.age = age
    self.weight = weight
    self.height = height
    self.neck = neck
    self.waist = waist
    self.hip = hip
    self.units = units
    self.results = {}
    
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

    self.categorization_men = {"02-05%": "Essential Fat", "06-13%": "Athletes",
                               "14-17%": "Fitness", "18-25%": "Average", "25+%": "Obese"}

    self.calculate_body_fat()
    self.create_info()

  def calculate_body_fat(self):
    if self.units == "imperial":
      if self.gender == "male":
        bf_navy_usc = male_navy_USC(self.waist, self.neck, self.height)
        bf_BMI_usc = male_BMI_USC(self.weight, self.height, self.age)
      elif self.gender == "female":
        bf_navy_usc = female_navy_USC(self.waist, self.neck, self.height, self.hip)
        bf_BMI_usc = female_navy_SI(self.waist, self.neck, self.height, self.hip)
      
      body_fat_mass = fat_mass(bf_navy_usc, self.weight)
      lean_mass = lean_body_mass(self.weight, body_fat_mass)
      
      self.results["Body Fat Navy"] = round(bf_navy_usc, 1)
      self.results["Body Fat BMI"] = round(bf_BMI_usc, 1)
      self.results["Fat Mass"] = round(body_fat_mass, 1)
      self.results["Lean Body Mass"] = round(lean_mass, 1)
    
    elif self.units == "metric":
      if self.gender == "male":
        bf_navy_si = male_navy_SI(self.waist, self.neck, self.height)
        bf_BMI_si = male_BMI_SI(self.weight, self.height, self.age)
      elif self.gender == "female":
        bf_navy_si = female_navy_SI(self.waist, self.neck, self.height, self.hip)
        bf_BMI_si = female_BMI_SI(self.weight, self.height, self.age)
      
      body_fat_mass = fat_mass(bf_navy_si, self.weight)
      lean_mass = lean_body_mass(self.weight, body_fat_mass)
      
      self.results["Body Fat Navy"] = round(bf_navy_si, 1)
      self.results["Body Fat BMI"] = round(bf_BMI_si, 1)
      self.results["Fat Mass"] = round(body_fat_mass, 1)
      self.results["Lean Body Mass"] = round(lean_mass, 1)

  def create_info(self):
    if self.gender == "male":
      self.results["Ideal Body Fat"] = self.ideal_fat_men[self.age]
    elif self.gender == "female": self.results["Ideal Body Fat"] = self.ideal_fat_women[self.age]
    
    for key, value in self.categorization_men.items():
      if key[0] == "0":
        if int(self.results["Body Fat Navy"]) >= int(key[1]) and int(self.results["Body Fat Navy"]) <= int(key[4]):
          self.results["Body Fat Category"] = value
      else:
        if key == "25%+" and int(self.results["Body Fat Navy"] >= 25): self.results["Body Fat Category"] = value
        elif int(self.results["Body Fat Navy"]) >= int(key[:2]) and int(self.results["Body Fat Navy"]) <= int(key[3:5]):
          self.results["Body Fat Category"] = value
    
    if self.results["Ideal Body Fat"] == "8.5%":
      diff_ideal_body_fat = round(self.results["Body Fat Navy"]-float(self.results["Ideal Body Fat"][0:3]), 1)
    else:
      diff_ideal_body_fat = round(self.results["Body Fat Navy"]-float(self.results["Ideal Body Fat"][0:4]), 1)
    
    weight_to_ideal_body_fat = round(fat_mass(diff_ideal_body_fat, self.weight), 1)
    self.results["Body Fat To Lose To Reach Ideal"] = weight_to_ideal_body_fat
    
  def get_results(self):
    return self.results
