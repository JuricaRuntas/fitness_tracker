import unittest
import copy
import os
from test_class import TestClass
from fitness_tracker.database_wrapper import DatabaseWrapper

class TestSignup(unittest.TestCase):
  def setUp(self):
    self.test_class = TestClass("users", "test.db")
    self.db_wrapper = DatabaseWrapper("test.db")
    self.test_class.create_test_user()
    
  def tearDown(self):
    self.test_class.delete_test_user()

  def test_create_user(self):
    name_and_password = self.test_class.fetch_remote_name_and_password()
    self.assertEqual(tuple([self.test_class.test_user["email"], self.test_class.test_user["password"]]), name_and_password)
  
  def test_create_user_table(self):
    self.db_wrapper.create_user_table(self.test_class.test_user["email"], self.test_class.test_user["password"])
    columns = ('email', 'password', 'name', 'age', 'gender', 'units',
               'weight', 'height', 'goal', 'goalparams', 'goalweight', 'logged_in') 
    table_columns = self.test_class.fetch_column_names()
    table_data = self.test_class.fetch_all_local_columns()[0][:-1][0:2]

    self.assertEqual(table_columns, columns)
    self.assertEqual(table_data, tuple([self.test_class.test_user["email"], self.test_class.test_user["password"]]))
  
  def test_create_user_info_after_signup(self):
    self.db_wrapper.create_user_table(self.test_class.test_user["email"], self.test_class.test_user["password"])
    user_info = {key: value for key, value in self.test_class.test_user.items() if not key  == "email" and not key == "password"}
    info = copy.deepcopy(self.test_class.test_user)
    del info["email"]
    del info["password"]
    self.db_wrapper.create_user_info_after_signup(info)
    fetch_info = self.test_class.fetch_all_remote_columns()[0][:-1]
    self.assertEqual(fetch_info, tuple(self.test_class.test_user.values()))

if __name__ == "__main__":
  unittest.main()
