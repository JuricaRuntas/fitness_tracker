import os
import sys
import psycopg2
from psycopg2 import sql
import sqlite3
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg
from fitness_tracker.config import db_info, db_path

def logged_in_user_email(db_path=db_path):
  try:
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT email FROM 'users' WHERE logged_in='YES'")
      return cursor.fetchone()[0]
  except TypeError: # all users have "logged_in='NO'"
    pass

def fetch_local_user_data():
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[2:]

def fetch_username(db_path=db_path):
  try:
    email = logged_in_user_email()
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT name FROM 'users' WHERE email=?", (email,))
      return cursor.fetchone()[0]
  except (sqlite3.OperationalError, TypeError): # titlebar will raise this error if users table doesn't exist
    pass

def fetch_units(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT units FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_user_weight(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT weight FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_age(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_gender(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT gender FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_height(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT height FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_goal_weight(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT goalweight FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_goal_params(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT goalparams FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_goal(db_path=db_path):
  email = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT goal FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def set_weight(user_data):
  # 4th column of user table is currently weight
  weight = user_data[4]
  if "metric" in user_data: return " ".join([str(weight), "kg"])
  elif "imperial" in user_data: return " ".join([str(weight), "lb"])
  
def convert_weight(current_units, weight):
  if current_units == "metric":
    return kg_to_pounds(float(weight))
  elif current_units == "imperial":
    return pounds_to_kg(float(weight))

def update_weight(weight, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET weight=%s WHERE email=%s", (str(weight), email,))
      
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET weight=? WHERE email=?", (str(weight), email,))

def update_height(height, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET height=%s WHERE email=%s", (str(height), email,))
      
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET height=? WHERE email=?", (str(height), email,))

def update_gender(gender, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET gender=%s WHERE email=%s", (str(gender), email,))
      
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET gender=? WHERE email=?", (str(gender), email,))

def update_age(age, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET age=%s WHERE email=%s", (str(age), email,))
      
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET age=? WHERE email=?", (str(age), email,))

def update_username(name, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET name=%s WHERE email=%s", (str(name), email,))
      

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET name=? WHERE email=?", (str(name), email,))
  
def update_goal(goal, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET goal=%s WHERE email=%s", (goal, email,))

  with sqlite3.connect(db_path) as conn: 
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET goal=? WHERE email=?", (goal, email,))

def update_goal_parameters(goal_params, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET goalparams=%s WHERE email=%s", (goal_params, email,))

  with sqlite3.connect(db_path) as conn: 
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET goalparams=? WHERE email=?", (goal_params, email,))

def update_goal_weight(goal_weight, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE users SET goalweight=%s WHERE email=%s", (goal_weight, email,))

  with sqlite3.connect(db_path) as conn: 
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET goalweight=? WHERE email=?", (goal_weight, email,))

def update_calorie_goal(calorie_goal, db_path=db_path):
  email = logged_in_user_email()
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET calorie_goal=%s WHERE email=%s", (calorie_goal, email,))

  with sqlite3.connect(db_path) as conn: 
    cursor = conn.cursor()
    cursor.execute("UPDATE nutrition SET calorie_goal=? WHERE email=?", (calorie_goal, email,))

def update_units():
  email = logged_in_user_email()
  current_units = None
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor() 
    set_units_imperial = "UPDATE 'users' SET units='imperial' WHERE email=?"
    set_units_metric = "UPDATE 'users' SET units='metric' WHERE email=?"
    cursor.execute("SELECT units FROM 'users' WHERE email=?", (email,))
    current_units = cursor.fetchone()[0]
    update_units = set_units_imperial if current_units == "metric" else set_units_metric
    cursor.execute(update_units, (email,))
 
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      set_units_imperial = "UPDATE users SET units='imperial' WHERE email=%s"
      set_units_metric = "UPDATE users SET units='metric' WHERE email=%s"
      update_units = set_units_imperial if current_units == "metric" else set_units_metric
      cursor.execute(update_units, (email,))
