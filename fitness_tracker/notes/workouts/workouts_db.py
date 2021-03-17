import psycopg2
from psycopg2 import sql
import sqlite3
import json
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_path, db_info

def table_is_empty(cursor):
  email = logged_in_user_email(cursor)
  cursor.execute("SELECT COUNT (*) FROM 'workouts' WHERE email=?", (email,))
  if cursor.fetchone()[0] == 0: return True
  return False

def create_workouts_table(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  create_table = """
                 CREATE TABLE IF NOT EXISTS
                 'workouts' (
                 email text,
                 workouts text,
                 current_workout_plan text,
                 id integer NOT NULL,
                 PRIMARY KEY(id));
                 """
  sqlite_cursor.execute(create_table)
  sqlite_connection.commit()

def fetch_workouts_table_data(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
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
  
  if table_is_empty(sqlite_cursor):
    sqlite_cursor.execute("INSERT INTO 'workouts' (email, workouts, current_workout_plan) VALUES (?, ?, ?)", (email, workouts, current_workout_plan,))
    sqlite_connection.commit()

def fetch_workouts(cursor):
  email = logged_in_user_email(cursor)
  cursor.execute("SELECT workouts FROM 'workouts' WHERE email=?", (email,))
  return cursor.fetchone()[0]

def fetch_current_workout_plan(cursor):
  email = logged_in_user_email(cursor)
  cursor.execute("SELECT current_workout_plan FROM 'workouts' WHERE email=?", (email,))
  return cursor.fetchone()[0]

def insert_default_workouts_data(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
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

    insert_query = "INSERT INTO 'workouts' {columns} VALUES {values}"
    sqlite_cursor.execute(insert_query.format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
    sqlite_connection.commit()
  except psycopg2.errors.UniqueViolation:
    fetch_workouts_table_data(sqlite_connection)

def update_workouts(workout_name, new_workout, sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  current_workouts = json.loads(fetch_workouts(sqlite_cursor))
  current_workouts[workout_name] = new_workout
  new_workout = json.dumps(current_workouts)
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (new_workout, email,))
  
  sqlite_cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (new_workout, email,))
  sqlite_connection.commit()

def update_current_workout(workout_name, set_as_current_workout, sqlite_connection):
  if set_as_current_workout == True:
    sqlite_cursor = sqlite_connection.cursor()
    email = logged_in_user_email(sqlite_cursor)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute("UPDATE workouts SET current_workout_plan=%s WHERE email=%s", (workout_name, email,))

    sqlite_cursor.execute("UPDATE 'workouts' SET current_workout_plan=? WHERE email=?", (workout_name, email,))
    sqlite_connection.commit()

def delete_workout(workout_name, sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  workouts = json.loads(fetch_workouts(sqlite_cursor))
  del workouts[workout_name]
  workouts = json.dumps(workouts)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (workouts, email,))
  
  sqlite_cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (workouts, email,))
  sqlite_connection.commit()
