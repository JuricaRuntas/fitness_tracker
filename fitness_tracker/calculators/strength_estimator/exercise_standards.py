import math
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg

class LiftStandards:
  def __init__(self, exercise, age_range, gender, units):
    self.exercise = exercise
    self.age_range = age_range
    self.gender = gender
    self.units = units
    self.lift_standard = self.create_standard()

  def create_standard(self):
    if self.gender == "Male":
      if self.exercise == "Bench Press":
        return self.create_age_group_standard(male_bench_press_kg, self.age_range)
      elif self.exercise == "Deadlift":
        return self.create_age_group_standard(male_deadlift_kg, self.age_range)
      elif self.exercise == "Squat":
        return self.create_age_group_standard(male_squat_kg, self.age_range)
    
    elif self.gender == "Female":
      if self.exercise == "Bench Press":
        return self.create_age_group_standard(female_bench_press_kg, self.age_range)
      elif self.exercise == "Deadlift":
        return self.create_age_group_standard(female_deadlift_kg, self.age_range)
      elif self.exercise == "Squat":
        return self.create_age_group_standard(female_squat_kg, self.age_range)
  
  def standard(self):
    return self.lift_standard

  def create_age_group_standard(self, standards, age_range):
    percentages = {"14-17": 13/100, "18-23": 2/100,
                   "24-39": 0/100, "40-49": 5/100,
                   "50-59": 17/100, "60-69": 31/100,
                   "70-79": 45/100, "80-89": 56/100}
    age_group_standards = [standards[0]]
    
    if self.units == "lb":
      old_standards = standards
      standards = []
      for bodyweight_group in old_standards[1:]:
        converted_weight = []
        for weight in map(kg_to_pounds, bodyweight_group):
          index = bodyweight_group.index(round(pounds_to_kg(weight)))
          if index == 0:
            # round number to next 10
            if int(str(int(weight))[-1]) > 4: weight = math.ceil(weight/10.0)*10
            # round number to previous 10
            elif int(str(int(weight))[-1]) <= 4: weight = math.floor(weight/10.0)*10
          converted_weight.append(round(weight))
        standards.append(converted_weight)

    for age_group in standards:
      if isinstance(age_group[0], str): continue
      bodyweight = age_group[0]
      weight = list(map(lambda n: round(n - (n * percentages[age_range])), age_group[1:]))
      weight.insert(0, bodyweight)
      age_group_standards.append(weight)
    return age_group_standards

male_bench_press_kg = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                       [50, 23, 37, 55, 77, 102],
                       [55, 28, 43, 63, 86, 112],
                       [60, 33, 49, 70, 95, 121],
                       [65, 38, 55, 77, 103, 130],
                       [70, 43, 61, 84, 110, 139],
                       [75, 47, 67, 91, 118, 147],
                       [80, 52, 72, 97, 125, 155],
                       [85, 57, 78, 103, 132, 163],
                       [90, 61, 83, 109, 139, 171],
                       [95, 65, 88, 115, 145, 178],
                       [100, 70, 93, 121, 152, 185],
                       [105, 74, 98, 126, 158, 192],
                       [110, 78, 102, 131, 164, 199],
                       [115, 82, 107, 137, 170, 205],
                       [120, 86, 112, 142, 176, 211],
                       [125, 90, 116, 147, 181, 217],
                       [130, 94, 120, 152, 187, 223],
                       [135, 98, 125, 156, 192, 229],
                       [140, 101, 129, 161, 197, 235]]

female_bench_press_kg = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                         [40, 8, 18, 31, 49, 69],
                         [45, 10, 21, 35, 54, 75],
                         [50, 13, 24, 39, 58, 80],
                         [55, 15, 26, 43, 63, 85],
                         [60, 17, 29, 46, 67, 90],
                         [65, 19, 32, 49, 71, 95],
                         [70, 21, 34, 52, 74, 99],
                         [75, 22, 37, 55, 78, 103],
                         [80, 24, 39, 58, 81, 107],
                         [85, 26, 41, 61, 85, 111],
                         [90, 8, 44, 64, 88, 114],
                         [95, 30, 46, 66, 91, 118],
                         [100, 31, 48, 69, 94, 121],
                         [105, 33, 50, 71, 97, 124],
                         [110, 34, 52, 74, 99, 127],
                         [115, 36, 54, 76, 102, 130],
                         [120, 38, 56, 78, 105, 133]]

