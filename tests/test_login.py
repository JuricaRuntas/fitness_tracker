import unittest
import json
import os
from fitness_tracker.login.login_helpers import check_password, fetch_user_info
from test_class import TestClass

class TestLogin(unittest.TestCase):
  def setUp(self):
    self.test_class = TestClass("users", "test.db")
    self.sqlite_connection = self.test_class.sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = self.test_class.pg_connection
    self.pg_cursor = self.pg_connection.cursor() 
    self.test_class.create_test_user()
    
  def tearDown(self):
    self.test_class.delete_test_user()
    os.remove("test.db")
  
  def test_check_password(self):
    status = check_password(self.test_class.test_user["email"], "testpassword123")
    self.assertEqual(status, True)
   
  # case 1: local table doesn't exist
  def test_fetch_user_info_1(self):
    fetch_user_info(self.test_class.test_user["email"], self.test_class.test_user["password"], self.sqlite_connection, self.pg_connection.cursor())
    
    table_exists_code = 1
    table_exists = self.test_class.local_table_exists()
    self.assertEqual(table_exists_code, table_exists)
    
    table_data = self.test_class.fetch_all_local_columns()[0][:-2]
    self.assertEqual(table_data, tuple(self.test_class.test_user.values()))
    
    table_columns = self.test_class.fetch_column_names()
    columns = ('email', 'password', 'name', 'age', 'gender', 'units',
               'weight', 'height', 'goal', 'goalparams', 'goalweight', 'logged_in')
    self.assertEqual(table_columns, columns)
  
  # case 2: local table exists
  def test_fetch_user_info_2(self):
    fetch_user_info(self.test_class.test_user["email"], self.test_class.test_user["password"], self.sqlite_connection, self.pg_connection.cursor())
    
    table_exists_code = 1
    table_exists = self.test_class.local_table_exists()
    self.assertEqual(table_exists_code, table_exists)
    
    table_data = self.test_class.fetch_all_local_columns()[0][:-2]
    self.assertEqual(table_data, tuple(self.test_class.test_user.values()))
    
    table_columns = self.test_class.fetch_column_names()
    columns = ('email', 'password', 'name', 'age', 'gender', 'units',
               'weight', 'height', 'goal', 'goalparams', 'goalweight', 'logged_in')
    self.assertEqual(table_columns, columns)

if __name__ == "__main__":
 unittest.main() 
