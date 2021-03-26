import json
import sqlite3
import psycopg2
import hashlib
import copy
from fitness_tracker.database_wrapper import DatabaseWrapper

class TestClass:
  def __init__(self, table_name, db_path="test.db"):
    self.test_user = {"email": "test@gmail.com",
                      "password": hashlib.sha256("testpassword123".encode('UTF-8')).hexdigest(),
                      "name": "Test", "age": "18", "gender": "male", "units": "metric",
                      "weight": "100", "height": "190", "goal": "Weight gain",
                      "goalparams": json.dumps(["Moderately active", 0.25]), "goalweight": "120"}
	  
    self.test_password = "testpassword123"
    self.db_path = db_path
    self.table_name = table_name
    
    self.db_wrapper = DatabaseWrapper(self.db_path)
    self.sqlite_connection = self.db_wrapper.sqlite_connection
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_connection = self.db_wrapper.pg_connection
    self.pg_cursor = self.pg_connection.cursor()

  def create_test_user(self):
    self.db_wrapper.create_user(self.test_user["email"], self.test_password)
    self.db_wrapper.create_user_table(self.test_user["email"], self.test_user["password"])
    info = copy.deepcopy(self.test_user)
    del info["email"]
    del info["password"]
    self.db_wrapper.create_user_info_after_signup(info)

  def delete_test_user(self):
    self.pg_cursor.execute("DELETE FROM users WHERE email=%s", (self.test_user["email"],))
    if self.table_name != "users":
      self.pg_cursor.execute("DELETE FROM "+self.table_name+" WHERE email=%s", (self.test_user["email"],))
    self.pg_connection.commit()
  
  # SQLITE METHODS
  def fetch_column_from_local_table(self, column_name):
    self.sqlite_cursor.execute("SELECT "+column_name+" FROM "+self.table_name+" WHERE email=?", (self.test_user["email"],))
    return self.sqlite_cursor.fetchone()[0]

  def fetch_all_local_columns(self):
    self.sqlite_cursor.execute("SELECT * FROM "+self.table_name+" WHERE email=?", (self.test_user["email"],))
    return self.sqlite_cursor.fetchall()

  def fetch_column_names(self):
    self.sqlite_cursor.execute("SELECT * FROM "+self.table_name)
    return tuple(description[0] for description in self.sqlite_cursor.description)[:-1]
  
  def local_table_exists(self):
    self.sqlite_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
    return self.sqlite_cursor.fetchone()[0]

  # POSTGRESQL METHODS
  def fetch_column_from_remote_table(self, column_name):
    self.pg_cursor.execute("SELECT "+column_name+" FROM "+self.table_name+" WHERE email=%s", (self.test_user["email"],))
    return self.pg_cursor.fetchone()[0]

  def fetch_all_remote_columns(self):
    self.pg_cursor.execute("SELECT * FROM "+self.table_name+" WHERE email=%s", (self.test_user["email"],))
    return self.pg_cursor.fetchall()

  def fetch_remote_name_and_password(self):
    self.pg_cursor.execute("SELECT email, password FROM "+self.table_name+" WHERE email=%s", (self.test_user["email"],))
    return self.pg_cursor.fetchone()
