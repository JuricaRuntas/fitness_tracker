import os
import importlib
import sqlite3
import psycopg2

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": os.environ["FT_ADMIN_PASSWORD"]}

db_path = os.path.join(os.path.dirname(importlib.util.find_spec("fitness_tracker").origin), "fitness_tracker.db")

class DBConnection:
  def __init__(self, db_type):
    assert db_type in ("sqlite", "pg")
    if db_type == "sqlite":
      self.connection = sqlite3.connect(db_path)
    elif db_type == "pg":
      self.connection = psycopg2.connect(**db_info)
  
  def connect(self):
    return self.connection
