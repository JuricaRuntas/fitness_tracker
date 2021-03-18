import unittest
import sqlite3
import psycopg2
import os
from fitness_tracker.signup.signup_helpers import create_user, create_user_info_after_signup, create_user_table
from fitness_tracker.config import db_info
from signup_test_helpers import *

class TestSignup(unittest.TestCase):
  def setUp(self):
    with sqlite3.connect("test.db") as conn:
      self.sqlite_connection = conn
      self.sqlite_cursor = conn.cursor()
    with psycopg2.connect(**db_info) as pg_conn:
      with pg_conn.cursor() as pg_cursor:
        self.pg_connection = pg_conn
        self.pg_cursor = pg_cursor

    create_test_user(self.sqlite_connection, self.pg_connection)

  def tearDown(self):
    delete_test_user()
    os.remove("test.db")

  def test_create_user(self):
    name_and_password = fetch_name_and_password()
    self.assertEqual(tuple([test_user["email"], test_user["password"]]), name_and_password)

  def test_create_user_table(self):
    create_user_table(test_user["email"], "testpassword123", self.sqlite_connection)
    table_columns = fetch_test_table_columns(self.sqlite_cursor)
    table_data = fetch_test_table_data(self.sqlite_cursor)[0:2]

    self.assertEqual(table_columns, tuple(test_user.keys()))
    self.assertEqual(table_data, tuple([test_user["email"], test_user["password"]]))
    
  def test_create_user_info_after_signup(self):
    create_user_table(test_user["email"], "testpassword123", self.sqlite_connection)
    user_info = {key: value for key, value in test_user.items() if not key  == "email" and not key == "password"}
    create_user_info_after_signup(test_user, test_user["email"], self.sqlite_connection, self.pg_connection)
    fetch_info = fetch_user_info()[0][:-1]
    self.assertEqual(fetch_info, tuple(test_user.values()))

if __name__ == "__main__":
  unittest.main()
