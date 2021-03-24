import unittest
import json
import os
from datetime import datetime
from fitness_tracker.notes.compound_exercises.compound_exercises_db import (create_big_lifts_table, insert_default_values,
                                                                            fetch_user_big_lifts_table_data, update_big_lifts_units,
                                                                            update_1RM_lifts, update_lifts_for_reps, lift_difference,
                                                                            update_lift_history, convert_lift_history_weight,
                                                                            delete_history_entry, update_preferred_lifts,
                                                                            update_1RM_and_lifts_for_reps,
                                                                            update_one_rep_maxes_history)
from fitness_tracker.user_profile.profile_db import update_units
from test_class import TestClass

class TestBigLifts(unittest.TestCase):
  def setUp(self):
    self.test_class = TestClass("big_lifts", "test.db")
    self.sqlite_connection = self.test_class.sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = self.test_class.pg_connection
    self.pg_cursor = self.pg_connection.cursor()
    
    self.test_class.create_test_user()
    create_big_lifts_table(self.sqlite_connection)
    insert_default_values(self.sqlite_connection, self.pg_connection)
  
  def tearDown(self):
    self.test_class.delete_test_user()
    os.remove("test.db")
  
  def test_create_big_lifts_table(self):
    big_lifts_columns = ("email", "one_rep_maxes", "lifts_for_reps",
                         "preferred_lifts", "lift_history",
                         "units", "rm_history")
    columns = self.test_class.fetch_column_names()
    self.assertEqual(big_lifts_columns, columns)
  
  def test_insert_default_values(self):
    default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
    one_RM = json.dumps({exercise: "0" for exercise in default_exercises})
    lifts_for_reps = json.dumps({exercise: ["0", "0"] for exercise in default_exercises})
    preferred_lifts = {"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                       "Squat": "Back Squat", "Vertical Press": "Overhead Press"}
    secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                           "Squat": "Front Squat", "Vertical Press": "Push Press"}
  
    months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
    current_year = str(datetime.now().year)
    rm_history = {current_year:{}}
    for month in months:
      exercises_dict = {}
      for lift_type in preferred_lifts:
        exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
      for lift_type in secondary_exercises:
        exercises_dict[lift_type][secondary_exercises[lift_type]] = []
      
      rm_history[current_year][month] = exercises_dict

    default_values = {"one_rep_maxes": one_RM, "lifts_for_reps": lifts_for_reps,
                      "preferred_lifts": json.dumps(preferred_lifts), "rm_history": json.dumps(rm_history),
                      "email": self.test_class.test_user["email"], "units": self.test_class.test_user["units"]} 
    
    big_lifts_data = self.test_class.fetch_all_remote_columns()[0]
    
    # big_lifts_data[4] == lift_history
    fetched_email = big_lifts_data[0]
    fetched_one_RM = big_lifts_data[1]
    fetched_lifts_for_reps = big_lifts_data[2]
    fetched_preferred_lifts = big_lifts_data[3]
    fetched_units = big_lifts_data[5]
    fetched_rm_history = big_lifts_data[6]

    fetched_default_values = {"one_rep_maxes": fetched_one_RM, "lifts_for_reps": fetched_lifts_for_reps,
                              "preferred_lifts": fetched_preferred_lifts, "rm_history": fetched_rm_history,
                              "email": fetched_email, "units": fetched_units}

    self.assertDictEqual(fetched_default_values, default_values)
  
  def test_fetch_user_big_lifts_data(self):
    fetch_user_big_lifts_table_data(self.sqlite_connection, self.pg_connection)
    big_lifts_data = self.test_class.fetch_all_remote_columns()[0][:-1]
    local_big_lifts_data = self.test_class.fetch_all_local_columns()[0][:-1]
    self.assertEqual(local_big_lifts_data, big_lifts_data)
  
  def test_update_units(self):
    new_units = "imperial"
    update_units(self.sqlite_connection, self.pg_connection)
    update_big_lifts_units(self.sqlite_connection, self.pg_connection)
    units = self.test_class.fetch_column_from_local_table("units")
    self.assertEqual(new_units, units)
  
  def test_update_1RM_lifts(self):
    new_values = {"Bench Press": "100", "Deadlift": "200",
                  "Back Squat": "300", "Overhead Press": "400"}
    update_1RM_lifts(new_values, self.sqlite_connection, self.pg_connection)
    
    server_1RM = json.loads(self.test_class.fetch_column_from_remote_table("one_rep_maxes"))
    self.assertEqual(new_values, server_1RM)

    local_1RM = json.loads(self.test_class.fetch_column_from_local_table("one_rep_maxes"))
    self.assertEqual(new_values, local_1RM)
  
  def test_update_lifts_for_reps(self):
    new_values = {"Bench Press": ["10", "100"], "Deadlift": ["3", "250"],
                  "Back Squat": ["5", "200"], "Overhead Press": ["1", "100"]}
    update_lifts_for_reps(new_values, self.sqlite_connection, self.pg_connection)
    
    server_lifts_for_reps = json.loads(self.test_class.fetch_column_from_remote_table("lifts_for_reps"))
    self.assertEqual(new_values, server_lifts_for_reps)
    
    local_lifts_for_reps = json.loads(self.test_class.fetch_column_from_local_table("lifts_for_reps"))
    self.assertEqual(new_values, local_lifts_for_reps)
  
  def test_lift_difference(self):
    one_RM_lifts1 = {"Bench Press": "120", "Deadlift": "150",
                     "Back Squat": "200", "Overhead Press": "300"} 
    one_RM_lifts2 = {"Bench Press": "120", "Deadlift": "300",
                     "Back Squat": "180", "Overhead Press": "300"}

    correct_diff_1RM = {"Deadlift": "300", "Back Squat": "180"}

    update_1RM_lifts(one_RM_lifts1, self.sqlite_connection, self.pg_connection)
    diff_1RM = lift_difference(one_RM_lifts2, self.sqlite_cursor, one_RM = True)
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

    update_lifts_for_reps(lifts_for_reps1, self.sqlite_connection, self.pg_connection)
    diff_lifts_for_reps = lift_difference(lifts_for_reps2, self.sqlite_cursor, lifts_reps=True) 
    self.assertDictEqual(correct_diff_lifts_for_reps, diff_lifts_for_reps)
  
  # case 1: lift history doesn't exist
  def test_update_lift_history(self):
    new_lift_history = {"Bench Press": ["10", "300"],
                        "Deadlift": "100",
                        "Back Squat": "500",
                        "Push Press": ["100", "30"]}
    update_lift_history(new_lift_history, self.sqlite_connection, self.pg_connection)
    local_lift_history = json.loads(self.test_class.fetch_column_from_local_table("lift_history"))
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
    update_lift_history(lift_history, self.sqlite_connection, self.pg_connection)
    new_lift_history = {"Incline Bench Press": "300",
                        "Deadlift": ["3", "180"]}
    update_lift_history(new_lift_history, self.sqlite_connection, self.pg_connection)
    local_lift_history = json.loads(self.test_class.fetch_column_from_local_table("lift_history"))
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
    update_lift_history(lift_history, self.sqlite_connection, self.pg_connection)
    convert_lift_history_weight("lb", self.sqlite_connection, self.pg_connection)
    correct_converted_lift_history = [["Bench Press", ["10", "661.38"], 3],
                                      ["Deadlift", "220.46", 2],
                                      ["Back Squat", "1102.3", 1],
                                      ["Push Press", ["100", "66.14"], 0]]
    local_lift_history = json.loads(self.test_class.fetch_column_from_local_table("lift_history"))
    self.assertEqual(correct_converted_lift_history, local_lift_history)
  
  def test_convert_lift_history_weight2(self):
    lift_history = {"Bench Press": ["10", "225"],
                    "Deadlift": "145",
                    "Back Squat": "300",
                    "Push Press": ["100", "100"]}
    update_lift_history(lift_history, self.sqlite_connection, self.pg_connection)
    convert_lift_history_weight("kg", self.sqlite_connection, self.pg_connection)
    correct_converted_lift_history = [["Bench Press", ["10", "102.06"], 3],
                                      ["Deadlift", "65.77", 2],
                                      ["Back Squat", "136.08", 1],
                                      ["Push Press", ["100", "45.36"], 0]]
    local_lift_history = json.loads(self.test_class.fetch_column_from_local_table("lift_history"))
    self.assertEqual(correct_converted_lift_history, local_lift_history)
  
  def test_delete_history_entry(self): 
    lift_history = {"Bench Press": ["10", "225"],
                    "Deadlift": "145",
                    "Back Squat": "300",
                    "Push Press": ["100", "100"]}
    update_lift_history(lift_history, self.sqlite_connection, self.pg_connection)
    delete_history_entry(2, self.sqlite_connection, self.pg_connection)
    local_lift_history = json.loads(self.test_class.fetch_column_from_local_table("lift_history"))
    correct_lift_history = [["Bench Press", ["10", "225"], 3],
                            ["Back Squat", "300", 1],
                            ["Push Press", ["100", "100"], 0]]
    self.assertEqual(correct_lift_history, local_lift_history)
  
  def test_update_preferred_lifts(self):
    new_preferred_lifts = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Deadlift",
                                      "Squat": "Front Squat", "Vertical Press": "Overhead Press"}

    update_preferred_lifts(new_preferred_lifts, self.sqlite_connection, self.pg_connection)
    local_preferred_lifts = json.loads(self.test_class.fetch_column_from_local_table("preferred_lifts"))
    self.assertDictEqual(new_preferred_lifts, local_preferred_lifts)
  
  def test_update_1RM_and_lifts_for_reps(self):
    new_preferred_lifts = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Deadlift",
                                      "Squat": "Front Squat", "Vertical Press": "Overhead Press"}
    update_preferred_lifts(new_preferred_lifts, self.sqlite_connection, self.pg_connection)
    update_1RM_and_lifts_for_reps(self.sqlite_connection, self.pg_connection)
    local_1RM = json.loads(self.test_class.fetch_column_from_local_table("one_rep_maxes"))
    local_lifts_for_reps = json.loads(self.test_class.fetch_column_from_local_table("lifts_for_reps"))
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
  
  def test_update_one_rep_maxes_history(self):
    current_year = "2021"
    RM_dict = {current_year:{}}
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"] 
    preferred_lifts = {"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                       "Squat": "Back Squat", "Vertical Press": "Overhead Press"}
    secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                           "Squat": "Front Squat", "Vertical Press": "Push Press"}

    for month in months:
      exercises_dict = {}
      for lift_type in preferred_lifts:
        exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
      for lift_type in secondary_exercises:
        exercises_dict[lift_type][secondary_exercises[lift_type]] = []

      RM_dict[current_year][month] = exercises_dict

    new_RM_lifts = {"Bench Press": "500.0", "Deadlift": "300.0",
                    "Back Squat": "150.0", "Overhead Press": "100.0"}
    
    for i, (lift, weight) in enumerate(new_RM_lifts.items()):
      current_lift_type = RM_dict[current_year]["March"][list(preferred_lifts.keys())[i]]
      current_lift_type[lift].append(weight)
    
    # test 1: history doesn't exist
    update_one_rep_maxes_history(new_RM_lifts, current_year, self.sqlite_connection, self.pg_connection)
    fetched_RM_history = json.loads(self.test_class.fetch_column_from_local_table("rm_history"))
    self.assertDictEqual(RM_dict, fetched_RM_history)

    # test 2: history exists, add exercise that doesn't exist yet
    new_RM_lifts = {"Incline Bench Press": "123.0", "Front Squat": "120.0"}
    
    for i, (lift, weight) in enumerate(new_RM_lifts.items()):
      current_lift_type = RM_dict[current_year]["March"][list(preferred_lifts.keys())[i]]
      if lift not in current_lift_type: current_lift_type[lift] = []
      current_lift_type[lift].append(weight)

    update_one_rep_maxes_history(new_RM_lifts, current_year, self.sqlite_connection, self.pg_connection)
    fetched_RM_history = json.loads(self.test_class.fetch_column_from_local_table("rm_history"))
    self.assertDictEqual(RM_dict, fetched_RM_history)

    # test 3: add another year
    previous_year_dict = {}
    new_RM_lifts_2020 = {"Bench Press": "200.5", "Incline Bench Press": "50.0", "Back Squat": "500.0"}
    for month in months:
      exercises_dict = {}
      for lift_type in preferred_lifts:
        exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
      for lift_type in secondary_exercises:
        exercises_dict[lift_type][secondary_exercises[lift_type]] = []
      previous_year_dict[month] = exercises_dict
    RM_dict["2020"] = previous_year_dict
    
    for i, (lift, weight) in enumerate(new_RM_lifts_2020.items()):
      current_lift_type = RM_dict["2020"]["March"][list(preferred_lifts.keys())[i]]
      if lift not in current_lift_type: current_lift_type[lift] = []
      current_lift_type[lift].append(weight)
    
    update_one_rep_maxes_history(new_RM_lifts_2020, "2020", self.sqlite_connection, self.pg_connection)
    fetched_RM_history_2020 = json.loads(self.test_class.fetch_column_from_local_table("rm_history"))
    self.assertDictEqual(RM_dict, fetched_RM_history_2020)

if __name__ == "__main__":
  unittest.main()
