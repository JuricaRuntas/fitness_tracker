import unittest
from fitness_tracker.calculators.body_fat.body_fat_formulas import *
from fitness_tracker.calculators.body_fat.body_fat_calculator import BodyFatCalculator

class TestFormulas(unittest.TestCase):
  def test_male_navy_USC(self):
    self.assertEqual(round(male_navy_USC(37.5, 19.5, 70.5), 1), 15.3)

  def test_male_navy_SI(self):
    self.assertEqual(round(male_navy_SI(96, 50, 178), 1), 15.7)

  def test_female_navy_USC(self):
    self.assertEqual(round(female_navy_USC(37.5, 19.5, 70.5, 34.5), 1), 21.8)

  def test_female_navy_SI(self):
    self.assertEqual(round(female_navy_SI(96, 50, 178, 92), 1), 24.1)

  def test_male_BMI_USC(self):
    self.assertEqual(round(male_BMI_USC(152, 70.5, 25), 1), 15.3)

  def test_male_BMI_SI(self):
    self.assertEqual(round(male_BMI_SI(70, 178, 25), 1), 16.1)

  def test_female_BMI_USC(self):
    self.assertEqual(round(female_BMI_USC(152, 70.5, 25), 1), 26.1)

  def test_female_BMI_SI(self):
    self.assertEqual(round(female_BMI_SI(70, 178, 25), 1), 26.9)

class TestCalculator(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.maxDiff = None
    
    cls.age = 25
    
    cls.weight_USC = 152
    cls.height_USC = 70.5
    cls.neck_USC = 19.5
    cls.waist_USC = 37.5
    cls.hip_USC = 34.5
    
    cls.weight_SI = 70
    cls.height_SI = 178
    cls.neck_SI = 50
    cls.waist_SI = 96
    cls.hip_SI = 92
    
    cls.correct_results_male_USC = {'Body Fat Navy': 15.3, 'Body Fat BMI': 15.3,
                                    'Fat Mass': 23.2, 'Lean Body Mass': 128.8,
                                    'Ideal Body Fat': '10.5%', 'Body Fat Category': 'Fitness',
                                    'Body Fat To Lose To Reach Ideal': 7.3}
    cls.correct_results_female_USC = {'Body Fat Navy': 21.8, 'Body Fat BMI': 26.1,
                                      'Fat Mass': 33.2, 'Lean Body Mass': 118.8,
                                      'Ideal Body Fat': '18.4%', 'Body Fat Category': 'Fitness',
                                      'Body Fat To Lose To Reach Ideal': 5.2} 
    cls.correct_results_male_SI = {'Body Fat Navy': 15.7, 'Body Fat BMI': 16.1,
                                   'Fat Mass': 11.0, 'Lean Body Mass': 59.0,
                                   'Ideal Body Fat': '10.5%', 'Body Fat Category': 'Fitness',
                                   'Body Fat To Lose To Reach Ideal': 3.6}
    cls.correct_results_female_SI = {'Body Fat Navy': 24.1, 'Body Fat BMI': 26.9,
                                     'Fat Mass': 16.9, 'Lean Body Mass': 53.1,
                                     'Ideal Body Fat': '18.4%', 'Body Fat Category': 'Fitness',
                                     'Body Fat To Lose To Reach Ideal': 4.0}
  
  def test_male_USC(self):
    calc = BodyFatCalculator("male", self.age, self.weight_USC, self.height_USC,
                             self.neck_USC, self.waist_USC, "imperial", self.hip_USC)
    results = calc.get_results()
    self.assertDictEqual(results, self.correct_results_male_USC)
  
  def test_female_USC(self):
    calc = BodyFatCalculator("female", self.age, self.weight_USC, self.height_USC,
                             self.neck_USC, self.waist_USC, "imperial", self.hip_USC)
    results = calc.get_results()
    self.assertDictEqual(results, self.correct_results_female_USC)

  def test_male_SI(self):
    calc = BodyFatCalculator("male", self.age, self.weight_SI, self.height_SI,
                             self.neck_SI, self.waist_SI, "metric", self.hip_SI)
    results = calc.get_results()
    self.assertDictEqual(results, self.correct_results_male_SI)

  def test_female_SI(self):
    calc = BodyFatCalculator("female", self.age, self.weight_SI, self.height_SI,
                             self.neck_SI, self.waist_SI, "metric", self.hip_SI)
    results = calc.get_results()
    self.assertDictEqual(results, self.correct_results_female_SI)

if __name__ == "__main__":
  unittest.main()
