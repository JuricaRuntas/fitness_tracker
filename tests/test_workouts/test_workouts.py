import unittest
import json
import os
from fitness_tracker.notes.workouts.workouts_db import (create_workouts_table, fetch_workouts_table_data,
                                                        insert_default_workouts_data, update_workouts,
                                                        update_current_workout, delete_workout)
from workouts_test_helpers import *

class TestWorkouts(unittest.TestCase):
  def setUp(self):
    create_test_user("test.db")
    create_workouts_table("test.db")
    insert_default_workouts_data("test.db")

  def tearDown(self):
    delete_test_user(test_user["email"])
    delete_test_from_workouts_table(test_user["email"])
    os.remove("test.db")

  def test_create_workouts_table(self):
    workouts_columns = ("email", "workouts", "current_workout_plan")
    fetched_columns = fetch_workouts_table_columns()
    self.assertEqual(workouts_columns, fetched_columns)
  
  def test_insert_default_workouts_data(self):
    default_data = {"email": test_user["email"],
                    "workouts": "{}",
                    "current_workout_plan": ""}
    fetched_data = fetch_workouts_data(test_user["email"])[0]

    fetched_email = fetched_data[0]
    fetched_workouts = fetched_data[1]
    fetched_current_workout_plan = fetched_data[2]

    fetched_default_data = {"email": fetched_email,
                            "workouts": fetched_workouts,
                            "current_workout_plan": fetched_current_workout_plan}

    self.assertDictEqual(fetched_default_data, default_data)
  
  def test_fetch_workouts_table_data(self):
    fetch_workouts_table_data("test.db")
    server_workouts_data = fetch_workouts_data(test_user["email"])[0][:-1]
    local_workouts_data = fetch_local_workouts_data("test.db")[0][:-1]
    self.assertEqual(server_workouts_data, local_workouts_data)
  
  def test_update_workouts(self):
    new_workout = {"Tuesday": {"Exercise 1": {"Sets": "2", "Reps": "10", "Rest": "2 min", "Duration (optional)": "30 min"},
                               "Exercise 2": {"Sets": "6", "Reps": "2", "Rest": "45 min", "Duration (optional)": ""}},
                   "Friday": {"Exercise 1": {"Sets": "1", "Reps": "1", "Rest": "5 min", "Duration (optional)": "10 min"}}}
    workout = {"My Workout1": new_workout}
    update_workouts("My Workout1", new_workout, "test.db")
    
    workouts = fetch_test_workouts(path="test.db", email=test_user["email"])
    server_workouts = json.loads(workouts[0])
    local_workouts = json.loads(workouts[1])

    self.assertDictEqual(workout, server_workouts)
    self.assertDictEqual(workout, local_workouts)
  
  def test_update_current_workout(self):
    new_current_workout = "My Workout1"
    update_current_workout("My Workout1", True, "test.db")
    test_current_workout = fetch_test_current_workout("test.db", test_user["email"])

    server_current_workout = test_current_workout[0]
    local_current_workout = test_current_workout[1]

    self.assertEqual(new_current_workout, server_current_workout)
    self.assertEqual(new_current_workout, local_current_workout)

  def test_delete_workout(self):
    new_workout = {"Tuesday": {"Exercise 1": {"Sets": "2", "Reps": "10", "Rest": "2 min", "Duration (optional)": "30 min"},
                               "Exercise 2": {"Sets": "6", "Reps": "2", "Rest": "45 min", "Duration (optional)": ""}},
                   "Friday": {"Exercise 1": {"Sets": "1", "Reps": "1", "Rest": "5 min", "Duration (optional)": "10 min"}}}
    workout = {"My Workout1": new_workout}
    update_workouts("My Workout1", new_workout, "test.db")
    delete_workout("My Workout1", "test.db")
    fetched_workouts = fetch_test_workouts(path="test.db", email=test_user["email"])

    server_workouts = json.loads(fetched_workouts[0])
    local_workouts = json.loads(fetched_workouts[1])

    self.assertDictEqual({}, server_workouts)
    self.assertDictEqual({}, local_workouts)

if __name__ == "__main__":
  unittest.main()
