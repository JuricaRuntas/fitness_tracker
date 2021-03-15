import sys
import sqlite3
import psycopg2
import json
from datetime import datetime
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import fetch_units, logged_in_user_email
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg
from fitness_tracker.config import db_path, db_info

def table_is_empty(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM 'big_lifts' WHERE email=?", (email,))
    if cursor.fetchone()[0] == 0: return True
  return False

def fetch_units_from_big_lifts(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT units FROM 'big_lifts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_one_rep_maxes(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("""SELECT one_rep_maxes FROM 'big_lifts' WHERE email=?""", (email,))
    return cursor.fetchone()[0]

def fetch_lifts_for_reps(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lifts_for_reps FROM 'big_lifts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_preferred_lifts(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT preferred_lifts FROM 'big_lifts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_lift_history(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT lift_history FROM 'big_lifts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_rm_history(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT rm_history FROM 'big_lifts' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_user_rm_history(db_path=db_path):
  email = logged_in_user_email(db_path)
  rm_history = None
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT rm_history FROM big_lifts WHERE email=%s", (email,))
      rm_history = cursor.fetchone()[0]

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (rm_history, email,))
  
  return rm_history

def fetch_user_big_lifts_table_data(db_path=db_path):
  email = logged_in_user_email(db_path)
  big_lifts_data = None

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM big_lifts WHERE email=%s", (email,))
      big_lifts_data = cursor.fetchall()[0][:-1]
  
  one_rep_maxes = big_lifts_data[1]
  lifts_for_reps = big_lifts_data[2]
  preferred_lifts = big_lifts_data[3]
  lift_history = big_lifts_data[4]
  units = big_lifts_data[5]
  rm_history = big_lifts_data[6]

  if table_is_empty(db_path):
    insert_values = """
    INSERT INTO 'big_lifts' (email, one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units, rm_history) VALUES
    (?, ?, ?, ?, ?, ?, ?)
                    """
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute(insert_values, (email, one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units, rm_history,))

def insert_default_values(db_path=db_path):
  email = logged_in_user_email(db_path)
  default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
  secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                         "Squat": "Front Squat", "Vertical Press": "Push Press"}
  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  units = fetch_units(db_path)
  one_RM_dict = json.dumps({exercise:"0" for exercise in default_exercises})
  lifts_for_reps = json.dumps({exercise:["0", "0"] for exercise in default_exercises})
  preferred_lifts = {"Horizontal Press": default_exercises[0],
                     "Floor Pull": default_exercises[1],
                     "Squat": default_exercises[2],
                     "Vertical Press": default_exercises[3]}
  
  current_year = str(datetime.now().year)
  rm_history = {current_year:{}}
  for month in months:
    exercises_dict = {}
    for lift_type in preferred_lifts:
      exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
    for lift_type in secondary_exercises:
      exercises_dict[lift_type][secondary_exercises[lift_type]] = []

    rm_history[current_year][month] = exercises_dict

  default_dict = {"one_rep_maxes": one_RM_dict, "lifts_for_reps": lifts_for_reps,
                  "preferred_lifts": json.dumps(preferred_lifts), "rm_history": json.dumps(rm_history),
                  "email": email, "units": units}

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
        cursor.execute("INSERT INTO 'big_lifts' {columns} VALUES {values}".format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
  except psycopg2.errors.UniqueViolation: # user already has big_lifts table with data on server
    fetch_user_big_lifts_table_data(db_path)

def create_big_lifts_table(db_path=db_path):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    create_table = """
                   CREATE TABLE IF NOT EXISTS
                   'big_lifts' (
                   email text,
                   one_rep_maxes text,
                   lifts_for_reps text,
                   preferred_lifts text,
                   lift_history text,
                   units text,
                   rm_history text,
                   id integer NOT NULL,
                   PRIMARY KEY(id));
                   """
    cursor.execute(create_table)

def update_preferred_lifts(new_preferred_lifts, db_path=db_path):
  email = logged_in_user_email(db_path)
  new_preferred_lifts = json.dumps(new_preferred_lifts)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET preferred_lifts=%s WHERE email=%s", (new_preferred_lifts, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET preferred_lifts=? WHERE email=?", (new_preferred_lifts, email,))

# updates exercises
def update_1RM_and_lifts_for_reps(db_path=db_path):
  email = logged_in_user_email(db_path)
  preferred_lifts = list(json.loads(fetch_preferred_lifts(db_path)).values())
  one_rep_maxes = json.loads(fetch_one_rep_maxes(db_path))
  lifts_for_reps = json.loads(fetch_lifts_for_reps(db_path))

  new_one_rep_maxes = json.dumps({preferred_lifts[i]:value for i, value in enumerate(one_rep_maxes.values())})
  new_lifts_for_reps = json.dumps({preferred_lifts[i]:value for i, value in enumerate(lifts_for_reps.values())})
      
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (new_one_rep_maxes, email,))
      cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (new_lifts_for_reps, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (new_one_rep_maxes, email,))
    cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (new_lifts_for_reps, email,))

# updates weight
def update_1RM_lifts(new_lifts, db_path=db_path):
  email = logged_in_user_email(db_path)
  one_rep_max_lifts = json.loads(fetch_one_rep_maxes(db_path))
  for i, lift in enumerate(one_rep_max_lifts.keys()):
    if not lift in new_lifts: continue
    one_rep_max_lifts[lift] = new_lifts[lift]

  one_rep_max_lifts = json.dumps(one_rep_max_lifts)
 
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (one_rep_max_lifts, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (one_rep_max_lifts, email,))

