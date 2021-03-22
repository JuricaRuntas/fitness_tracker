import unittest
import sqlite3
import psycopg2
import os
from fitness_tracker.notes.weight_loss.weight_loss_db import (create_weight_loss_table, insert_default_weight_loss_values,
                                                              fetch_user_weight_loss_table_data)
from fitness_tracker.config import db_info
from weight_loss_test_helpers import *

class TestWeightLoss(unittest.TestCase):
  def setUp(self):  
    with sqlite3.connect("test.db") as conn:
      self.sqlite_connection = conn
      self.sqlite_cursor = conn.cursor()
    with psycopg2.connect(**db_info) as pg_conn:
      self.pg_connection = pg_conn
      self.pg_cursor = self.pg_connection.cursor()

    create_test_user(self.sqlite_connection, self.pg_connection)
    create_weight_loss_table(self.sqlite_connection)
    insert_default_weight_loss_values(self.sqlite_connection, self.pg_connection)
  
  def tearDown(self):
    delete_test_user(test_user["email"])
    os.remove("test.db")
  
  def test_create_weight_loss_table(self):
    big_lifts_columns = ("email", "weight_history", "preferred_activity",
                         "cardio_history")
    columns = fetch_weight_loss_columns(self.sqlite_cursor)
    self.assertEqual(big_lifts_columns, columns)

  def test_insert_default_weight_loss_values(self):
    default_weight_history, default_cardio_history = [], []
    default_preferred_activity = "Running"
  
    default_dict = {"email": test_user["email"], "weight_history": json.dumps(default_weight_history),
                    "preferred_activity": default_preferred_activity,
                    "cardio_history": json.dumps(default_cardio_history)}
     
    fetched_data = fetch_weight_loss_data(self.pg_cursor)[0]
    
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
    weight_loss_data = fetch_weight_loss_data(self.pg_cursor)[0][:-1]
    local_weight_loss_data = fetch_local_weight_loss_data(self.sqlite_cursor)[0][:-1]
    self.assertEqual(local_weight_loss_data, weight_loss_data)

if __name__ == "__main__":
  unittest.main()
