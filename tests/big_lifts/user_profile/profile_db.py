import os
import sys
import sqlite3

db_path = "test_user_profile.db"

def fetch_table_name(path=db_path):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    get_table_name = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    cursor.execute(get_table_name)
    return cursor.fetchone()[0]

def fetch_units(path=db_path):
  table_name = fetch_table_name(path)
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    fetch_current_units = "SELECT units FROM '{table}'"
    cursor.execute(fetch_current_units.format(table=table_name))
    return cursor.fetchone()[0]

def fetch_email(path=db_path):
  table_name = fetch_table_name(path)
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM '{table}'".format(table=table_name))
    return cursor.fetchone()[0]
