import sys
import json
import psycopg2
from datetime import datetime
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import fetch_units, logged_in_user_email
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg
from fitness_tracker.config import db_path, db_info

def table_is_empty(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT COUNT (*) FROM 'big_lifts' WHERE email=?", (email,))
  if sqlite_cursor.fetchone()[0] == 0: return True
  return False

def fetch_units_from_big_lifts(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT units FROM 'big_lifts' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_one_rep_maxes(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("""SELECT one_rep_maxes FROM 'big_lifts' WHERE email=?""", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_lifts_for_reps(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT lifts_for_reps FROM 'big_lifts' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_preferred_lifts(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT preferred_lifts FROM 'big_lifts' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_lift_history(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT lift_history FROM 'big_lifts' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_rm_history(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT rm_history FROM 'big_lifts' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_user_rm_history(sqlite_connection, pg_cursor):
  sqlite_cursor = sqlite_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  
  pg_cursor.execute("SELECT rm_history FROM big_lifts WHERE email=%s", (email,))
  rm_history = cursor.fetchone()[0]

  sqlite_cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (rm_history, email,))
  sqlite_connection.commit()

  return rm_history

def fetch_user_big_lifts_table_data(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)

  pg_cursor.execute("SELECT * FROM big_lifts WHERE email=%s", (email,))
  big_lifts_data = pg_cursor.fetchall()[0][:-1]
  
  one_rep_maxes = big_lifts_data[1]
  lifts_for_reps = big_lifts_data[2]
  preferred_lifts = big_lifts_data[3]
  lift_history = big_lifts_data[4]
  units = big_lifts_data[5]
  rm_history = big_lifts_data[6]

  if table_is_empty(sqlite_cursor):
    insert_values = """
    INSERT INTO 'big_lifts' (email, one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units, rm_history) VALUES
    (?, ?, ?, ?, ?, ?, ?)
                    """
    sqlite_cursor.execute(insert_values, (email, one_rep_maxes, lifts_for_reps, preferred_lifts, lift_history, units, rm_history,))
    sqlite_connection.commit()

def insert_default_values(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
  secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                         "Squat": "Front Squat", "Vertical Press": "Push Press"}
  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  units = fetch_units(sqlite_cursor)
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
    columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_dict.keys()))
    values = tuple(value for value in default_dict.values())
    pg_cursor.execute(sql.SQL("INSERT INTO big_lifts ({columns}) VALUES %s").format(columns=columns), (values,))
    pg_connection.commit()

    sqlite_cursor.execute("INSERT INTO 'big_lifts' {columns} VALUES {values}".format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
    sqlite_connection.commit()
  except psycopg2.errors.UniqueViolation: # user already has big_lifts table with data on server
    pg_cursor.execute("ROLLBACK")
    pg_connection.commit()
    fetch_user_big_lifts_table_data(sqlite_connection, pg_connection)

def create_big_lifts_table(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
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
  sqlite_cursor.execute(create_table)
  sqlite_connection.commit()

def update_preferred_lifts(new_preferred_lifts, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  new_preferred_lifts = json.dumps(new_preferred_lifts)
  
  pg_cursor.execute("UPDATE big_lifts SET preferred_lifts=%s WHERE email=%s", (new_preferred_lifts, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET preferred_lifts=? WHERE email=?", (new_preferred_lifts, email,))
  sqlite_connection.commit()

# updates exercises
def update_1RM_and_lifts_for_reps(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  preferred_lifts = list(json.loads(fetch_preferred_lifts(sqlite_cursor)).values())
  one_rep_maxes = json.loads(fetch_one_rep_maxes(sqlite_cursor))
  lifts_for_reps = json.loads(fetch_lifts_for_reps(sqlite_cursor))

  new_one_rep_maxes = json.dumps({preferred_lifts[i]:value for i, value in enumerate(one_rep_maxes.values())})
  new_lifts_for_reps = json.dumps({preferred_lifts[i]:value for i, value in enumerate(lifts_for_reps.values())})
      
  pg_cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (new_one_rep_maxes, email,))
  pg_cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (new_lifts_for_reps, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (new_one_rep_maxes, email,))
  sqlite_cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (new_lifts_for_reps, email,))
  sqlite_connection.commit()

# updates weight
def update_1RM_lifts(new_lifts, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  one_rep_max_lifts = json.loads(fetch_one_rep_maxes(sqlite_cursor))
  for i, lift in enumerate(one_rep_max_lifts.keys()):
    if not lift in new_lifts: continue
    one_rep_max_lifts[lift] = new_lifts[lift]

  one_rep_max_lifts = json.dumps(one_rep_max_lifts)
 
  pg_cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (one_rep_max_lifts, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (one_rep_max_lifts, email,))
  sqlite_connection.commit()

# updates reps and weight
def update_lifts_for_reps(new_lifts_for_reps, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  lifts_for_reps = json.loads(fetch_lifts_for_reps(sqlite_cursor))
  new_lifts_for_reps = list(new_lifts_for_reps.values())
  
  for i, lift in enumerate(lifts_for_reps.keys()):
    lifts_for_reps[lift] = new_lifts_for_reps[i]

  lifts_for_reps = json.dumps(lifts_for_reps)

  pg_cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (lifts_for_reps, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (lifts_for_reps, email,))
  sqlite_connection.commit()

def update_lift_history(lift_history, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  current_lift_history = fetch_lift_history(sqlite_cursor)
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
  
  pg_cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (new_lift_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (new_lift_history, email,))
  sqlite_connection.commit()

def update_big_lifts_units(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  units = fetch_units(sqlite_cursor)
  
  pg_cursor.execute("UPDATE big_lifts SET units=%s WHERE email=%s", (units, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET units=? WHERE email=?", (units, email,))
  sqlite_connection.commit()

def update_one_rep_maxes_history(new_values, year, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  rm_history = json.loads(fetch_rm_history(sqlite_cursor))
  preferred_lifts = json.loads(fetch_preferred_lifts(sqlite_cursor))
  default_exercises = {"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                       "Squat": "Back Squat", "Vertical Press": "Overhead Press"}
  secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                         "Squat": "Front Squat", "Vertical Press": "Push Press"}

  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  now = datetime.now()

  if year not in rm_history:
    rm_history[year] = {}
    for month in months:
      exercises_dict = {}
      for lift_type in default_exercises:
        exercises_dict[lift_type] = {default_exercises[lift_type]:[]}
      for lift_type in secondary_exercises:
        exercises_dict[lift_type][secondary_exercises[lift_type]] = []
      rm_history[year][month] = exercises_dict 
  
  for i, (lift, weight) in enumerate(new_values.items()):
    current_lift_type = rm_history[year][months[now.month-1]][list(preferred_lifts.keys())[i]]
    if lift not in current_lift_type: current_lift_type[lift] = []
    current_lift_type[lift].append(weight) 
  
  rm_history = json.dumps(rm_history)

  pg_cursor.execute("UPDATE big_lifts SET rm_history=%s WHERE email=%s", (rm_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (rm_history, email,))
  sqlite_connection.commit()

def add_year_to_rm_history(year, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  rm_history = json.loads(fetch_rm_history(sqlite_cursor))
  preferred_lifts = json.loads(fetch_preferred_lifts(sqlite_cursor))
  months = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
  new_year = {}
  for month in months:
    exercises_dict = {}
    for lift_type in preferred_lifts:
      exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
    new_year[month] = exercises_dict

  rm_history[str(year)] = new_year

  pg_cursor.execute("UPDATE big_lifts SET rm_history=%s WHERE email=%s", (json.dumps(rm_history), email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET rm_history=? WHERE email=?", (json.dumps(rm_history), email,))
  sqlite_connection.commit()

def clear_one_rep_maxes(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  one_rep_maxes = json.loads(fetch_one_rep_maxes(sqlite_cursor))
  for exercise, value in one_rep_maxes.items():
    one_rep_maxes[exercise] = "0"

  one_rep_maxes = json.dumps(one_rep_maxes)
  
  pg_cursor.execute("UPDATE big_lifts SET one_rep_maxes=%s WHERE email=%s", (one_rep_maxes, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET one_rep_maxes=? WHERE email=?", (one_rep_maxes, email,))
  sqlite_connection.commit()

def clear_lifts_for_reps(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  lifts_for_reps = json.loads(fetch_lifts_for_reps(sqlite_cursor))
  for exercise, values in lifts_for_reps.items():
    lifts_for_reps[exercise] = ["0", "0"]

  lifts_for_reps = json.dumps(lifts_for_reps)

  pg_cursor.execute("UPDATE big_lifts SET lifts_for_reps=%s WHERE email=%s", (lifts_for_reps, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET lifts_for_reps=? WHERE email=?", (lifts_for_reps, email,))
  sqlite_connection.commit()

def sort_exercises(exercise):
  if exercise in ["Bench Press", "Incline Bench Press"]: return 4
  elif exercise in ["Deadlift", "Sumo Deadlift"]: return 3
  elif exercise in ["Back Squat", "Front Squat"]: return 2
  elif exercise in ["Overhead Press", "Push Press"]: return 1 

# returns sorted dictionary containing updated lifts
def lift_difference(new_lifts, sqlite_cursor, one_RM=False, lifts_reps=False):
  difference = None
  if one_RM:
    db_lifts = set(": ".join([exercise, weight]) for exercise, weight in json.loads(fetch_one_rep_maxes(sqlite_cursor)).items())
    new_lifts = set(": ".join([exercise, weight]) for exercise, weight in new_lifts.items() if not weight == '0.0')
    diff = list(new_lifts.difference(db_lifts)) # local lifts that are not in db
    difference = {exercise.split(": ")[0]:exercise.split(": ")[1] for exercise in diff}
  elif lifts_reps:
    db_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in json.loads(fetch_lifts_for_reps(sqlite_cursor)).items())
    new_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in new_lifts.items() if not values[1] == '0.0')
    diff = list(new_lifts.difference(db_lifts))
    difference = {exercise.split(":")[0]:exercise.split(":")[1].split("x") for exercise in diff}
  return {key: value for key, value in sorted(difference.items(), key=lambda exercise: sort_exercises(exercise[0]))}

def delete_history_entry(entry_index, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  lift_history = json.loads(fetch_lift_history(sqlite_cursor))
  lift_history = [lift for lift in lift_history if not lift[-1] == entry_index]
  
  if not len(lift_history) == 0:
    pg_cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (json.dumps(lift_history), email,))
  else:
    pg_cursor.execute("UPDATE big_lifts SET lift_history=NULL WHERE email=%s", (email,))
  pg_connection.commit()

  if not len(lift_history) == 0:
    sqlite_cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (json.dumps(lift_history), email,))
  else:
    sqlite_cursor.execute("UPDATE 'big_lifts' SET lift_history=NULL WHERE email=?", (email,))
  sqlite_connection.commit()

def convert_lift_history_weight(convert_to_units, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  try:
    lift_history = json.loads(fetch_lift_history(sqlite_cursor))
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
  
  pg_cursor.execute("UPDATE big_lifts SET lift_history=%s WHERE email=%s", (json.dumps(lift_history), email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'big_lifts' SET lift_history=? WHERE email=?", (json.dumps(lift_history), email,))
  sqlite_connection.commit()
