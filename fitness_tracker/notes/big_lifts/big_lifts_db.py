import sys
import sqlite3
import psycopg2
import json
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import fetch_units, fetch_email
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg
from fitness_tracker.config import db_info, get_db_paths

db_paths = get_db_paths(["profile.db", "big_lifts.db"])

def table_is_empty(path=db_paths["big_lifts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM big_lifts")
    if cursor.fetchone()[0] == 0: return True
  return False

def fetch_units_from_big_lifts():
  with sqlite3.connect(db_paths["big_lifts.db"]) as conn:
    cursor = conn.cursor()
    fetch_current_units = "SELECT units FROM big_lifts"
    cursor.execute(fetch_current_units)
    return cursor.fetchone()[0]

def fetch_one_rep_maxes(path=db_paths["big_lifts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("""SELECT "1RM" FROM big_lifts""")
    return cursor.fetchone()[0]

def fetch_lifts_for_reps(path=db_paths["big_lifts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lifts_for_reps FROM big_lifts")
    return cursor.fetchone()[0]

def fetch_preferred_lifts(path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT preferred_lifts FROM big_lifts WHERE email='%s'" % email)
    return cursor.fetchone()[0]

def fetch_lift_history(path=db_paths["big_lifts.db"]):
  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lift_history FROM big_lifts")
    return cursor.fetchone()[0]

def fetch_user_big_lifts_table_data(path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
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
  
  if table_is_empty(path=path):
    insert_values = """
                    INSERT INTO big_lifts (email, '1RM', lifts_for_reps, preferred_lifts, lift_history, units) VALUES
                    ('%s', ?, ?, ?, ?, ?)
                    """ % email
    with sqlite3.connect(path) as conn:
      cursor = conn.cursor()
      cursor.execute(insert_values, (one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units,))

def insert_default_values(path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
  email = fetch_email(user_path)
  units = fetch_units(user_path)
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
  
      with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        insert_query = "INSERT INTO big_lifts {columns} VALUES {values}"
        cursor.execute(insert_query.format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
  except psycopg2.errors.UniqueViolation: # user already has big_lifts table with data on server
    fetch_user_big_lifts_table_data(path=path, user_path=user_path)

def create_big_lifts_table(path=db_paths["big_lifts.db"]):
  with sqlite3.connect(path) as conn:
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

def update_preferred_lifts(new_preferred_lifts, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  new_preferred_lifts = json.dumps(new_preferred_lifts)
  email = fetch_email(user_path)
  update_query = "UPDATE big_lifts SET preferred_lifts='%s' WHERE email='%s'" % (new_preferred_lifts, email)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query)

# updates exercises
def update_1RM_and_lifts_for_reps(path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  preferred_lifts = list(json.loads(fetch_preferred_lifts(path, user_path)).values())
  one_rep_maxes = json.loads(fetch_one_rep_maxes(path))
  lifts_for_reps = json.loads(fetch_lifts_for_reps(path))

  new_one_rep_maxes = json.dumps({preferred_lifts[i]:value for i, value in enumerate(one_rep_maxes.values())})
  new_lifts_for_reps = json.dumps({preferred_lifts[i]:value for i, value in enumerate(lifts_for_reps.values())})
  update_query1 = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'""" % (new_one_rep_maxes, email)
  update_query2 = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (new_lifts_for_reps, email)
      
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query1)
      cursor.execute(update_query2)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query1)
    cursor.execute(update_query2)

# updates weight
def update_1RM_lifts(new_values, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  new_values = list(new_values.values())
  email = fetch_email(user_path)
  one_rep_max_lifts = json.loads(fetch_one_rep_maxes(path))
  for i, lift in enumerate(one_rep_max_lifts.keys()):
    one_rep_max_lifts[lift] = new_values[i]

  one_rep_max_lifts = json.dumps(one_rep_max_lifts)
 
  update_query = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'""" % (one_rep_max_lifts, email)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query)

# updates reps and weight
def update_lifts_for_reps(new_lifts_for_reps, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  lifts_for_reps = json.loads(fetch_lifts_for_reps(path))
  new_lifts_for_reps = list(new_lifts_for_reps.values())
  
  for i, lift in enumerate(lifts_for_reps.keys()):
    lifts_for_reps[lift] = new_lifts_for_reps[i]

  lifts_for_reps = json.dumps(lifts_for_reps)

  update_query = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (lifts_for_reps, email)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update_query)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update_query)

def update_lift_history(lift_history, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(path)
  current_lift_history = fetch_lift_history(path)
  lift_history = [[exercise, value] for exercise, value in lift_history.items()]
  new_lift_history = None
  if current_lift_history == None:
    indices = list(reversed(range(len(lift_history))))
    for i, lift in enumerate(lift_history):
      lift.append(indices[i])
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

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update)

def update_big_lifts_units(path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  units = fetch_units(user_path)
  update = "UPDATE big_lifts SET units='%s' WHERE email='%s'" % (units, email)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update)

def clear_one_rep_maxes():
  email = fetch_email()
  one_rep_maxes = json.loads(fetch_one_rep_maxes())
  for exercise, value in one_rep_maxes.items():
    one_rep_maxes[exercise] = "0"

  one_rep_maxes = json.dumps(one_rep_maxes)
  
  clear = """UPDATE big_lifts SET "1RM"='%s' WHERE email='%s'"""% (one_rep_maxes, email)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(clear)

  with sqlite3.connect(db_paths["big_lifts.db"]) as conn:
    cursor = conn.cursor()
    cursor.execute(clear)

def clear_lifts_for_reps():
  email = fetch_email()
  lifts_for_reps = json.loads(fetch_lifts_for_reps())
  for exercise, values in lifts_for_reps.items():
    lifts_for_reps[exercise] = ["0", "0"]

  lifts_for_reps = json.dumps(lifts_for_reps)

  clear = "UPDATE big_lifts SET lifts_for_reps='%s' WHERE email='%s'" % (lifts_for_reps, email)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(clear)

  with sqlite3.connect(db_paths["big_lifts.db"]) as conn:
    cursor = conn.cursor()
    cursor.execute(clear)

def sort_exercises(exercise):
  if exercise in ["Bench Press", "Incline Bench Press"]: return 4
  elif exercise in ["Deadlift", "Sumo Deadlift"]: return 3
  elif exercise in ["Back Squat", "Front Squat"]: return 2
  elif exercise in ["Overhead Press", "Push Press"]: return 1 

# returns sorted dictionary containing updated lifts
def lift_difference(new_lifts, one_RM=False, lifts_reps=False, path=db_paths["big_lifts.db"]):
  difference = None
  if one_RM:
    db_lifts = set(": ".join([exercise, weight]) for exercise, weight in json.loads(fetch_one_rep_maxes(path)).items())
    new_lifts = set(": ".join([exercise, weight]) for exercise, weight in new_lifts.items() if not weight == '0.0')
    diff = list(new_lifts.difference(db_lifts)) # local lifts that are not in db
    difference = {exercise.split(": ")[0]:exercise.split(": ")[1] for exercise in diff}
  elif lifts_reps:
    db_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in json.loads(fetch_lifts_for_reps(path)).items())
    new_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in new_lifts.items() if not values[1] == '0.0')
    diff = list(new_lifts.difference(db_lifts))
    difference = {exercise.split(":")[0]:exercise.split(":")[1].split("x") for exercise in diff}
  return {key: value for key, value in sorted(difference.items(), key=lambda exercise: sort_exercises(exercise[0]))}

def delete_history_entry(entry_index, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  lift_history = json.loads(fetch_lift_history(path))
  lift_history = [lift for lift in lift_history if not lift[-1] == entry_index]
  
  update_query1 = "UPDATE big_lifts SET lift_history='%s' WHERE email='%s'" % (json.dumps(lift_history), email)
  update_query2 = "UPDATE big_lifts SET lift_history=NULL WHERE email='%s'" % (email)
  update = update_query1 if not len(lift_history) == 0 else update_query2
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(update)

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update)

def convert_lift_history_weight(convert_to_units, path=db_paths["big_lifts.db"], user_path=db_paths["profile.db"]):
  email = fetch_email(user_path)
  try:
    lift_history = json.loads(fetch_lift_history(path))
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

  with sqlite3.connect(path) as conn:
    cursor = conn.cursor()
    cursor.execute(update)
