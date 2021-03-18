import sqlite3
import json
import hashlib
import psycopg2
from psycopg2 import sql
from fitness_tracker.config import db_info
from fitness_tracker.signup.signup_helpers import create_user_table, create_user_info_after_signup, create_user

test_user = {"email": "test@gmail.com",
             "password": hashlib.sha256("testpassword123".encode('UTF-8')).hexdigest(),
             "name": "Test", "age": "18", "gender": "male", "units": "metric",
             "weight": "100", "height": "190", "goal": "Weight gain",
             "goalparams": json.dumps(["Moderately active", 0.25]), "goalweight": "120"}

def create_test_user(sqlite_connection, pg_connection):
  create_user(test_user["email"], "testpassword123", pg_connection)
  create_user_table(test_user["email"], "testpassword123", sqlite_connection)
  create_user_info_after_signup(test_user, test_user["email"], sqlite_connection, pg_connection)

def delete_test_user(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("DELETE FROM users WHERE email=%s", (email,))

def delete_test_from_nutrition(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("DELETE FROM nutrition WHERE email=%s", (email,))

def fetch_nutrition_columns(cursor):
  cursor.execute("SELECT * FROM 'nutrition'")
  return tuple(description[0] for description in cursor.description if not description[0] == 'ID')

def insert_nutrition_data(email, calorie_goal):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      insert = "INSERT INTO nutrition ({columns}) VALUES %s"
      columns = sql.SQL(", ").join(sql.Identifier(column) for column in ("email", "calorie_goal"))
      values = (email, calorie_goal)
      cursor.execute(sql.SQL(insert).format(columns=columns), (values,))

def fetch_default_meal_plans_values(sqlite_cursor):
  values = None
  sqlite_cursor.execute("SELECT * FROM 'nutrition' WHERE email=?", (test_user["email"],))
  values = sqlite_cursor.fetchall()[0][2:-1]
  return values

def fetch_server_nutrition_data():
   with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],

                         user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM nutrition WHERE email=%s", (test_user["email"],))
      return cursor.fetchall()

def fetch_local_nutrition_data(sqlite_cursor):
  sqlite_cursor.execute("SELECT * FROM 'nutrition' WHERE email=?", (test_user["email"],))
  return sqlite_cursor.fetchall() 

def fetch_local_meal_plans(sqlite_cursor):
  sqlite_cursor.execute("SELECT meal_plans FROM 'nutrition' WHERE email=?", (test_user["email"],))
  return sqlite_cursor.fetchone()[0]
