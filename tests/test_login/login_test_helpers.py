import json
import psycopg2
import hashlib
import sqlite3
from psycopg2 import sql
from fitness_tracker.config import db_info
from fitness_tracker.signup.signup_helpers import create_user_table, create_user_info_after_signup, create_user

test_user = {"email": "test@gmail.com",
             "password": hashlib.sha256("testpassword123".encode('UTF-8')).hexdigest(),
             "name": "Test", "age": "18", "gender": "male", "units": "metric",
             "weight": "100", "height": "190", "goal": "Weight gain",
             "goalparams": json.dumps(["Moderately active", 0.25]), "goalweight": "120"}

def create_test_user(path):
  create_user(test_user["email"], "testpassword123")
  create_user_table(test_user["email"], "testpassword123", path)
  create_user_info_after_signup(test_user, test_user["email"], path)

def delete_test_user():
  with psycopg2.connect(host=db_info["host"], port=db_info["port"],
                        database=db_info["database"], user=db_info["user"],
                        password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      delete_query = "DELETE FROM users WHERE email='%s'" % test_user["email"]
      cursor.execute(delete_query)

def test_table_exists():
  with sqlite3.connect("test.db") as conn:
    table_name = "".join([test_user["email"], "_table"])
    cursor = conn.cursor()
    table_exists = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s';" % table_name
    cursor.execute(table_exists)
    return cursor.fetchone()[0]

def fetch_test_table_data():
  table_name = "".join([test_user["email"], "_table"])
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    fetch_query = "SELECT * FROM '%s'" % table_name
    cursor.execute(fetch_query)
    return cursor.fetchall()[0][:-1]

def fetch_test_table_columns():
  table_name = "".join([test_user["email"], "_table"])
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    fetch_query = "SELECT * FROM '%s'" % table_name
    cursor.execute(fetch_query)
    return tuple(description[0] for description in cursor.description if not description[0] == "ID")
