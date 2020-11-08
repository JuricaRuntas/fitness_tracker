import os
import sys
import psycopg2
from psycopg2 import sql
import sqlite3
from PyQt5.QtCore import QFileInfo

path = os.path.normpath(QFileInfo(__file__).absolutePath())
db_path = path.split(os.path.sep)[:-2]
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

def fetch_table_name():
  table_name = None
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    get_table_name = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    cursor.execute(get_table_name)
    table_name = cursor.fetchone()[0]
  return table_name

def fetch_local_user_data(table_name):
  user_data = None
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    get_user_data = "SELECT * FROM '{table}'"
    cursor.execute(get_user_data.format(table=table_name))
    user_data = cursor.fetchone()[1:]
  return user_data

def fetch_units(table_name):
  units = None
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    fetch_current_units = "SELECT units FROM '{table}'"
    cursor.execute(fetch_current_units.format(table=table_name))
    units = cursor.fetchone()[0]
  return units

def set_weight(user_data):
  # 4th column of user table is currently weight
  weight = user_data[3]
  if "metric" in user_data: return " ".join([str(weight), "kg"])
  elif "imperial" in user_data: return " ".join([str(weight), "lb"])
  
def convert_weight(current_units, weight):
  add_common_to_path()
  from common.units_conversion import kg_to_pounds, pounds_to_kg
  if current_units == "metric":
    return kg_to_pounds(weight)
  elif current_units == "imperial":
    return pounds_to_kg(weight)

def update_weight(table_name, weight):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    update = "UPDATE '{table}' SET weight=%s" % weight
    cursor.execute(update.format(table=table_name))
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      update = "UPDATE {table} SET weight=%s" % weight
      cursor.execute(sql.SQL(update).format(table=sql.Identifier(table_name)))

def update_units(table_name):
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
      set_units_imperial = "UPDATE {table} SET units='imperial'"
      set_units_metric = "UPDATE {table} SET units='metric'"
      update_units = set_units_imperial if current_units == "metric" else set_units_metric
      cursor.execute(sql.SQL(update_units).format(table=sql.Identifier(table_name)))

def add_common_to_path():
  path = os.path.normpath(QFileInfo(__file__).absolutePath())
  path = path.split(os.path.sep)[:-1]
  path = os.path.sep.join(path)
  sys.path.append(path)
