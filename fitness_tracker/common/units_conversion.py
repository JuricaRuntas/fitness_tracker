import math

def pounds_to_kg(lbs):
  return round(float(lbs)/2.2046, 2)

def kg_to_pounds(kg):
  return round(float(kg)*2.2046, 2)

def inch_to_cm(inch):
  return round(float(inch)*2.54, 2)

def cm_to_inch(cm):
  return round(float(cm)/2.54, 2)

def metric_to_imperial_height(cm):
  inches_total = cm_to_inch(float(cm))
  feet = math.floor(inches_total/12)
  inches = round(inches_total - 12*feet)
  return feet, inches

def imperial_to_metric_height(feet, inches):
  feet_to_cm = inch_to_cm(float(feet)*12)
  inches_to_cm = inch_to_cm(float(inches))
  return math.ceil(feet_to_cm+inches_to_cm)
