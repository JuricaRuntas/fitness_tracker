import sqlite3
import json
import hashlib
import psycopg2
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

def delete_test_user(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("DELETE FROM users WHERE email=%s", (email,))

def fetch_big_lifts_columns():
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM big_lifts")
    return tuple(description[0] for description in cursor.description if not description[0] == "id")

def fetch_big_lifts_data(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM big_lifts WHERE email=%s", (email,))
      return cursor.fetchall()

def fetch_local_big_lifts_data(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchall()

def fetch_local_big_lifts_units(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT units FROM big_lifts WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]

def update_test_user_table_units(units, path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET units=? WHERE email=?", (units, test_user["email"],))

def delete_test_from_big_lifts(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("DELETE FROM big_lifts WHERE email=%s", (test_user["email"],))

def fetch_1RM_lifts(db_path, email):
  one_rep_maxes = []
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT one_rep_maxes FROM big_lifts WHERE email=%s", (test_user["email"],))
      one_rep_maxes.append(cursor.fetchone()[0])

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT one_rep_maxes FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    one_rep_maxes.append(cursor.fetchone()[0])
  return one_rep_maxes

def fetch_lifts_for_reps(db_path, email):
  lifts_for_reps = []
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT lifts_for_reps FROM big_lifts WHERE email=%s", (test_user["email"],))
      lifts_for_reps.append(cursor.fetchone()[0])

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lifts_for_reps FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    lifts_for_reps.append(cursor.fetchone()[0])
  return lifts_for_reps

def fetch_local_lift_history(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lift_history FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]

def fetch_local_preferred_lifts(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT preferred_lifts FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]

def fetch_local_one_rep_maxes(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT one_rep_maxes FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]

def fetch_local_lifts_for_reps(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lifts_for_reps FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]

def fetch_local_one_rm_history(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT rm_history FROM 'big_lifts' WHERE email=?", (test_user["email"],))
    return cursor.fetchone()[0]
