import psycopg2
from psycopg2 import sql
import json
from fitness_tracker.user_profile.profile_db import logged_in_user_email

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

def fetch_workouts_table_data(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  select_workouts = "SELECT workouts FROM workouts WHERE email=%s"
  select_current_workout_plan = "SELECT current_workout_plan FROM workouts WHERE email=%s"

  pg_cursor.execute(select_workouts, (email,))
  workouts = pg_cursor.fetchone()[0]

  pg_cursor.execute(select_current_workout_plan, (email,))
  current_workout_plan = pg_cursor.fetchone()[0]
  
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

def insert_default_workouts_data(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  workouts = {}
  current_workout_plan = ""
  default_dict = {"email": email, "workouts": json.dumps(workouts), "current_workout_plan": current_workout_plan}
  try:
    columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_dict.keys()))
    values = tuple(value for value in default_dict.values())
    pg_cursor.execute(sql.SQL("INSERT INTO workouts ({columns}) VALUES %s").format(columns=columns), (values,))
    pg_connection.commit()
    
    sqlite_cursor.execute("INSERT INTO 'workouts' {columns} VALUES {values}".format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
    sqlite_connection.commit()
  except psycopg2.errors.UniqueViolation:
    pg_cursor.execute("ROLLBACK")
    pg_connection.commit()
    fetch_workouts_table_data(sqlite_connection, pg_connection)

def update_workouts(workout_name, new_workout, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  current_workouts = json.loads(fetch_workouts(sqlite_cursor))
  current_workouts[workout_name] = new_workout
  new_workout = json.dumps(current_workouts)
  
  pg_cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (new_workout, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (new_workout, email,))
  sqlite_connection.commit()

def update_current_workout(workout_name, set_as_current_workout, sqlite_connection, pg_connection):
  if set_as_current_workout == True:
    sqlite_cursor = sqlite_connection.cursor()
    pg_cursor = pg_connection.cursor()
    email = logged_in_user_email(sqlite_cursor)
    pg_cursor.execute("UPDATE workouts SET current_workout_plan=%s WHERE email=%s", (workout_name, email,))
    pg_connection.commit()

    sqlite_cursor.execute("UPDATE 'workouts' SET current_workout_plan=? WHERE email=?", (workout_name, email,))
    sqlite_connection.commit()

def delete_workout(workout_name, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  workouts = json.loads(fetch_workouts(sqlite_cursor))
  del workouts[workout_name]
  workouts = json.dumps(workouts)
  
  pg_cursor.execute("UPDATE workouts SET workouts=%s WHERE email=%s", (workouts, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'workouts' SET workouts=? WHERE email=?", (workouts, email,))
  sqlite_connection.commit()
