import unittest
import json
import os
import sqlite3
from fitness_tracker.login.login_helpers import check_password, fetch_user_info
from login_test_helpers import *

class TestLogin(unittest.TestCase):
  def setUp(self):
    with sqlite3.connect("test.db") as conn:
      self.sqlite_connection = conn
      self.sqlite_cursor = conn.cursor()
    create_test_user(self.sqlite_connection)

  def tearDown(self):
    delete_test_user()
    os.remove("test.db")
  
  def test_check_password(self):
    status = check_password(test_user["email"], "testpassword123")
    self.assertEqual(status, True)
   
  # case 1: local table doesn't exist
  def test_fetch_user_info_1(self):
    fetch_user_info(test_user["email"], test_user["password"], self.sqlite_cursor)
    
    table_exists_code = 1
    table_exists = test_table_exists(self.sqlite_cursor)
    self.assertEqual(table_exists_code, table_exists)
    
    table_data = fetch_test_table_data(self.sqlite_cursor)
    self.assertEqual(table_data, tuple(test_user.values()))
    
    table_columns = fetch_test_table_columns(self.sqlite_cursor)
    self.assertEqual(table_columns, tuple(test_user.keys()))
  
  # case 2: local table exists
  def test_fetch_user_info_2(self):
    fetch_user_info(test_user["email"], test_user["password"], self.sqlite_cursor)
    
    table_exists_code = 1
    table_exists = test_table_exists(self.sqlite_cursor)
    self.assertEqual(table_exists_code, table_exists)
    
    table_data = fetch_test_table_data(self.sqlite_cursor)
    self.assertEqual(table_data, tuple(test_user.values()))
    
    table_columns = fetch_test_table_columns(self.sqlite_cursor)
    self.assertEqual(table_columns, tuple(test_user.keys()))

if __name__ == "__main__":
 unittest.main() 
