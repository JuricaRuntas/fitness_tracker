import psycopg2
from psycopg2 import sql
import sqlite3
import json
from fitness_tracker.user_profile.profile_db import fetch_email
from fitness_tracker.config import db_info, get_db_paths

db_paths = get_db_paths(["profile.db", "workouts.db"])

def table_is_empty(path=db_paths["workouts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM workouts")
    if cursor.fetchone()[0] == 0: return True
  return False

def create_workouts_table(path=db_paths["workouts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    create_table = """
                   CREATE TABLE IF NOT EXISTS
                   workouts (
                   email text,
                   workouts text,
                   current_workout_plan text,
                   id integer NOT NULL,
                   PRIMARY KEY(id));
                   """
    cursor.execute(create_table)

def fetch_workouts_table_data(path=db_paths["workouts.db"], profile_path=db_paths["profile.db"]):
  email = fetch_email(profile_path)
  select_workouts = "SELECT workouts FROM workouts WHERE email=%s"
  select_current_workout_plan = "SELECT current_workout_plan FROM workouts WHERE email=%s"

  workouts = None
  current_workout_plan = None

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(select_workouts, (email,))
      workouts = cursor.fetchone()[0]

      cursor.execute(select_current_workout_plan , (email,))
      current_workout_plan = cursor.fetchone()[0]
  
  if table_is_empty(path=path):
    insert_values = """
                    INSERT INTO workouts (email, workouts, current_workout_plan) VALUES ('%s', ?, ?)
                    """ % email
    with sqlite3.connect(path) as conn:
      cursor = conn.cursor()
      cursor.execute(insert_values, (workouts, current_workout_plan,))

def fetch_workouts(path=db_paths["workouts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT workouts FROM workouts")
    return cursor.fetchone()[0]

def fetch_current_workout_plan(path=db_paths["workouts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT current_workout_plan FROM workouts")
    return cursor.fetchone()[0]

def insert_default_workouts_data(path=db_paths["workouts.db"], profile_path=db_paths["profile.db"]):
  email = fetch_email(profile_path)
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

    with sqlite3.connect(path) as conn:
      cursor = conn.cursor()
      insert_query = "INSERT INTO workouts {columns} VALUES {values}"
      cursor.execute(insert_query.format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
  except psycopg2.errors.UniqueViolation:
    fetch_workouts_table_data(path=path, profile_path=profile_path)

def update_workouts(workout_name, new_workout, path=db_paths["workouts.db"], profile_path=db_paths["profile.db"]):
  email = fetch_email(profile_path)
  current_workouts = json.loads(fetch_workouts(path))
  current_workouts[workout_name] = new_workout
  new_workout = json.dumps(current_workouts)
  update_query = "UPDATE workouts SET workouts='%s' WHERE email='%s'" % (new_workout, email)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query)
  
  update_query = "UPDATE workouts SET workouts='%s'" % new_workout
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query)

def update_current_workout(workout_name, set_as_current_workout, path=db_paths["workouts.db"], profile_path=db_paths["profile.db"]):
  if set_as_current_workout == True:
    email = fetch_email(profile_path)
    update_query = "UPDATE workouts SET current_workout_plan='%s' WHERE email='%s'" % (workout_name, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update_query)

    update_query = "UPDATE workouts SET current_workout_plan='%s'" % workout_name
    with sqlite3.connect(path) as conn:
      cursor = conn.cursor()
      cursor.execute(update_query)

def delete_workout(workout_name, path=db_paths["workouts.db"], profile_path=db_paths["profile.db"]):
  email = fetch_email(profile_path)
  workouts = json.loads(fetch_workouts(path))
  del workouts[workout_name]
  workouts = json.dumps(workouts)
  update_query = "UPDATE workouts SET workouts='%s' WHERE email='%s'" % (workouts, email) 
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query)
  
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query)
