import unittest
from fitness_tracker.calculators.one_rep_max.one_rep_max_calculator import OneRepMaxCalculator

class TestOneRepMaxCalculator(unittest.TestCase):
  def test_metric_weight(self):
    weight = 120
    reps = 5
    calc = OneRepMaxCalculator(weight, reps)
    results = calc.results()
    one_rep_max = results[5]
    self.assertEqual(one_rep_max, 135)
    self.assertListEqual(results, [70, 80, 95, 110, 120, 135,  140])

  def test_imperial_weight(self):
    weight = 265
    reps = 5
    calc = OneRepMaxCalculator(weight, reps)
    results = calc.results()
    one_rep_max = results[5]
    self.assertEqual(one_rep_max, 300)
    self.assertListEqual(results, [150, 180, 210, 240, 270, 300, 305])

if __name__ == "__main__":
  unittest.main()
