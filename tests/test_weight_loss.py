import unittest
import os
import json
from datetime import datetime
from fitness_tracker.notes.weight_loss.weight_loss_db import (create_weight_loss_table, insert_default_weight_loss_values,
                                                              fetch_user_weight_loss_table_data)
from test_class import TestClass

class TestWeightLoss(unittest.TestCase):
  def setUp(self):  
    self.test_class = TestClass("weight_loss", "test.db")
    self.sqlite_connection = self.test_class.sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = self.test_class.pg_connection
    self.pg_cursor = self.pg_connection.cursor() 
    
    self.test_class.create_test_user()
    create_weight_loss_table(self.sqlite_connection)
    insert_default_weight_loss_values(self.sqlite_connection, self.pg_connection)
  
  def tearDown(self):
    self.test_class.delete_test_user()
    os.remove("test.db")
  
  def test_create_weight_loss_table(self):
    big_lifts_columns = ("email", "weight_history", "preferred_activity",
                         "cardio_history")
    columns = self.test_class.fetch_column_names()
    self.assertEqual(big_lifts_columns, columns)

  def test_insert_default_weight_loss_values(self):
    current_date = datetime.today().strftime("%d/%m/%Y")
    default_weight_history, default_cardio_history = {}, {}
    default_preferred_activity = "Running"
    default_activities = ["Running", "Walking", "Cycling", "Swimming"]
    default_preferred_activity = "Running"
  
    default_cardio_history[current_date] = {}
    for activity in default_activities:
      default_cardio_history[current_date][activity] = [] 
    
    default_dict = {"email": self.test_class.test_user["email"], "weight_history": json.dumps(default_weight_history),
                    "preferred_activity": default_preferred_activity,
                    "cardio_history": json.dumps(default_cardio_history)}
     
    fetched_data = self.test_class.fetch_all_local_columns()[0]
    
    fetched_email = fetched_data[0]
    fetched_weight_history = fetched_data[1]
    fetched_preferred_activity = fetched_data[2]
    fetched_cardio_history = fetched_data[3]

    fetched_dict = {"email": fetched_email, "weight_history": fetched_weight_history,
                    "preferred_activity": fetched_preferred_activity,
                    "cardio_history": fetched_cardio_history} 
    
    self.assertDictEqual(default_dict, fetched_dict)

  def test_fetch_user_weight_loss_table_data(self):
    fetch_user_weight_loss_table_data(self.sqlite_connection, self.pg_connection)
    weight_loss_data = self.test_class.fetch_all_remote_columns()[0][:-1]
    local_weight_loss_data = self.test_class.fetch_all_local_columns()[0][:-1]
    self.assertEqual(local_weight_loss_data, weight_loss_data)

if __name__ == "__main__":
  unittest.main()
