import sqlite3
import psycopg2
from psycopg2 import sql
import os
from user_physique.user_physique_helpers import UserPhysique

path = os.path.abspath(os.path.dirname(__file__))
nutrition_db = os.path.sep.join([*path.split(os.path.sep)[:-3], "db", "nutrition.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432, 
           "database": "postgres", "user": "admin", "password": "admin"}

class Nutrition:
  def table_is_empty(self):
    with sqlite3.connect(nutrition_db) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT COUNT (*) FROM nutrition")
      if cursor.fetchone()[0] == 0: return True
    return False

  def table_exists(self):
    table_exists = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='nutrition'"
    with sqlite3.connect(nutrition_db) as conn:
      cursor = conn.cursor()
      cursor.execute(table_exists)
      if cursor.fetchone()[0] == 0: return False
    return True

  def fetch_calorie_goal(self):
    calorie_goal = None
    with sqlite3.connect(nutrition_db) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT calorie_goal FROM nutrition")
      calorie_goal = cursor.fetchone()[0]
    return calorie_goal

  def fetch_nutrition_data(self):
    email = UserPhysique().fetch_user_email()
    select_calorie_goal = "SELECT calorie_goal FROM nutrition WHERE email=%s"
    calorie_goal = None
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(select_calorie_goal, (email,))
        calorie_goal = cursor.fetchone()[0]
    if self.table_is_empty():
      insert_values = "INSERT INTO nutrition (email, calorie_goal) VALUES ('%s', ?)" % email
      with sqlite3.connect(nutrition_db) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_values, (calorie_goal,))

  def insert_calorie_goal(self, calorie_goal):
    email = UserPhysique().fetch_user_email()
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
      self.fetch_nutrition_data()

  def create_nutrition_table(self):
    with sqlite3.connect(nutrition_db) as conn:
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
