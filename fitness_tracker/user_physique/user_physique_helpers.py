import os
import sys
import psycopg2
from psycopg2 import sql
import sqlite3
from common.units_conversion import kg_to_pounds, pounds_to_kg

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.sep.join([*path.split(os.path.sep)[:-2], "db", "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

class UserPhysique:
  def fetch_table_name(self):
    table_name = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      get_table_name = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
      cursor.execute(get_table_name)
      table_name = cursor.fetchone()[0]
    return table_name

  def fetch_local_user_data(self, table_name):
    user_data = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      get_user_data = "SELECT * FROM '{table}'"
      cursor.execute(get_user_data.format(table=table_name))
      user_data = cursor.fetchone()[2:]
    return user_data

  def fetch_units(self, table_name):
    units = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      fetch_current_units = "SELECT units FROM '{table}'"
      cursor.execute(fetch_current_units.format(table=table_name))
      units = cursor.fetchone()[0]
    return units

  def fetch_user_email(self):
    email = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      table_name = self.fetch_table_name()
      cursor.execute("SELECT email from '{table}'".format(table=table_name))
      try:
        email = cursor.fetchone()[0]
      except TypeError:
        pass
      return email

  def fetch_user_weight(self):
    user_weight = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      table_name = self.fetch_table_name()
      cursor.execute("SELECT weight FROM '{table}'".format(table=table_name))
      user_weight = cursor.fetchone()[0]
    return user_weight
  
  def set_weight(self, user_data):
    # 4th column of user table is currently weight
    weight = user_data[3]
    if "metric" in user_data: return " ".join([str(weight), "kg"])
    elif "imperial" in user_data: return " ".join([str(weight), "lb"])
    
  def convert_weight(self, current_units, weight):
    if current_units == "metric":
      return kg_to_pounds(float(weight))
    elif current_units == "imperial":
      return pounds_to_kg(float(weight))

  def update_weight(self, table_name, weight):
    email = self.fetch_user_email()
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      update = "UPDATE '{table}' SET weight=%s" % str(weight)
      cursor.execute(update.format(table=table_name))
    
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        update = "UPDATE users SET weight=%s WHERE email='%s'" % (weight, email)
        cursor.execute(sql.SQL(update).format(table=sql.Identifier(table_name)))

  def update_units(self, table_name):
    email = self.fetch_user_email()
    current_units = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor() 
      set_units_imperial = "UPDATE '{table}' SET units='imperial'"
      set_units_metric = "UPDATE '{table}' SET units='metric'"
      fetch_current_units = "SELECT units FROM '{table}'"
      cursor.execute(fetch_current_units.format(table=table_name))
      current_units = cursor.fetchone()[0]
      update_units = set_units_imperial if current_units == "metric" else set_units_metric
      cursor.execute(update_units.format(table=table_name))
   
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        set_units_imperial = "UPDATE users SET units='imperial' WHERE email=%s"
        set_units_metric = "UPDATE users SET units='metric' WHERE email=%s"
        update_units = set_units_imperial if current_units == "metric" else set_units_metric
        cursor.execute(update_units, (email,))
