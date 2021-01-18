from fitness_tracker.common.units_conversion import pounds_to_kg, imperial_to_metric_height
from fitness_tracker.user_profile.profile_db import fetch_units

class CalorieGoalCalculator:
  def __init__(self, age, gender, height, weight, activity_level, goal, weight_per_week):
    self.units = fetch_units()
    self.age = age
    self.gender = gender
    activity_factors = {"Maintain": 1, "Sedentary": 1.2, "Lightly active": 1.375,
                        "Moderately active": 1.550, "Very active": 1.725,
                        "Extra active": 1.9}
    self.activity_level = activity_factors[activity_level]
    if self.units == "imperial":
      self.height = imperial_to_metric_height(height["feet"], height["inches"])
      self.weight = pounds_to_kg(weight)
    else:
      self.height = height
      self.weight = weight
    self.goal = goal
    self.weight_per_week = weight_per_week
  
  def calculate_calorie_goal(self):
    if self.goal == "Maintain weight": return self.calculate_BMR()
    elif self.goal == "Weight loss": return self.calculate_weight_loss_goal(self.weight_per_week)
    elif self.goal == "Weight gain": return self.calculate_weight_gain_goal(self.weight_per_week)

  def calculate_BMR(self):
    """
    The Basal Metabolic Rate - amount of energy expended while at rest in a neutrally temperate environment, 
    and in a post-absorptive state (meaning that the digestive system is inactive, which requires about 12 hours of fasting).
    """
    equ = 10*self.weight+6.25*self.height-5*self.age # Mifflin-St Jeor Equation
    if self.gender == "male": equ += 5
    elif self.gender == "female": equ -= 161
    return round(equ*self.activity_level)

  def calculate_weight_loss_goal(self, weight_per_week):
    assert weight_per_week == 0.25 or weight_per_week == 0.5 or weight_per_week == 1 # kg
    calories_per_day = self.calculate_BMR()
    if weight_per_week == 0.25:
      return round(calories_per_day*0.89)
    elif weight_per_week == 0.5:
      return round(calories_per_day*0.78)
    elif weight_per_week == 1:
      return round(calories_per_day*0.56)
  
  def calculate_weight_gain_goal(self, weight_per_week):
    assert weight_per_week == 0.25 or weight_per_week == 0.5 or weight_per_week == 1 # kg
    calories_per_day = self.calculate_BMR()
    if weight_per_week == 0.25:
      return round(calories_per_day*1.11)
    elif weight_per_week == 0.5:
      return round(calories_per_day*1.22)
    elif weight_per_week == 1:
      return round(calories_per_day*1.44)