male_deadlift_kg = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                    [50, 43, 64, 91, 123, 158],
                    [55, 50, 73, 102, 136, 173],
                    [60, 57, 82, 113, 148, 186],
                    [65, 65, 91, 123, 159, 199],
                    [70, 72, 99, 132, 170, 211],
                    [75, 79, 107, 142, 181, 223],
                    [80, 85, 115, 151, 191, 234],
                    [85, 92, 123, 159, 201, 245],
                    [90, 98, 130, 168, 211, 256],
                    [95, 105, 137, 176, 220, 266],
                    [100, 111, 144, 184, 229, 276],
                    [105, 117, 151, 192, 237, 285],
                    [110, 123, 158, 199, 246, 294],
                    [115, 129, 164, 207, 254, 303],
                    [120, 134, 171, 214, 262, 312],
                    [125, 140, 177, 221, 269, 320],
                    [130, 145, 183, 228, 277, 328],
                    [135, 151, 189, 234, 284, 336],
                    [140, 156, 195, 241, 291, 344]]

female_deadlift_kg =  [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                       [40, 24, 40, 62, 89, 119],
                       [45, 27, 45, 68, 96, 127],
                       [50, 31, 49, 73, 102, 134],
                       [55, 34, 53, 78, 108, 141],
                       [60, 37, 57, 83, 113, 147],
                       [65, 40, 61, 88, 119, 153],
                       [70, 43, 65, 92, 124, 158],
                       [75, 46, 68, 96, 128, 164],
                       [80, 49, 71, 100 ,133, 169],
                       [85, 51, 74, 103, 137, 173],
                       [90, 54, 77, 107, 141, 178],
                       [95, 56, 80, 110, 145, 182],
                       [100, 59, 83, 114, 149, 187],
                       [105, 61, 86, 117, 152, 191],
                       [110, 63, 88, 120, 156, 195],
                       [115, 65, 91, 123, 159, 198],
                       [120, 67, 93, 126, 162, 202]]

male_squat_kg = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                 [50, 33, 51, 75, 103, 134],
                 [55, 39, 59, 84, 114, 147],
                 [60, 46, 67, 94, 125, 159],
                 [65, 52, 75, 103, 136, 171],
                 [70, 58, 82, 112, 146, 183],
                 [75, 65, 90, 120, 156, 194],
                 [80, 71, 97, 129, 165, 204],
                 [85, 77, 104, 137, 174, 214],
                 [90, 83, 111, 145, 183, 224],
                 [95, 88, 117, 152, 192, 233],
                 [100, 94, 124, 160, 200, 242],
                 [105, 99, 130, 167, 208, 251],
                 [110, 105, 136, 174, 216, 260],
                 [115, 110, 142, 181, 223, 268],
                 [120, 115, 148, 187, 231, 276],
                 [125, 120, 154, 194, 238, 284],
                 [130, 125, 160, 200, 245, 292],
                 [135, 130, 165, 206, 252, 299],
                 [140, 135, 171, 212, 258, 307]]

female_squat_kg = [["Bodyweight", "Beginner", "Novice", "Intermediate", "Advanced", "Elite"],
                   [40, 18, 32, 51, 75, 101],
                   [45, 21, 36, 56, 81, 109],
                   [50, 24, 40, 61, 87, 115],
                   [55, 27, 43, 65, 92, 122],
                   [60, 29, 47, 70, 97, 127],
                   [65, 32, 50, 74, 102, 133],
                   [70, 34, 53, 78, 106, 138],
                   [75, 37, 56, 81, 111, 143],
                   [80, 39, 59, 85, 115, 148],
                   [85, 42, 62, 88, 119, 152],
                   [90, 44, 65, 92, 123, 156],
                   [95, 46, 68, 95, 126, 161],
                   [100, 48, 70, 98, 130, 164],
                   [105, 50, 73, 101, 133, 168],
                   [110, 52, 75, 103, 136, 172],
                   [115, 54, 77, 106, 139, 175],
                   [120, 56, 80, 109, 143, 179]]
