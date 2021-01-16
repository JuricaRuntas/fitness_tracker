import json
import hashlib
import sqlite3
import psycopg2
from fitness_tracker.signup.signup_helpers import create_user_table, create_user_info_after_signup, create_user
from fitness_tracker.config import db_info

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
      delete = "DELETE FROM users WHERE email='%s'" % email
      cursor.execute(delete)

def delete_test_from_workouts_table(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      delete = "DELETE FROM workouts WHERE email='%s'" % email
      cursor.execute(delete)

def fetch_workouts_table_columns():
  with sqlite3.connect("test.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    return tuple(description[0] for description in cursor.description if not description[0] == "id") 

def fetch_workouts_data(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      fetch_query = "SELECT * FROM workouts WHERE email='%s'" % email
      cursor.execute(fetch_query)
      return cursor.fetchall()

def fetch_local_workouts_data(path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    fetch_query = "SELECT * FROM workouts"
    cursor.execute(fetch_query)
    return cursor.fetchall()

def fetch_test_workouts(path, email):
  workouts = []
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      query = """SELECT workouts FROM workouts WHERE email='%s'""" % email
      cursor.execute(query)
      workouts.append(cursor.fetchone()[0])

  with sqlite3.connect(path) as conn:
    query = "SELECT workouts FROM workouts"
    cursor = conn.cursor()
    cursor.execute(query)
    workouts.append(cursor.fetchone()[0])
  return workouts
 
def fetch_test_current_workout(path, email):
  workouts = []
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      query = """SELECT current_workout_plan FROM workouts WHERE email='%s'""" % email
      cursor.execute(query)
      workouts.append(cursor.fetchone()[0])

  with sqlite3.connect(path) as conn:
    query = "SELECT current_workout_plan FROM workouts"
    cursor = conn.cursor()
    cursor.execute(query)
    workouts.append(cursor.fetchone()[0])
  return workouts
