import json
import psycopg2
from datetime import datetime
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import logged_in_user_email

def weight_loss_table_is_empty(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT COUNT (*) FROM 'weight_loss' WHERE email=?", (email,))
  if sqlite_cursor.fetchone()[0] == 0: return True
  return False

def create_weight_loss_table(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  create_table = """
                 CREATE TABLE IF NOT EXISTS
                 'weight_loss' (
                 email text,
                 weight_history text,
                 preferred_activity text,
                 cardio_history text,
                 ID integer NOT NULL,
                 PRIMARY KEY(ID));
                 """
  sqlite_cursor.execute(create_table)
  sqlite_connection.commit()

def fetch_user_weight_loss_table_data(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)

  pg_cursor.execute("SELECT * FROM weight_loss WHERE email=%s", (email,))
  weight_loss_data = pg_cursor.fetchall()[0][:-1]

  weight_history = weight_loss_data[1]
  preferred_activity = weight_loss_data[2]
  cardio_history = weight_loss_data[3]

  if weight_loss_table_is_empty(sqlite_cursor):
    insert = "INSERT INTO 'weight_loss' (email, weight_history, preferred_activity, cardio_history) VALUES (?, ?, ?, ?)"
    sqlite_cursor.execute(insert, (email, weight_history, preferred_activity, cardio_history,))
    sqlite_connection.commit()

def insert_default_weight_loss_values(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  current_date = datetime.today().strftime("%d/%m/%Y")
  default_weight_history, default_cardio_history = {}, {}
  default_activities = ["Running", "Walking", "Cycling", "Swimming"]
  default_preferred_activity = "Running"
  
  default_cardio_history[current_date] = {}
  for activity in default_activities:
    default_cardio_history[current_date][activity] = []

  default_dict = {"email": email, "weight_history": json.dumps(default_weight_history),
                  "preferred_activity": default_preferred_activity,
                  "cardio_history": json.dumps(default_cardio_history)}

  try:
    columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_dict.keys()))
    values = tuple(value for value in default_dict.values())
    pg_cursor.execute(sql.SQL("INSERT INTO weight_loss ({columns}) VALUES %s").format(columns=columns), (values,))
    pg_connection.commit()

    sqlite_cursor.execute("INSERT INTO 'weight_loss' {columns} VALUES {values}".format(columns=tuple(default_dict.keys()), values=tuple(default_dict.values())))
    sqlite_connection.commit()
  except psycopg2.errors.UniqueViolation:
    pg_cursor.execute("ROLLBACK")
    pg_connection.commit()
    fetch_user_weight_loss_table_data(sqlite_connection, pg_connection)

def fetch_preferred_activity(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT preferred_activity FROM 'weight_loss' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def update_preferred_activity(new_activity, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)

  pg_cursor.execute("UPDATE weight_loss SET preferred_activity=%s WHERE email=%s", (new_activity, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET preferred_activity=? WHERE email=?", (new_activity, email,))
  sqlite_connection.commit()

def fetch_weight_history(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT weight_history FROM 'weight_loss' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def update_weight_history(date, weight, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  
  current_weight_history = json.loads(fetch_weight_history(sqlite_cursor))
  current_weight_history[date] = weight
  current_weight_history = json.dumps(current_weight_history)
  
  pg_cursor.execute("UPDATE weight_loss SET weight_history=%s WHERE email=%s", (current_weight_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET weight_history=? WHERE email=?", (current_weight_history, email,))
  sqlite_connection.commit()

def delete_weight_history_entry(date, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  weight_history = json.loads(fetch_weight_history(sqlite_cursor))

  if date in weight_history: del weight_history[date]

  pg_cursor.execute("UPDATE weight_loss SET weight_history=%s WHERE email=%s", (json.dumps(weight_history), email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET weight_history=? WHERE email=?", (json.dumps(weight_history), email,))
  sqlite_connection.commit()

def fetch_cardio_history(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT cardio_history FROM 'weight_loss' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def add_date_to_cardio_history(date, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  activities = ["Running", "Walking", "Cycling", "Swimming"]
  cardio_history = json.loads(fetch_cardio_history(sqlite_cursor))
  
  cardio_history[date] = {}
  for activity in activities:
    cardio_history[date][activity] = []
  
  cardio_history = json.dumps(cardio_history)

  pg_cursor.execute("UPDATE weight_loss SET cardio_history=%s WHERE email=%s", (cardio_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET cardio_history=? WHERE email=?", (cardio_history, email,))
  sqlite_connection.commit()

def add_cardio_entry_to_cardio_history(activity, duration, distance, calories_burnt, sqlite_connection, pg_connection):
  assert activity in ("Running", "Walking", "Cycling", "Swimming")
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  current_cardio_history = json.loads(fetch_cardio_history(sqlite_cursor))
  email = logged_in_user_email(sqlite_cursor)
  date = datetime.today().strftime("%d/%m/%Y")

  new_entry = {"Time Spent": str(duration), "Distance Travelled": str(distance), "Calories Burnt": str(calories_burnt)}
  current_cardio_history[date][activity].append(new_entry)
  current_cardio_history = json.dumps(current_cardio_history)

  pg_cursor.execute("UPDATE weight_loss SET cardio_history=%s WHERE email=%s", (current_cardio_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET cardio_history=? WHERE email=?", (current_cardio_history, email,))
  sqlite_connection.commit()

def update_cardio_entry(date, activity, new_activity_entry, entry_index, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  current_cardio_history = json.loads(fetch_cardio_history(sqlite_cursor))
  email = logged_in_user_email(sqlite_cursor)
  
  current_cardio_history[date][activity][entry_index] = new_activity_entry 
  current_cardio_history = json.dumps(current_cardio_history)

  pg_cursor.execute("UPDATE weight_loss SET cardio_history=%s WHERE email=%s", (current_cardio_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET cardio_history=? WHERE email=?", (current_cardio_history, email,))
  sqlite_connection.commit()

def delete_cardio_entry(date, activity, index, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  current_cardio_history = json.loads(fetch_cardio_history(sqlite_cursor))
  email = logged_in_user_email(sqlite_cursor)
  
  del current_cardio_history[date][activity][index]
  current_cardio_history = json.dumps(current_cardio_history)
  
  pg_cursor.execute("UPDATE weight_loss SET cardio_history=%s WHERE email=%s", (current_cardio_history, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'weight_loss' SET cardio_history=? WHERE email=?", (current_cardio_history, email,))
  sqlite_connection.commit()
