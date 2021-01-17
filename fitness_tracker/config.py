import os
import importlib

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": os.environ["FT_ADMIN_PASSWORD"]}

db_list = ["profile.db", "workouts.db", "nutrition.db", "big_lifts.db"]

def get_db_paths(db_name):
  db_paths = {}
  path = os.path.dirname(importlib.util.find_spec("fitness_tracker").origin)
  db_path = os.path.join(path, "db")
  if isinstance(db_name, str):
    db_paths[db_name] = os.path.sep.join([db_path, db_name])
  elif isinstance(db_name, list):
    for db in db_name:
      db_paths[db] = os.path.sep.join([db_path, db])
  return db_paths
