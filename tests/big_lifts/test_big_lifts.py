import unittest
import sqlite3
import json
import os
from fitness_tracker.notes.big_lifts.big_lifts_db import (create_big_lifts_table, insert_default_values,
                                                         fetch_user_big_lifts_table_data, update_big_lifts_units,
                                                         update_1RM_lifts, update_lifts_for_reps)
from big_lifts_test_helpers import *

class TestBigLifts(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
    one_RM = json.dumps({exercise: "0" for exercise in default_exercises})
    lifts_for_reps = json.dumps({exercise: ["0", "0"] for exercise in default_exercises})
    preferred_lifts = json.dumps({"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                                  "Squat": "Back Squat", "Vertical Press": "Overhead Press"})
    cls.default_values = {"1RM": one_RM, "lifts_for_reps": lifts_for_reps,
                      "preferred_lifts": preferred_lifts, "email": test_user["email"],
                      "units": test_user["units"]} 

  def tearDown(self):
    os.remove("test.db")
  
  def test_create_big_lifts_table(self):
    big_lifts_columns = ("email", "1RM", "lifts_for_reps",
                         "preferred_lifts", "lift_history",
                         "units")
    create_big_lifts_table("test.db")
    columns = fetch_big_lifts_columns()
    self.assertEqual(big_lifts_columns, columns)

  def test_insert_default_values(self):
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
    
    big_lifts_data = fetch_big_lifts_data(test_user["email"])[0]
    
    fetched_email = big_lifts_data[0]
    fetched_one_RM = big_lifts_data[1]
    fetched_lifts_for_reps = big_lifts_data[2]
    fetched_preferred_lifts = big_lifts_data[3]
    fetched_units = big_lifts_data[5]

    fetched_default_values = {"1RM": fetched_one_RM, "lifts_for_reps": fetched_lifts_for_reps,
                              "preferred_lifts": fetched_preferred_lifts, "email": fetched_email,
                              "units": fetched_units}

    self.assertDictEqual(fetched_default_values, self.default_values)
  
  def test_fetch_user_big_lifts_data(self):
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
    os.remove("test.db")
    create_big_lifts_table("test.db")
    fetch_user_big_lifts_table_data("test.db", "test_user_profile.db")
    big_lifts_data = fetch_big_lifts_data(test_user["email"])[0][:-1]
    local_big_lifts_data = fetch_local_big_lifts_data("test.db")[0][:-1]
    self.assertEqual(local_big_lifts_data, big_lifts_data)

  def test_update_units(self):
    table_name = "".join([test_user["email"], "_table"])
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
    new_units = "imperial"
    update_test_user_table_units(new_units, "test_user_profile.db", table_name)
    update_big_lifts_units("test.db", "test_user_profile.db")
    units = fetch_local_big_lifts_units("test.db")
    self.assertEqual(new_units, units)
  
  def test_update_1RM_lifts(self):
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
    new_values = {"Bench Press": "100", "Deadlift": "200",
                  "Back Squat": "300", "Overhead Press": "400"}
    update_1RM_lifts(new_values, path=["test_user_profile.db", "test.db"])
    one_rep_maxes = fetch_1RM_lifts("test.db", test_user["email"])
    
    server_1RM = json.loads(one_rep_maxes[0])
    self.assertEqual(new_values, server_1RM)

    local_1RM = json.loads(one_rep_maxes[1])
    self.assertEqual(new_values, local_1RM)
  
  def test_update_lifts_for_reps(self):
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
    new_values = {"Bench Press": ["10", "100"], "Deadlift": ["3", "250"],
                  "Back Squat": ["5", "200"], "Overhead Press": ["1", "100"]}
    update_lifts_for_reps(new_values, path=["test_user_profile.db", "test.db"])
    lifts_for_reps = fetch_lifts_for_reps("test.db", test_user["email"])
    
    server_lifts_for_reps = json.loads(lifts_for_reps[0])
    self.assertEqual(new_values, server_lifts_for_reps)
    
    local_lifts_for_reps = json.loads(lifts_for_reps[1])
    self.assertEqual(new_values, local_lifts_for_reps)

if __name__ == "__main__":
  create_user_test_table()
  unittest.main(exit=False)
  delete_test_from_big_lifts(test_user["email"])
  os.remove("test_user_profile.db")
