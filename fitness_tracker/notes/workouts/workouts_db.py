import psycopg2
from psycopg2 import sql
import sqlite3
import json
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_path, db_info

def table_is_empty(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM 'workouts' WHERE email=?", (email,))
    if cursor.fetchone()[0] == 0: return True
  return False

def create_workouts_table(db_path=db_path):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    create_table = """
                   CREATE TABLE IF NOT EXISTS
                   'workouts' (
                   email text,
                   workouts text,
                   current_workout_plan text,
                   id integer NOT NULL,
                   PRIMARY KEY(id));
                   """
    cursor.execute(create_table)

def fetch_workouts_table_data(db_path=db_path):
  email = logged_in_user_email(db_path)
  select_workouts = "SELECT workouts FROM workouts WHERE email=%s"
  select_current_workout_plan = "SELECT current_workout_plan FROM workouts WHERE email=%s"

  workouts = None
  current_workout_plan = None

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(select_workouts, (email,))
      workouts = cursor.fetchone()[0]

      cursor.execute(select_current_workout_plan, (email,))
      current_workout_plan = cursor.fetchone()[0]
  
  if table_is_empty(db_path):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO 'workouts' (email, workouts, current_workout_plan) VALUES (?, ?, ?)", (email, workouts, current_workout_plan,))

def fetch_workouts(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT workouts FROM 'workouts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_current_workout_plan(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT current_workout_plan FROM 'workouts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def insert_default_workouts_data(db_path=db_path):
  email = logged_in_user_email(db_path)
  workouts = {}
  current_workout_plan = ""
  default_dict = {"email": email, "workouts": json.dumps(workouts), "current_workout_plan": current_workout_plan}
  try:
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        insert_query = "INSERT INTO workouts ({columns}) VALUES %s"
        columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_dict.keys()))
        values = tuple(value for value in default_dict.values())
        cursor.execute(sql.SQL(insert_query).format(columns=columns), (values,))

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      insert_query = "INSERT INTO 'workouts' {columns} VALUES {values}"
      cursor.execute(insert_query.format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
  except psycopg2.errors.UniqueViolation:
    fetch_workouts_table_data(db_path)

def update_workouts(workout_name, new_workout, db_path=db_path):
  email = logged_in_user_email(db_path)
  current_workouts = json.loads(fetch_workouts(db_path))
  current_workouts[workout_name] = new_workout
  new_workout = json.dumps(current_workouts)
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (new_workout, email,))
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (new_workout, email,))

def update_current_workout(workout_name, set_as_current_workout, db_path=db_path):
  if set_as_current_workout == True:
    email = logged_in_user_email(db_path)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute("UPDATE workouts SET current_workout_plan=%s WHERE email=%s", (workout_name, email,))

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("UPDATE 'workouts' SET current_workout_plan=? WHERE email=?", (workout_name, email,))

def delete_workout(workout_name, db_path=db_path):
  email = logged_in_user_email(db_path)
  workouts = json.loads(fetch_workouts(db_path))
  del workouts[workout_name]
  workouts = json.dumps(workouts)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (workouts, email,))
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (workouts, email,))
