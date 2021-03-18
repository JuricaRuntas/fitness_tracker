import json
from psycopg2 import sql
import sqlite3
from fitness_tracker.common.units_conversion import kg_to_pounds, pounds_to_kg

def logged_in_user_email(cursor):
  try:
    cursor.execute("SELECT email FROM 'users' WHERE logged_in='YES'")
    return cursor.fetchone()[0]
  except TypeError: # all users have "logged_in='NO'"
    pass

def fetch_username(cursor):
  try:
    email = logged_in_user_email(cursor)
    cursor.execute("SELECT name FROM 'users' WHERE email=?", (email,))
    return cursor.fetchone()[0]
  except (sqlite3.OperationalError, TypeError): # titlebar will raise this error if users table doesn't exist
    pass

def fetch_units(cursor):
  email = logged_in_user_email(cursor)
  cursor.execute("SELECT units FROM 'users' WHERE email=?", (email,))
  return cursor.fetchone()[0]

def fetch_local_user_data(cursor):
  email = logged_in_user_email(cursor)
  cursor.execute("SELECT * FROM 'users' WHERE email=?", (email,))
  fetched_info = cursor.fetchall()[0][2:-2]
  info = ["Name", "Age", "Gender", "Units", "Weight", "Height", "Goal", "Goal Params", "Weight Goal"]
  user_info_dict = {}
  for (fetched, category) in zip(fetched_info, info):
    if category != "Goal Params": user_info_dict[category] = fetched
    else: user_info_dict[category] = json.loads(fetched)
  return user_info_dict

def set_weight(user_data):
  # 4th column of user table is currently weight
  weight = user_data[4]
  if "metric" in user_data: return " ".join([str(weight), "kg"])
  elif "imperial" in user_data: return " ".join([str(weight), "lb"])
  
def convert_weight(current_units, weight):
  if current_units == "metric":
    return kg_to_pounds(float(weight))
  elif current_units == "imperial":
    return pounds_to_kg(float(weight))

def update_user_info_parameter(sqlite_connection, pg_connection, parameter, value):
  assert parameter in ("weight", "height", "gender", "age", "name", "goal", "goalparams", "goalweight") 
  
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  
  email = logged_in_user_email(sqlite_cursor)
  
  if parameter == "goalparams": value = json.dumps(value)

  pg_cursor.execute(sql.SQL("UPDATE users SET {}=%s WHERE email=%s").format(sql.Identifier(parameter)), (value, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'users' SET %s=? WHERE email=?" % parameter, (value, email,))
  sqlite_connection.commit()

def update_units(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()

  email = logged_in_user_email(sqlite_cursor)
  
  sqlite_cursor.execute("SELECT units FROM 'users' WHERE email=?", (email,))
  
  set_units_imperial = "UPDATE 'users' SET units='imperial' WHERE email=?"
  set_units_metric = "UPDATE 'users' SET units='metric' WHERE email=?"

  update_units = set_units_imperial if sqlite_cursor.fetchone()[0] == "metric" else set_units_metric
  
  sqlite_cursor.execute(update_units, (email,))
  sqlite_connection.commit()

  set_units_imperial = "UPDATE users SET units='imperial' WHERE email=%s"
  set_units_metric = "UPDATE users SET units='metric' WHERE email=%s"
  update_units = set_units_imperial if current_units == "metric" else set_units_metric
  pg_cursor.execute(update_units, (email,))
  pg_connection.commit()
