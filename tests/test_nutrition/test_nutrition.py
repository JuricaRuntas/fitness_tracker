import unittest
import os
import json
import sqlite3
from datetime import datetime
from fitness_tracker.notes.nutrition.nutrition_db import (create_nutrition_table, insert_default_meal_plans_values,
                                                          fetch_nutrition_data, modify_meal, update_meal, rotate_meals)
from fitness_tracker.notes.nutrition.spoonacular import FoodDatabase
from nutrition_test_helpers import *

class TestNutrition(unittest.TestCase):
  def setUp(self):
    with sqlite3.connect("test.db") as conn:
      self.sqlite_connection = conn
      self.sqlite_cursor = conn.cursor()
    create_test_user(self.sqlite_connection)
    create_nutrition_table(self.sqlite_connection)
    insert_default_meal_plans_values(self.sqlite_connection)
  
  def tearDown(self):
    delete_test_user(test_user["email"])
    delete_test_from_nutrition(test_user["email"])
    os.remove("test.db")
  
  def test_create_nutrition_table(self):
    nutrition_columns = ("email", "calorie_goal", "meal_plans", "manage_meals")
    columns = fetch_nutrition_columns(self.sqlite_cursor)
    self.assertEqual(nutrition_columns, columns)
  
  def test_insert_default_meal_plan(self):
    days_in_a_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    default_meal_names = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meals = {"Past": [], "Present": [], "Future":[], "Current Week Number": int(datetime.now().strftime("%V"))}
    for time in meals:
      if not time == "Past" and not time == "Current Week Number":
        this_week_meals = {}
        for day in days_in_a_week:
          day_dict = {}
          for meal in default_meal_names:
            day_dict[meal] = []
          this_week_meals[day] = day_dict
        meals[time] = this_week_meals
    default_dict = {"meal_plans": meals, "manage_meals": default_meal_names}
    
    insert_default_meal_plans_values(self.sqlite_connection)
    fetched_default = fetch_default_meal_plans_values(self.sqlite_cursor)
    
    fetched_default_dict = json.loads(fetched_default[0])
    self.assertDictEqual(default_dict["meal_plans"], fetched_default_dict)
    
    fetched_default_manage_meals = json.loads(fetched_default[1])
    self.assertEqual(default_dict["manage_meals"], fetched_default_manage_meals)
  
  def test_fetch_nutrition_data(self):
    delete_test_user(test_user["email"])
    create_test_user(self.sqlite_connection)
    create_nutrition_table(self.sqlite_connection) 
    fetch_nutrition_data(self.sqlite_connection)
    nutrition_data = fetch_server_nutrition_data()[0][:-1]
    local_nutrition_data = fetch_local_nutrition_data(self.sqlite_cursor)[0][:-1]
    self.assertEqual(nutrition_data, local_nutrition_data)
  
  def test_rename_meal(self):
    fetched_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    fetched_local_meal_plans["Present"]["Tuesday"]["Snack 2"] = fetched_local_meal_plans["Present"]["Tuesday"]["Lunch"]
    del fetched_local_meal_plans["Present"]["Tuesday"]["Lunch"]

    modify_meal(action="Rename", meal_to_modify="Lunch", day="Tuesday", sqlite_connection=self.sqlite_connection, modify_to="Snack 2", this_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
    
    fetched_local_meal_plans["Future"]["Friday"]["My Meal 1"] = fetched_local_meal_plans["Future"]["Friday"]["Dinner"]
    del fetched_local_meal_plans["Future"]["Friday"]["Dinner"]

    modify_meal(action="Rename", meal_to_modify="Dinner", day="Friday", sqlite_connection=self.sqlite_connection, modify_to="My Meal 1", next_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
  
  def test_add_meal(self):
    fetched_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    
    fetched_local_meal_plans["Present"]["Monday"]["New meal 1"] = []
    modify_meal(action="Add", meal_to_modify="New meal 1", day="Monday", sqlite_connection=self.sqlite_connection, this_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
    
    fetched_local_meal_plans["Future"]["Tuesday"]["Meal 2"] = []
    modify_meal(action="Add", meal_to_modify="Meal 2", day="Tuesday", sqlite_connection=self.sqlite_connection, next_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
    
    fetched_local_meal_plans["Present"]["Monday"]["New meal 1"].append("*test food info*")
    update_meal("New meal 1", "*test food info*", "Monday", self.sqlite_connection, this_week=True)
    modify_meal(action="Add", meal_to_modify="New meal 1", day="Monday", sqlite_connection=self.sqlite_connection, this_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
  
  def test_delete_meal(self):
    fetched_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    
    del fetched_local_meal_plans["Present"]["Monday"]["Lunch"]
    modify_meal(action="Delete", meal_to_modify="Lunch", day="Monday", sqlite_connection=self.sqlite_connection, this_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)

    del fetched_local_meal_plans["Future"]["Friday"]["Dinner"]
    modify_meal(action="Delete", meal_to_modify="Dinner", day="Friday", sqlite_connection=self.sqlite_connection, next_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
  
  def test_update_meal(self):
    food_db = FoodDatabase()
    banana_id = food_db.food_search("Banana", 1)[0]["id"]
    banana_info = food_db.food_info(banana_id)
    fetched_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    
    fetched_local_meal_plans["Present"]["Monday"]["Breakfast"].append(banana_info)
    update_meal("Breakfast", banana_info, "Monday", self.sqlite_connection, this_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)
    
    fetched_local_meal_plans["Future"]["Saturday"]["Lunch"].append(banana_info)
    update_meal("Lunch", banana_info, "Saturday", self.sqlite_connection, next_week=True)
    new_local_meal_plans = json.loads(fetch_local_meal_plans(self.sqlite_cursor))
    self.assertDictEqual(fetched_local_meal_plans, new_local_meal_plans)

if __name__ == "__main__":
  unittest.main()
