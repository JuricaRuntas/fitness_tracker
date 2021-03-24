import unittest
import json
import os
from fitness_tracker.notes.workouts.workouts_db import (create_workouts_table, fetch_workouts_table_data,
                                                        insert_default_workouts_data, update_workouts,
                                                        update_current_workout, delete_workout)
from test_class import TestClass

class TestWorkouts(unittest.TestCase):
  def setUp(self):
    self.test_class = TestClass("workouts", "test.db")
    self.sqlite_connection = self.test_class.sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = self.test_class.pg_connection
    self.pg_cursor = self.pg_connection.cursor() 

    self.test_class.create_test_user()
    create_workouts_table(self.sqlite_connection)
    insert_default_workouts_data(self.sqlite_connection, self.pg_connection)

  def tearDown(self):
    self.test_class.delete_test_user()
    os.remove("test.db")

  def test_create_workouts_table(self):
    create_workouts_table(self.sqlite_connection)
    workouts_columns = ("email", "workouts", "current_workout_plan")
    fetched_columns = self.test_class.fetch_column_names()
    self.assertEqual(workouts_columns, fetched_columns)
  
  def test_insert_default_workouts_data(self):
    insert_default_workouts_data(self.sqlite_connection, self.pg_connection)
    default_data = {"email": self.test_class.test_user["email"],
                    "workouts": "{}",
                    "current_workout_plan": ""}
    fetched_data = self.test_class.fetch_all_remote_columns()[0]

    fetched_email = fetched_data[0]
    fetched_workouts = fetched_data[1]
    fetched_current_workout_plan = fetched_data[2]

    fetched_default_data = {"email": fetched_email,
                            "workouts": fetched_workouts,
                            "current_workout_plan": fetched_current_workout_plan}

    self.assertDictEqual(fetched_default_data, default_data)
  
  def test_fetch_workouts_table_data(self):
    fetch_workouts_table_data(self.sqlite_connection, self.pg_connection)
    server_workouts_data = self.test_class.fetch_all_remote_columns()[0][:-1]
    local_workouts_data = self.test_class.fetch_all_local_columns()[0][:-1]
    self.assertEqual(server_workouts_data, local_workouts_data)
  
  def test_update_workouts(self):
    new_workout = {"Tuesday": {"Exercise 1": {"Sets": "2", "Reps": "10", "Rest": "2 min", "Duration (optional)": "30 min"},
                               "Exercise 2": {"Sets": "6", "Reps": "2", "Rest": "45 min", "Duration (optional)": ""}},
                   "Friday": {"Exercise 1": {"Sets": "1", "Reps": "1", "Rest": "5 min", "Duration (optional)": "10 min"}}}
    workout = {"My Workout1": new_workout}
    update_workouts("My Workout1", new_workout, self.sqlite_connection, self.pg_connection)
    
    server_workouts = json.loads(self.test_class.fetch_column_from_remote_table("workouts"))
    local_workouts = json.loads(self.test_class.fetch_column_from_local_table("workouts"))

    self.assertDictEqual(workout, server_workouts)
    self.assertDictEqual(workout, local_workouts)
  
  def test_update_current_workout(self):
    new_current_workout = "My Workout1"
    update_current_workout("My Workout1", True, self.sqlite_connection, self.pg_connection)

    server_current_workout = self.test_class.fetch_column_from_remote_table("current_workout_plan")
    local_current_workout = self.test_class.fetch_column_from_local_table("current_workout_plan")

    self.assertEqual(new_current_workout, server_current_workout)
    self.assertEqual(new_current_workout, local_current_workout)

  def test_delete_workout(self):
    new_workout = {"Tuesday": {"Exercise 1": {"Sets": "2", "Reps": "10", "Rest": "2 min", "Duration (optional)": "30 min"},
                               "Exercise 2": {"Sets": "6", "Reps": "2", "Rest": "45 min", "Duration (optional)": ""}},
                   "Friday": {"Exercise 1": {"Sets": "1", "Reps": "1", "Rest": "5 min", "Duration (optional)": "10 min"}}}
    workout = {"My Workout1": new_workout}
    update_workouts("My Workout1", new_workout, self.sqlite_connection, self.pg_connection)
    delete_workout("My Workout1", self.sqlite_connection, self.pg_connection)

    server_workouts = json.loads(self.test_class.fetch_column_from_remote_table("workouts"))
    local_workouts = json.loads(self.test_class.fetch_column_from_local_table("workouts"))

    self.assertDictEqual({}, server_workouts)
    self.assertDictEqual({}, local_workouts)

if __name__ == "__main__":
  unittest.main()