# updates reps and weight
def update_lifts_for_reps(new_lifts_for_reps, db_path=db_path):
  email = logged_in_user_email(db_path)
  lifts_for_reps = json.loads(fetch_lifts_for_reps(db_path))
  new_lifts_for_reps = list(new_lifts_for_reps.values())
  
  for i, lift in enumerate(lifts_for_reps.keys()):
    lifts_for_reps[lift] = new_lifts_for_reps[i]

  lifts_for_reps = json.dumps(lifts_for_reps)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (lifts_for_reps, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (lifts_for_reps, email,))

def update_lift_history(lift_history, db_path=db_path):
  email = logged_in_user_email(db_path)
  current_lift_history = fetch_lift_history(db_path)
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
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (new_lift_history, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (new_lift_history, email,))

def update_big_lifts_units(db_path=db_path):
  email = logged_in_user_email(db_path)
  units = fetch_units(db_path)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET units=%s WHERE email=%s", (units, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET units=? WHERE email=?", (units, email,))

def update_one_rep_maxes_history(new_values, year, db_path=db_path):
  email = logged_in_user_email(db_path)
  rm_history = json.loads(fetch_rm_history(db_path))
  preferred_lifts = json.loads(fetch_preferred_lifts(db_path))
  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  now = datetime.now()

  if year not in rm_history:
    rm_history[year] = {} 
    for month in months:
      exercises_dict = {}
      for lift_type in preferred_lifts:
        exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
      rm_history[year][month] = exercises_dict
  
  for i, (lift, weight) in enumerate(new_values.items()):
    current_lift_type = rm_history[year][months[now.month-1]][list(preferred_lifts.keys())[i]]
    if lift not in current_lift_type: current_lift_type[lift] = []
    current_lift_type[lift].append(weight) 
  
  rm_history = json.dumps(rm_history)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET rm_history=%s WHERE email=%s", (rm_history, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (rm_history, email,))

def add_year_to_rm_history(year):
  email = logged_in_user_email()
  rm_history = json.loads(fetch_rm_history())
  preferred_lifts = json.loads(fetch_preferred_lifts())
  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  new_year = {}
  for month in months:
    exercises_dict = {}
    for lift_type in preferred_lifts:
      exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
    new_year[month] = exercises_dict

  rm_history[str(year)] = new_year

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET rm_history=%s WHERE email=%s", (json.dumps(rm_history), email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (json.dumps(rm_history), email,))

def clear_one_rep_maxes():
  email = logged_in_user_email()
  one_rep_maxes = json.loads(fetch_one_rep_maxes())
  for exercise, value in one_rep_maxes.items():
    one_rep_maxes[exercise] = "0"

  one_rep_maxes = json.dumps(one_rep_maxes)
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (one_rep_maxes, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (one_rep_maxes, email,))

def clear_lifts_for_reps():
  email = logged_in_user_email()
  lifts_for_reps = json.loads(fetch_lifts_for_reps())
  for exercise, values in lifts_for_reps.items():
    lifts_for_reps[exercise] = ["0", "0"]

  lifts_for_reps = json.dumps(lifts_for_reps)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (lifts_for_reps, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (lifts_for_reps, email,))

def sort_exercises(exercise):
  if exercise in ["Bench Press", "Incline Bench Press"]: return 4
  elif exercise in ["Deadlift", "Sumo Deadlift"]: return 3
  elif exercise in ["Back Squat", "Front Squat"]: return 2
  elif exercise in ["Overhead Press", "Push Press"]: return 1 

# returns sorted dictionary containing updated lifts
def lift_difference(new_lifts, db_path=db_path, one_RM=False, lifts_reps=False):
  difference = None
  if one_RM:
    db_lifts = set(": ".join([exercise, weight]) for exercise, weight in json.loads(fetch_one_rep_maxes(db_path)).items())
    new_lifts = set(": ".join([exercise, weight]) for exercise, weight in new_lifts.items() if not weight == '0.0')
    diff = list(new_lifts.difference(db_lifts)) # local lifts that are not in db
    difference = {exercise.split(": ")[0]:exercise.split(": ")[1] for exercise in diff}
  elif lifts_reps:
    db_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in json.loads(fetch_lifts_for_reps(db_path)).items())
    new_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in new_lifts.items() if not values[1] == '0.0')
    diff = list(new_lifts.difference(db_lifts))
    difference = {exercise.split(":")[0]:exercise.split(":")[1].split("x") for exercise in diff}
  return {key: value for key, value in sorted(difference.items(), key=lambda exercise: sort_exercises(exercise[0]))}

def delete_history_entry(entry_index, db_path=db_path):
  email = logged_in_user_email(db_path)
  lift_history = json.loads(fetch_lift_history(db_path))
  lift_history = [lift for lift in lift_history if not lift[-1] == entry_index]
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      if not len(lift_history) == 0:
        cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (json.dumps(lift_history), email,))
      else:
        cursor.execute("UPDATE big_lifts SET lift_history=NULL WHERE email=%s", (email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    if not len(lift_history) == 0:
      cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (json.dumps(lift_history), email,))
    else:
      cursor.execute("UPDATE 'big_lifts' SET lift_history=NULL WHERE email=?", (email,))

def convert_lift_history_weight(convert_to_units, db_path=db_path):
  email = logged_in_user_email(db_path)
  try:
    lift_history = json.loads(fetch_lift_history(db_path))
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
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (json.dumps(lift_history), email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (json.dumps(lift_history), email,))
