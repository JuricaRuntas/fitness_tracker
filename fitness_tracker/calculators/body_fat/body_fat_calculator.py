from .body_fat_formulas import *

class BodyFatCalculator:
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

    self.categorization_men = {"2-5%": "Essential Fat", "6-13%": "Athletes",
                               "14-17%": "Fitness", "18-25%": "Average", "25+%": "Obese"}

    self.calculate_body_fat()
    self.create_info()

  def calculate_body_fat(self):
    if self.units == "imperial":
      if self.gender == "male":
        bf_navy_USC = male_navy_USC(self.waist, self.neck, self.height)
        bf_BMI_USC = male_BMI_USC(self.weight, self.height, self.age)
      elif self.gender == "female":
        bf_navy_USC = female_navy_USC(self.waist, self.neck, self.height, self.hip)
        bf_BMI_USC = female_BMI_USC(self.weight, self.height, self.age)
      body_fat_mass = fat_mass(bf_navy_USC, self.weight)
      lean_mass = lean_body_mass(self.weight, body_fat_mass)
      
      self.results["Body Fat Navy"] = round(bf_navy_USC, 1)
      self.results["Body Fat BMI"] = round(bf_BMI_USC, 1)
      self.results["Fat Mass"] = round(body_fat_mass, 1)
      self.results["Lean Body Mass"] = round(lean_mass, 1)
    
    elif self.units == "metric":
      if self.gender == "male":
        bf_navy_SI = male_navy_SI(self.waist, self.neck, self.height)
        bf_BMI_SI = male_BMI_SI(self.weight, self.height, self.age)
      elif self.gender == "female":
        bf_navy_SI = female_navy_SI(self.waist, self.neck, self.height, self.hip)
        bf_BMI_SI = female_BMI_SI(self.weight, self.height, self.age)
      
      body_fat_mass = fat_mass(bf_navy_SI, self.weight)
      lean_mass = lean_body_mass(self.weight, body_fat_mass)
      
      self.results["Body Fat Navy"] = round(bf_navy_SI, 1)
      self.results["Body Fat BMI"] = round(bf_BMI_SI, 1)
      self.results["Fat Mass"] = round(body_fat_mass, 1)
      self.results["Lean Body Mass"] = round(lean_mass, 1)

  def create_info(self):
    if self.gender == "male":
      age_group = self.binary_search_helper(self.ideal_fat_men.keys(), self.age)
      self.results["Ideal Body Fat"] = self.ideal_fat_men[age_group]
    elif self.gender == "female":
      age_group = self.binary_search_helper(self.ideal_fat_women.keys(), self.age)
      self.results["Ideal Body Fat"] = self.ideal_fat_women[age_group]
    
    body_fat_categorization = list(self.categorization_men.keys()) if self.gender == "male" else list(self.categorization_women.keys())
    percentages = [percentage.rstrip("%").strip("+").split("-") for percentage in list(body_fat_categorization)]
    for item in percentages:
      if self.gender == "male" and int(self.results["Body Fat Navy"]) >= 25:
        self.results["Body Fat Category"] = self.categorization_men["25+%"]
      elif self.gender == "female" and int(self.results["Body Fat Navy"]) >= 32:
        self.results["Body Fat Category"] = self.categorization_women["32+%"]
      elif int(self.results["Body Fat Navy"]) >= int(item[0]) and int(self.results["Body Fat Navy"]) <= int(item[1]):
        if self.gender == "female":
          self.results["Body Fat Category"] = self.categorization_women["".join(["-".join(item), "%"])]
        elif self.gender == "male":
          self.results["Body Fat Category"] = self.categorization_men["".join(["-".join(item), "%"])]
    
    if self.results["Ideal Body Fat"] == "8.5%":
      diff_ideal_body_fat = round(self.results["Body Fat Navy"]-float(self.results["Ideal Body Fat"][0:3]), 1)
    else:
      diff_ideal_body_fat = round(self.results["Body Fat Navy"]-float(self.results["Ideal Body Fat"][0:4]), 1)
    
    weight_to_ideal_body_fat = round(fat_mass(diff_ideal_body_fat, self.weight), 1)
    self.results["Body Fat To Lose To Reach Ideal"] = weight_to_ideal_body_fat
  
  def binary_search_helper(self, arr, target):
    arr = list(arr)
    low = 0
    high = len(arr)-1
    while low < high:
      mid = (high+low)//2
      if arr[mid] == target: break
      elif arr[mid] > target: high = mid-1
      else: low = mid+1
    mid = (high+low)//2
    return arr[mid]
   
  def get_results(self):
    return self.results
