import os
import sys

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": os.environ["FT_ADMIN_PASSWORD"]}

def get_db_paths(db_name):
  db_paths = {}
  namespace = sys._getframe(1).f_globals
  path_to_file = namespace["__file__"]
  path_to_file = list(reversed(path_to_file.split(os.path.sep)))
  top_level_index = path_to_file.index("fitness_tracker")
  db_path = os.path.sep.join([*list(reversed(path_to_file[top_level_index+1:])), "db"])
  if isinstance(db_name, str):
    db_paths[db_name] = os.path.sep.join([db_path, db_name])
  elif isinstance(db_name, list):
    for db in db_name:
      db_paths[db] = os.path.sep.join([db_path, db])
  return db_paths
