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
      cursor.execute("DELETE FROM users WHERE email=%s", (test_user["email"],))

def fetch_user_info():
  with psycopg2.connect(host=db_info["host"], port=db_info["port"],
                        database=db_info["database"], user=db_info["user"],
                        password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM users WHERE email=%s", (test_user["email"],))
      return cursor.fetchall()

def fetch_name_and_password():
  with psycopg2.connect(host=db_info["host"], port=db_info["port"],
                        database=db_info["database"], user=db_info["user"],
                        password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT email, password FROM users WHERE email=%s", (test_user["email"],))
      return cursor.fetchone()

def fetch_test_table_data():
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'users' WHERE email=?", (test_user["email"],))
    return cursor.fetchall()[0][:-1]

def fetch_test_table_columns():
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'users' WHERE email=?",  (test_user["email"],))
    return tuple(description[0] for description in cursor.description)[:-2]
