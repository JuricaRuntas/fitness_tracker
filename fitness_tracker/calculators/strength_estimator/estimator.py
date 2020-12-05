from .exercise_standards import LiftStandards

class StrengthLevelEstimator:
  def __init__(self, gender, age_range, bodyweight, exercise, one_RM, units):
    self.gender = gender
    self.age = age_range
    self.bodyweight = bodyweight
    self.exercise = exercise
    self.one_RM = one_RM
    self.units = units
    self.lift_standard = LiftStandards(exercise, age_range, gender, self.units).standard()

  def standard(self):
    return self.lift_standard
  
  def find_strength_group(self):
    if self.gender == "Male" and self.units == "kg": bodyweight_groups = [bodyweight_group for bodyweight_group in range(50, 145, 5)]
    elif self.gender == "Female" and self.units == "kg": bodyweight_groups = [bodyweight_group for bodyweight_group in range(40, 125, 5)]
    elif self.gender == "Male" and self.units == "lb": bodyweight_groups = [bodyweight_group for bodyweight_group in range(110, 320, 10)]
    elif self.gender == "Female" and self.units == "lb": bodyweight_groups = [bodyweight_group for bodyweight_group in range(90, 270, 10)]

    bodyweight_group = self.binary_search(bodyweight_groups, self.bodyweight)
    for standard in self.lift_standard:
      if standard[0] == bodyweight_group: bodyweight_standard = standard
    exercise_weight = bodyweight_standard.index(self.binary_search(bodyweight_standard, self.one_RM))
    if exercise_weight == 0: return self.lift_standard[0][1]
    else: return self.lift_standard[0][exercise_weight]

  def binary_search(self, arr, target):
    low = 0
    high = len(arr)-1

    if target <= arr[0]: return arr[0]
    if target >= arr[-1]: return arr[-1]

    while low < high:
      mid = (low+high)//2
      if arr[mid] == target: return arr[mid]
      elif target < arr[mid]:
        if target > arr[mid-1]:
          if target-arr[mid-1] >= arr[mid]-target: return arr[mid]
          else: return arr[mid-1]
        high = mid
      else:
        if mid < len(arr)-1 and target < arr[mid+1]:
          if target-arr[mid] >= arr[mid+1]-target: return arr[mid+1]
          else: return arr[mid]
        low = mid+1
    return arr[mid]

  def lift_weight_ratio(self):
    return round(self.one_RM/self.bodyweight, 2)
