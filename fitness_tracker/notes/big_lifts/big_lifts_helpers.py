import os
import sqlite3
import psycopg2
import json
from psycopg2 import sql
from PyQt5.QtCore import QFileInfo

path = os.path.normpath(QFileInfo(__file__).absolutePath())
db_path = path.split(os.path.sep)[:-3]
db_path_user_info = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "big_lifts.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

class BigLifts:
  def table_is_empty(self):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT COUNT (*) FROM big_lifts")
      if cursor.fetchone()[0] == 0: return True
    return False

  def fetch_user_info_table_name(self):
    table_name = None
    with sqlite3.connect(db_path_user_info) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
      try:
        table_name = cursor.fetchone()[0]
      except TypeError:
        pass
    return table_name

  def fetch_user_email(self):
    email = None
    with sqlite3.connect(db_path_user_info) as conn:
      cursor = conn.cursor()
      table_name = self.fetch_user_info_table_name()
      if table_name == None: return None
      cursor.execute("SELECT email FROM '{table}'".format(table=table_name))
      try:
        email = cursor.fetchone()[0]
      except TypeError:
        pass
    return email

  def fetch_units(self):
    table_name = self.fetch_user_info_table_name()
    units = None
    with sqlite3.connect(db_path_user_info) as conn:
      cursor = conn.cursor()
      fetch_current_units = "SELECT units from '{table}'"
      cursor.execute(fetch_current_units.format(table=table_name))
      units = cursor.fetchone()[0]
    return units

  def fetch_one_rep_maxes(self):
    one_rep_maxes = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("""SELECT "1RM" FROM big_lifts""")
      one_rep_maxes = cursor.fetchone()[0]
    return one_rep_maxes

  def fetch_lifts_for_reps(self):
    lifts_for_reps = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT lifts_for_reps FROM big_lifts")
      lifts_for_reps = cursor.fetchone()[0]
    return lifts_for_reps
 
  def fetch_preferred_lifts(self):
    email = self.fetch_user_email()
    preferred_lifts = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT preferred_lifts FROM big_lifts WHERE email='%s'" % email)
      preferred_lifts = cursor.fetchone()[0]
    return preferred_lifts

  def insert_default_values(self):
    default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
    email = self.fetch_user_email()
    table_name = self.fetch_user_info_table_name()
    one_RM_dict = json.dumps({exercise:"0" for exercise in default_exercises})
    lifts_for_reps = json.dumps({exercise:["0", "0"] for exercise in default_exercises})
    preferred_lifts = json.dumps({"Horizontal Press": default_exercises[0],
                                                 "Floor Pull": default_exercises[1],
                                                 "Squat": default_exercises[2],
                                                 "Vertical Press": default_exercises[3]})

    default_dict = {"1RM": one_RM_dict, "lifts_for_reps": lifts_for_reps,
                    "preferred_lifts": preferred_lifts, "email": email}

    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        insert_query = "INSERT INTO big_lifts ({columns}) VALUES %s"
        columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_dict.keys()))
        values = tuple(value for value in default_dict.values())
        cursor.execute(sql.SQL(insert_query).format(columns=columns), (values,))
    
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      insert_query = "INSERT INTO big_lifts {columns} VALUES {values}"
      cursor.execute(insert_query.format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))

  def create_big_lifts_table(self):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      create_table = """
                     CREATE TABLE IF NOT EXISTS
                     big_lifts (
                     email text,
                     '1RM' text,
                     lifts_for_reps text,
                     preferred_lifts text,
                     lift_history text,
                     id integer NOT NULL,
                     PRIMARY KEY(id));
                     """
      cursor.execute(create_table)

  def update_preferred_lifts(self, new_preferred_lifts):
    new_preferred_lifts = json.dumps(new_preferred_lifts)
    email = self.fetch_user_email()
    update_query = "UPDATE big_lifts SET preferred_lifts='%s' WHERE email='%s'" % (new_preferred_lifts, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update_query)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update_query)
  
  # updates exercises
  def update_1RM_and_lifts_for_reps(self):
    email = self.fetch_user_email()
    preferred_lifts = list(json.loads(self.fetch_preferred_lifts()).values())
    one_rep_maxes = json.loads(self.fetch_one_rep_maxes())
    lifts_for_reps = json.loads(self.fetch_lifts_for_reps())

    new_one_rep_maxes = json.dumps({preferred_lifts[i]:value for i, value in enumerate(one_rep_maxes.values())})
    new_lifts_for_reps = json.dumps({preferred_lifts[i]:value for i, value in enumerate(lifts_for_reps.values())})
    update_query1 = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'""" % (new_one_rep_maxes, email)
    update_query2 = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (new_lifts_for_reps, email)
        
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update_query1)
        cursor.execute(update_query2)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update_query1)
      cursor.execute(update_query2)
  
  # updates weight
  def update_1RM_lifts(self, new_values):
    email = self.fetch_user_email()
    units = self.fetch_units()
    one_rep_max_lifts = json.loads(self.fetch_one_rep_maxes())
    for i, lift in enumerate(one_rep_max_lifts.keys()):
      one_rep_max_lifts[lift] = new_values[i]

    one_rep_max_lifts = json.dumps(one_rep_max_lifts)
   
    update_query = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'""" % (one_rep_max_lifts, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update_query)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update_query)
  
  # updates reps and weight
  def update_lifts_for_reps(self, new_lifts_for_reps):
    email = self.fetch_user_email()
    big_lifts = json.loads(self.fetch_lifts_for_reps())
    for i, lift in enumerate(big_lifts.keys()):
      big_lifts[lift] = new_lifts_for_reps[i]

    big_lifts = json.dumps(big_lifts)

    update_query = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (big_lifts, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update_query)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update_query)

  def clear_one_rep_maxes(self):
    email = self.fetch_user_email()
    one_rep_maxes = json.loads(self.fetch_one_rep_maxes())
    for exercise, value in one_rep_maxes.items():
      one_rep_maxes[exercise] = "0"

    one_rep_maxes = json.dumps(one_rep_maxes)
    
    clear = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'"""% (one_rep_maxes, email)

    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(clear)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(clear)

  def clear_lifts_for_reps(self):
    email = self.fetch_user_email()
    lifts_for_reps = json.loads(self.fetch_lifts_for_reps())
    for exercise, values in lifts_for_reps.items():
      lifts_for_reps[exercise] = ["0", "0"]

    lifts_for_reps = json.dumps(lifts_for_reps)

    clear = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (lifts_for_reps, email)

    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(clear)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(clear)
