import math

# USC - inches
# SI - centimeters

# BMI Helpers
def BMI_USC(weight, height):
  return 703*(weight/height**2)

def BMI_SI(weight, height):
  # height/100, convert passed height to meters
  return weight/(height/100)**2

# U.S Navy Method - Male
def male_navy_USC(waist, neck, height):
  return 86.010*math.log10(waist-neck)-70.041*math.log10(height)+36.76

def male_navy_SI(waist, neck, height):
  return 495/((1.0324-0.19077*math.log10(waist-neck))+0.15456*math.log10(height))-450

# U.S Navy Method - Female
def female_navy_USC(waist, neck, height, hip):
  return 163.205*math.log10(waist+hip-neck)-97.684*math.log10(height)-78.387

def female_navy_SI(waist, neck, height, hip):
  return 495/(1.29579-0.35004*math.log10(waist+hip-neck)+0.22100*math.log10(height))-450

# BMI Method - Male
def male_BMI_USC(weight, height, age):
  return 1.20*BMI_USC(weight, height)+0.23*age-16.2

def male_BMI_SI(weight, height, age):
  return 1.20*BMI_SI(weight, height)+0.23*age-16.2

# BMI Method - Female
def female_BMI_USC(weight, height, age):
  return 1.20*BMI_USC(weight, height)+0.23*age-5.4

def female_BMI_SI(weight, height, age):
  return 1.20*BMI_SI(weight, height)+0.23*age-5.4

def fat_mass(body_fat, weight):
  return body_fat/100*weight

def lean_body_mass(weight, fat_mass):
  return weight-fat_mass
