import unittest
import sqlite3
import json
import os
from fitness_tracker.notes.big_lifts.big_lifts_db import (create_big_lifts_table, insert_default_values,
                                                         fetch_user_big_lifts_table_data, update_big_lifts_units,
                                                         update_1RM_lifts, update_lifts_for_reps, lift_difference,
                                                         update_lift_history, convert_lift_history_weight,
                                                         delete_history_entry, update_preferred_lifts,
                                                         update_1RM_and_lifts_for_reps)
from big_lifts_test_helpers import *

class TestBigLifts(unittest.TestCase):
  def setUp(self):  
    create_user_test_table()
    create_big_lifts_table("test.db")
    insert_default_values("test.db")
  
  def tearDown(self):
    delete_test_from_big_lifts(test_user["email"])
    os.remove("test.db")
    os.remove("test_user_profile.db")
  
  def test_create_big_lifts_table(self):
    big_lifts_columns = ("email", "1RM", "lifts_for_reps",
                         "preferred_lifts", "lift_history",
                         "units")
    columns = fetch_big_lifts_columns()
    self.assertEqual(big_lifts_columns, columns)
  
  def test_insert_default_values(self):
    default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
    one_RM = json.dumps({exercise: "0" for exercise in default_exercises})
    lifts_for_reps = json.dumps({exercise: ["0", "0"] for exercise in default_exercises})
    preferred_lifts = json.dumps({"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                                  "Squat": "Back Squat", "Vertical Press": "Overhead Press"})
    default_values = {"1RM": one_RM, "lifts_for_reps": lifts_for_reps,
                      "preferred_lifts": preferred_lifts, "email": test_user["email"],
                      "units": test_user["units"]} 
    
    big_lifts_data = fetch_big_lifts_data(test_user["email"])[0]
    
    fetched_email = big_lifts_data[0]
    fetched_one_RM = big_lifts_data[1]
    fetched_lifts_for_reps = big_lifts_data[2]
    fetched_preferred_lifts = big_lifts_data[3]
    fetched_units = big_lifts_data[5]

    fetched_default_values = {"1RM": fetched_one_RM, "lifts_for_reps": fetched_lifts_for_reps,
                              "preferred_lifts": fetched_preferred_lifts, "email": fetched_email,
                              "units": fetched_units}

    self.assertDictEqual(fetched_default_values, default_values)

  def test_fetch_user_big_lifts_data(self):
    os.remove("test.db")
    create_big_lifts_table("test.db")
    fetch_user_big_lifts_table_data("test.db", "test_user_profile.db")
    big_lifts_data = fetch_big_lifts_data(test_user["email"])[0][:-1]
    local_big_lifts_data = fetch_local_big_lifts_data("test.db")[0][:-1]
    self.assertEqual(local_big_lifts_data, big_lifts_data)
  
  def test_update_units(self):
    table_name = "".join([test_user["email"], "_table"])
    new_units = "imperial"
    update_test_user_table_units(new_units, "test_user_profile.db", table_name)
    update_big_lifts_units("test.db", "test_user_profile.db")
    units = fetch_local_big_lifts_units("test.db")
    self.assertEqual(new_units, units)
  
  def test_update_1RM_lifts(self):
    new_values = {"Bench Press": "100", "Deadlift": "200",
                  "Back Squat": "300", "Overhead Press": "400"}
    update_1RM_lifts(new_values, path=["test_user_profile.db", "test.db"])
    one_rep_maxes = fetch_1RM_lifts("test.db", test_user["email"])
    
    server_1RM = json.loads(one_rep_maxes[0])
    self.assertEqual(new_values, server_1RM)

    local_1RM = json.loads(one_rep_maxes[1])
    self.assertEqual(new_values, local_1RM)
   
  def test_update_lifts_for_reps(self):
    new_values = {"Bench Press": ["10", "100"], "Deadlift": ["3", "250"],
                  "Back Squat": ["5", "200"], "Overhead Press": ["1", "100"]}
    update_lifts_for_reps(new_values, path=["test_user_profile.db", "test.db"])
    lifts_for_reps = fetch_lifts_for_reps("test.db", test_user["email"])
    
    server_lifts_for_reps = json.loads(lifts_for_reps[0])
    self.assertEqual(new_values, server_lifts_for_reps)
    
    local_lifts_for_reps = json.loads(lifts_for_reps[1])
    self.assertEqual(new_values, local_lifts_for_reps)
  
  def test_lift_difference(self):
    one_RM_lifts1 = {"Bench Press": "120", "Deadlift": "150",
                     "Back Squat": "200", "Overhead Press": "300"} 
    one_RM_lifts2 = {"Bench Press": "120", "Deadlift": "300",
                     "Back Squat": "180", "Overhead Press": "300"}

    correct_diff_1RM = {"Deadlift": "300", "Back Squat": "180"}

    update_1RM_lifts(one_RM_lifts1, path=["test_user_profile.db", "test.db"])
    diff_1RM = lift_difference(one_RM_lifts2, one_RM = True, path="test.db")
    self.assertDictEqual(correct_diff_1RM, diff_1RM)

    lifts_for_reps1 = {"Bench Press": ["12", "100"],
                       "Deadlift": ["10", "200"],
                       "Back Squat": ["3", "300"],
                       "Overhead Press": ["9", "120"]}

    lifts_for_reps2 = {"Bench Press": ["9", "100"],
                       "Deadlift": ["15", "200"],
                       "Back Squat": ["3", "310"],
                       "Overhead Press": ["9", "120"]}
    
    correct_diff_lifts_for_reps = {"Bench Press": ["9", "100"],
                                   "Deadlift": ["15", "200"],
                                   "Back Squat": ["3", "310"]}

    update_lifts_for_reps(lifts_for_reps1, path=["test_user_profile.db", "test.db"])
    diff_lifts_for_reps = lift_difference(lifts_for_reps2, lifts_reps=True, path="test.db") 
    self.assertDictEqual(correct_diff_lifts_for_reps, diff_lifts_for_reps)
   
  # case 1: lift history doesn't exist
  def test_update_lift_history(self):
    new_lift_history = {"Bench Press": ["10", "300"],
                        "Deadlift": "100",
                        "Back Squat": "500",
                        "Push Press": ["100", "30"]}
    update_lift_history(new_lift_history, ["test_user_profile.db", "test.db"])
    local_lift_history = json.loads(fetch_local_lift_history("test.db"))
    correct_lift_history = [["Bench Press", ["10", "300"], 3],
                            ["Deadlift", "100", 2],
                            ["Back Squat", "500", 1],
                            ["Push Press", ["100", "30"], 0]]
    self.assertEqual(correct_lift_history, local_lift_history)
  
  # case 2: lift history exists
  def test_update_lift_history_2(self):
    lift_history = {"Bench Press": ["10", "300"],
                    "Deadlift": "100",
                    "Back Squat": "500",
                    "Push Press": ["100", "30"]}
    update_lift_history(lift_history, ["test_user_profile.db", "test.db"])
    new_lift_history = {"Incline Bench Press": "300",
                        "Deadlift": ["3", "180"]}
    update_lift_history(new_lift_history, ["test_user_profile.db", "test.db"])
    local_lift_history = json.loads(fetch_local_lift_history("test.db"))
    correct_lift_history = [["Incline Bench Press", "300", 5],
                            ["Deadlift", ["3", "180"], 4],
                            ["Bench Press", ["10", "300"], 3],
                            ["Deadlift", "100", 2],
                            ["Back Squat", "500", 1],
                            ["Push Press", ["100", "30"], 0]]
    self.assertEqual(correct_lift_history, local_lift_history)
    
  def test_convert_lift_history_weight1(self):
    lift_history = {"Bench Press": ["10", "300"],
                    "Deadlift": "100",
                    "Back Squat": "500",
                    "Push Press": ["100", "30"]}
    update_lift_history(lift_history, ["test_user_profile.db", "test.db"])
    convert_lift_history_weight("lb", ["test_user_profile.db", "test.db"])
    correct_converted_lift_history = [["Bench Press", ["10", "661.38"], 3],
                                      ["Deadlift", "220.46", 2],
                                      ["Back Squat", "1102.3", 1],
                                      ["Push Press", ["100", "66.14"], 0]]
    local_lift_history = json.loads(fetch_local_lift_history("test.db"))
    self.assertEqual(correct_converted_lift_history, local_lift_history)
  
  def test_convert_lift_history_weight2(self):
    lift_history = {"Bench Press": ["10", "225"],
                    "Deadlift": "145",
                    "Back Squat": "300",
                    "Push Press": ["100", "100"]}
    update_lift_history(lift_history, ["test_user_profile.db", "test.db"])
    convert_lift_history_weight("kg", ["test_user_profile.db", "test.db"])
    correct_converted_lift_history = [["Bench Press", ["10", "102.06"], 3],
                                      ["Deadlift", "65.77", 2],
                                      ["Back Squat", "136.08", 1],
                                      ["Push Press", ["100", "45.36"], 0]]
    local_lift_history = json.loads(fetch_local_lift_history("test.db"))
    self.assertEqual(correct_converted_lift_history, local_lift_history)
  
  def test_delete_history_entry(self): 
    lift_history = {"Bench Press": ["10", "225"],
                    "Deadlift": "145",
                    "Back Squat": "300",
                    "Push Press": ["100", "100"]}
    update_lift_history(lift_history, ["test_user_profile.db", "test.db"])
    delete_history_entry(2, path=["test_user_profile.db", "test.db"])
    local_lift_history = json.loads(fetch_local_lift_history("test.db"))
    correct_lift_history = [["Bench Press", ["10", "225"], 3],
                            ["Back Squat", "300", 1],
                            ["Push Press", ["100", "100"], 0]]
    self.assertEqual(correct_lift_history, local_lift_history)

  def test_update_preferred_lifts(self):
    new_preferred_lifts = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Deadlift",
                                      "Squat": "Front Squat", "Vertical Press": "Overhead Press"}

    update_preferred_lifts(new_preferred_lifts, path=["test_user_profile.db", "test.db"])
    local_preferred_lifts = json.loads(fetch_local_preferred_lifts("test.db"))
    self.assertDictEqual(new_preferred_lifts, local_preferred_lifts)
  
  def test_update_1RM_and_lifts_for_reps(self):
    new_preferred_lifts = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Deadlift",
                                      "Squat": "Front Squat", "Vertical Press": "Overhead Press"}
    update_preferred_lifts(new_preferred_lifts, path=["test_user_profile.db", "test.db"])
    update_1RM_and_lifts_for_reps(["test_user_profile.db", "test.db"])
    local_1RM = json.loads(fetch_local_one_rep_maxes("test.db"))
    local_lifts_for_reps = json.loads(fetch_local_lifts_for_reps("test.db"))
    correct_1RM = {"Incline Bench Press": "0",
                   "Deadlift": "0",
                   "Front Squat": "0",
                   "Overhead Press": "0"}
    
    correct_lifts_for_reps = {"Incline Bench Press": ["0", "0"],
                              "Deadlift": ["0", "0"],
                              "Front Squat": ["0", "0"],
                              "Overhead Press": ["0", "0"]}

    self.assertDictEqual(correct_1RM, local_1RM)
    self.assertDictEqual(correct_lifts_for_reps, local_lifts_for_reps)

if __name__ == "__main__":
  unittest.main()
