import unittest
from fitness_tracker.common.units_conversion import *

class TestUnitsConversion(unittest.TestCase):
  def test_pounds_to_kg(self):
    self.assertEqual(pounds_to_kg(175), 79.38)

  def test_kg_to_pounds(self):
    self.assertEqual(kg_to_pounds(70), 154.32)

  def test_inch_to_cm(self):
    self.assertEqual(inch_to_cm(5), 12.7)

  def test_cm_to_inch(self):
    self.assertEqual(cm_to_inch(5), 1.97)

  def test_metric_to_imperial_height(self):
    height = metric_to_imperial_height(183)
    self.assertEqual(height, (6, 0))

  def test_imperial_to_metric_height(self):
    height = imperial_to_metric_height(6, 0)
    self.assertEqual(height, 183)

if __name__ == "__main__":
  unittest.main()
