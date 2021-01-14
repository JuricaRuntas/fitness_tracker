import sqlite3
import psycopg2
from psycopg2 import sql
import os
from fitness_tracker.user_profile.profile_db import fetch_email

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.sep.join([*path.split(os.path.sep)[:-3], "db"])
nutrition_db = os.path.sep.join([db_path, "nutrition.db"])
profile_db = os.path.sep.join([db_path, "profile.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432, 
           "database": "postgres", "user": "admin", "password": "admin"}

def table_is_empty():
  with sqlite3.connect(nutrition_db) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM nutrition")
    if cursor.fetchone()[0] == 0: return True
  return False

def table_exists():
  table_exists = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='nutrition'"
  with sqlite3.connect(nutrition_db) as conn:
    cursor = conn.cursor()
    cursor.execute(table_exists)
    if cursor.fetchone()[0] == 0: return False
  return True

def fetch_calorie_goal():
  with sqlite3.connect(nutrition_db) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT calorie_goal FROM nutrition")
    return cursor.fetchone()[0]

def fetch_nutrition_data():
  email = fetch_email()
  select_calorie_goal = "SELECT calorie_goal FROM nutrition WHERE email=%s"
  calorie_goal = None
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(select_calorie_goal, (email,))
      calorie_goal = cursor.fetchone()[0]
  if table_is_empty():
    insert_values = "INSERT INTO nutrition (email, calorie_goal) VALUES ('%s', ?)" % email
    with sqlite3.connect(nutrition_db) as conn:
      cursor = conn.cursor()
      cursor.execute(insert_values, (calorie_goal,))

def update_calorie_goal(calorie_goal, user_path=profile_db):
  email = fetch_email(user_path)
  with sqlite3.connect(nutrition_db) as conn:
    cursor = conn.cursor()
    update = "UPDATE nutrition SET calorie_goal='%s'" % calorie_goal
    cursor.execute(update)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      update = "UPDATE nutrition SET calorie_goal='%s' WHERE email='%s'" % (calorie_goal, email)
      cursor.execute(update)

def insert_calorie_goal(calorie_goal):
  email = fetch_email()
  insert = "INSERT INTO nutrition ({columns}) VALUES %s"
  columns = sql.SQL(", ").join(sql.Identifier(column) for column in ["email", "calorie_goal"])
  values = (email, calorie_goal)
  try:
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql.SQL(insert).format(columns=columns), (values,))
    
    insert = "INSERT INTO nutrition {columns} VALUES {values}"
    with sqlite3.connect(nutrition_db) as conn:
      cursor = conn.cursor()
      cursor.execute(insert.format(columns=("email", "calorie_goal"), values=values))
  except psycopg2.errors.UniqueViolation:
    fetch_nutrition_data()

def create_nutrition_table(path=nutrition_db):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    create_table = """
                   CREATE TABLE IF NOT EXISTS
                   nutrition (
                   email text,
                   calorie_goal text,
                   ID integer NOT NULL,
                   PRIMARY KEY(ID));
                   """
    cursor.execute(create_table)
