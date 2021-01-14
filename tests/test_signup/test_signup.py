import unittest
import sqlite3
import os
from fitness_tracker.signup.signup_helpers import create_user, create_user_info_after_signup, create_user_table
from signup_test_helpers import *

class TestSignup(unittest.TestCase):
  def test_create_user(self):
    create_user(test_user["email"], "testpassword123")
    name_and_password = fetch_name_and_password()
    self.assertEqual(tuple([test_user["email"], test_user["password"]]), name_and_password)

  def test_create_user_table(self):
    create_user_table(test_user["email"], "testpassword123", "test.db")
    table_columns = fetch_test_table_columns()
    table_data = fetch_test_table_data()[0:2]

    self.assertEqual(table_columns, tuple(test_user.keys()))
    self.assertEqual(table_data, tuple([test_user["email"], test_user["password"]]))
    
  def test_create_user_info_after_signup(self):
    create_user_table(test_user["email"], "testpassword123", "test1.db")
    user_info = {key: value for key, value in test_user.items() if not key  == "email" and not key == "password"}
    create_user_info_after_signup(test_user, test_user["email"], test=[True, "".join([test_user["email"], "_table"])], path="test1.db")
    fetch_info = fetch_user_info()[0][:-1]
    self.assertEqual(fetch_info, tuple(test_user.values()))

if __name__ == "__main__":
  unittest.main(exit=False)
  delete_test_user()
  os.remove("test.db")
  os.remove("test1.db")
