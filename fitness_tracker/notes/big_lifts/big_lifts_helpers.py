import os
import sys
import sqlite3
import psycopg2
import json
from psycopg2 import sql
from PyQt5.QtCore import QFileInfo
from common.units_conversion import kg_to_pounds, pounds_to_kg

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

  def fetch_units_from_big_lifts(self):
    units = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      fetch_current_units = "SELECT units FROM big_lifts"
      cursor.execute(fetch_current_units)
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

  def fetch_lift_history(self):
    lift_history = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT lift_history FROM big_lifts")
      lift_history = cursor.fetchone()[0]
    return lift_history

  def fetch_user_big_lifts_table_data(self):
    email = self.fetch_user_email()
    select_1RM = """SELECT "1RM" FROM big_lifts WHERE email=%s"""
    select_lifts_for_reps = "SELECT lifts_for_reps FROM big_lifts WHERE email=%s"
    select_preferred_lifts = "SELECT preferred_lifts FROM big_lifts WHERE email=%s"
    select_lift_history = "SELECT lift_history FROM big_lifts WHERE email=%s"
    select_units = "SELECT units FROM big_lifts WHERE email=%s"

    one_rep_maxes = None
    lifts_for_reps = None
    preferred_lifts = None
    lift_history = None
    units = None

    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(select_1RM, (email,))
        one_rep_maxes = cursor.fetchone()[0]
        
        cursor.execute(select_lifts_for_reps, (email,))
        lifts_for_reps = cursor.fetchone()[0]
        
        cursor.execute(select_preferred_lifts, (email,))
        preferred_lifts = cursor.fetchone()[0]
        
        cursor.execute(select_lift_history, (email,))
        lift_history = cursor.fetchone()[0]

        cursor.execute(select_units, (email,))
        units = cursor.fetchone()[0]

    if self.table_is_empty():
      insert_values = """
                      INSERT INTO big_lifts (email, '1RM', lifts_for_reps, preferred_lifts, lift_history, units) VALUES
                      ('%s', ?, ?, ?, ?, ?)
                      """ % email
      with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_values, (one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units,))

  def insert_default_values(self):
    default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
    email = self.fetch_user_email()
    units = self.fetch_units()
    table_name = self.fetch_user_info_table_name()
    one_RM_dict = json.dumps({exercise:"0" for exercise in default_exercises})
    lifts_for_reps = json.dumps({exercise:["0", "0"] for exercise in default_exercises})
    preferred_lifts = json.dumps({"Horizontal Press": default_exercises[0],
                                                 "Floor Pull": default_exercises[1],
                                                 "Squat": default_exercises[2],
                                                 "Vertical Press": default_exercises[3]})

    default_dict = {"1RM": one_RM_dict, "lifts_for_reps": lifts_for_reps,
                    "preferred_lifts": preferred_lifts, "email": email, "units": units}

    try:
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
    except psycopg2.errors.UniqueViolation: # user already has big_lifts table with data on server
      self.fetch_user_big_lifts_table_data()
  
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
                     units text,
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
    new_values = list(new_values.values())
    email = self.fetch_user_email()
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
    new_lifts_for_reps = list(new_lifts_for_reps.values())
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

  def update_lift_history(self, lift_history):
    email = self.fetch_user_email()
    current_lift_history = self.fetch_lift_history()
    lift_history = [[exercise, value] for exercise, value in lift_history.items()]
    new_lift_history = None
    if current_lift_history == None:
      indices = list(reversed(range(len(lift_history))))
      for i, lift in enumerate(lift_history): lift.append(indices[i])
      new_lift_history = json.dumps(lift_history)
    else:
      last_index = json.loads(current_lift_history)[0][-1]+1
      current_lift_history = list(reversed(json.loads(current_lift_history)))
      for lift in reversed(lift_history):
        lift.append(last_index)
        current_lift_history.append(lift)
        last_index += 1
      new_lift_history = json.dumps(list(reversed(current_lift_history)))

    update = "UPDATE big_lifts SET lift_history='%s' WHERE email='%s'" % (new_lift_history, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update)

  def update_big_lifts_units(self):
    email = self.fetch_user_email()
    units = self.fetch_units()
    update = "UPDATE big_lifts SET units='%s' WHERE email='%s'" % (units, email)
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update)

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
  
  def sort_exercises(self, exercise):
    if exercise in ["Bench Press", "Incline Bench Press"]: return 4
    elif exercise in ["Deadlift", "Sumo Deadlift"]: return 3
    elif exercise in ["Back Squat", "Front Squat"]: return 2
    elif exercise in ["Overhead Press", "Push Press"]: return 1 
  
  # returns sorted dictionary containing updated lifts
  def lift_difference(self, new_lifts, one_RM=False, lifts_reps=False):
    difference = None
    if one_RM:
      db_lifts = set(": ".join([exercise, weight]) for exercise, weight in json.loads(self.fetch_one_rep_maxes()).items())
      new_lifts = set(": ".join([exercise, weight]) for exercise, weight in new_lifts.items() if not weight == '0.0')
      diff = list(new_lifts.difference(db_lifts)) # local lifts that are not in db
      difference = {exercise.split(": ")[0]:exercise.split(": ")[1] for exercise in diff}
    elif lifts_reps:
      db_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in json.loads(self.fetch_lifts_for_reps()).items())
      new_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in new_lifts.items() if not values[1] == '0.0')
      diff = list(new_lifts.difference(db_lifts))
      difference = {exercise.split(":")[0]:exercise.split(":")[1].split("x") for exercise in diff}
    return {key: value for key, value in sorted(difference.items(), key=lambda exercise: self.sort_exercises(exercise[0]))}

  def delete_history_entry(self, entry_index):
    email = self.fetch_user_email()
    lift_history = json.loads(self.fetch_lift_history())
    lift_history = [lift for lift in lift_history if not lift[-1] == entry_index]
    
    update_query1 = "UPDATE big_lifts SET lift_history='%s' WHERE email='%s'" % (json.dumps(lift_history), email)
    update_query2 = "UPDATE big_lifts SET lift_history=NULL WHERE email='%s'" % (email)
    update = update_query1 if not len(lift_history) == 0 else update_query2
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update)

  def convert_lift_history_weight(self, convert_to_units):
    email = self.fetch_user_email()
    try:
      lift_history = json.loads(self.fetch_lift_history())
    except TypeError: # lift history is empty
      return
    if convert_to_units == "kg":
      for lift in lift_history:
        if isinstance(lift[1], list): # second element of history entry is list, it is lifts_for_reps entry
          lift[1][1] = str(pounds_to_kg(float(lift[1][1])))
        else:
          lift[1] = str(pounds_to_kg(float(lift[1])))
    elif convert_to_units == "lb":
      for lift in lift_history:
        if isinstance(lift[1], list):
          lift[1][1] = str(kg_to_pounds(float(lift[1][1])))
        else:
          lift[1] = str(kg_to_pounds(float(lift[1])))
    
    update = "UPDATE big_lifts SET lift_history='%s' WHERE email='%s'" % (json.dumps(lift_history), email)
    
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(update)

    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(update)
