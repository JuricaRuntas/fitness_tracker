import os
import importlib

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": os.environ["FT_ADMIN_PASSWORD"]}

db_path = os.path.join(os.path.dirname(importlib.util.find_spec("fitness_tracker").origin), "fitness_tracker.db")
