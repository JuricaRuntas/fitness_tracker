import unittest
import os
from fitness_tracker.notes.nutrition.nutrition_db import create_nutrition_table
from nutrition_test_helpers import *

class TestNutrition(unittest.TestCase):
  def setUp(self):
    create_user_test_table("test_user_profile.db")
    create_nutrition_table("test.db")
    insert_nutrition_data(test_user["email"], "3250")

  def tearDown(self):
    delete_user_test_table()
    delete_test_from_nutrition(test_user["email"])
    os.remove("test.db")
    os.remove("test_user_profile.db")

  def test_create_nutrition_table(self):
    nutrition_columns = ("email", "calorie_goal")
    columns = fetch_nutrition_columns()
    self.assertEqual(nutrition_columns, columns)

if __name__ == "__main__":
  unittest.main()
