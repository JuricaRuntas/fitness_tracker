import unittest
import os
from fitness_tracker.signup.signup_helpers import create_user, create_user_info_after_signup, create_user_table
from test_class import TestClass

class TestSignup(unittest.TestCase):
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

  def test_create_user(self):
    name_and_password = self.test_class.fetch_remote_name_and_password()
    self.assertEqual(tuple([self.test_class.test_user["email"], self.test_class.test_user["password"]]), name_and_password)

  def test_create_user_table(self):
    create_user_table(self.test_class.test_user["email"], "testpassword123", self.sqlite_connection)
    columns = ('email', 'password', 'name', 'age', 'gender', 'units',
               'weight', 'height', 'goal', 'goalparams', 'goalweight', 'logged_in') 
    table_columns = self.test_class.fetch_column_names()
    table_data = self.test_class.fetch_all_local_columns()[0][:-1][0:2]

    self.assertEqual(table_columns, columns)
    self.assertEqual(table_data, tuple([self.test_class.test_user["email"], self.test_class.test_user["password"]]))
    
  def test_create_user_info_after_signup(self):
    create_user_table(self.test_class.test_user["email"], "testpassword123", self.sqlite_connection)
    user_info = {key: value for key, value in self.test_class.test_user.items() if not key  == "email" and not key == "password"}
    create_user_info_after_signup(self.test_class.test_user, self.test_class.test_user["email"], self.sqlite_connection, self.pg_connection)
    fetch_info = self.test_class.fetch_all_remote_columns()[0][:-1]
    self.assertEqual(fetch_info, tuple(self.test_class.test_user.values()))

if __name__ == "__main__":
  unittest.main()
