import sqlite3
import psycopg2
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_path, db_info

def table_is_empty(db_path=db_path):
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM 'nutrition' WHERE email=?", (email,))
    if cursor.fetchone()[0] == 0: return True
  return False

def table_exists(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='nutrition'")
    if cursor.fetchone()[0] == 0: return False
  return True

def fetch_calorie_goal():
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT calorie_goal FROM 'nutrition' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_nutrition_data(db_path=db_path):
  email = logged_in_user_email(db_path) 
  calorie_goal = None
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT calorie_goal FROM nutrition WHERE email=%s", (email,))
      calorie_goal = cursor.fetchone()[0]
  if table_is_empty(db_path):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO 'nutrition' (email, calorie_goal) VALUES (?, ?)", (email, calorie_goal,))

def update_calorie_goal(calorie_goal, db_path=db_path):
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'nutrition' SET calorie_goal=?", (calorie_goal,))
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET calorie_goal=%s WHERE email=%s", (calorie_goal, email,))

def insert_calorie_goal(calorie_goal):
  email = logged_in_user_email(db_path) 
  insert = "INSERT INTO nutrition ({columns}) VALUES %s"
  columns = sql.SQL(", ").join(sql.Identifier(column) for column in ["email", "calorie_goal"])
  values = (email, calorie_goal)
  try:
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql.SQL(insert).format(columns=columns), (values,))
    
    insert = "INSERT INTO 'nutrition' {columns} VALUES {values}"
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(insert.format(columns=("email", "calorie_goal"), values=values))
  except psycopg2.errors.UniqueViolation:
    fetch_nutrition_data(db_path)

def create_nutrition_table(db_path=db_path):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    create_table = """
                   CREATE TABLE IF NOT EXISTS
                   'nutrition' (
                   email text,
                   calorie_goal text,
                   ID integer NOT NULL,
                   PRIMARY KEY(ID));
                   """
    cursor.execute(create_table)
