import json
import psycopg2
from datetime import datetime
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import logged_in_user_email

def table_exists(sqlite_cursor):
  sqlite_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='nutrition'")
  if sqlite_cursor.fetchone()[0] == 0: return False
  return True

def table_is_empty(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor) 
  sqlite_cursor.execute("SELECT COUNT (*) FROM 'nutrition' WHERE email=?", (email,))
  if sqlite_cursor.fetchone()[0] == 0: return True
  return False

def fetch_calorie_goal(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor) 
  sqlite_cursor.execute("SELECT calorie_goal FROM 'nutrition' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_meal_plans(sqlite_cursor):
  email = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("SELECT meal_plans FROM 'nutrition' WHERE email=?", (email,))
  return sqlite_cursor.fetchone()[0]

def fetch_nutrition_data(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor) 
  
  pg_cursor.execute("SELECT * FROM nutrition WHERE email=%s", (email,))
  nutrition_data = pg_cursor.fetchall()[0][:-1]

  calorie_goal = nutrition_data[1]
  meal_plans = nutrition_data[2]
  manage_meals = nutrition_data[3]
  
  if table_is_empty(sqlite_cursor):
    insert_query = "INSERT INTO 'nutrition' (email, calorie_goal, meal_plans, manage_meals) VALUES (?, ?, ?, ?)"
    sqlite_cursor.execute(insert_query, (email, calorie_goal, meal_plans, manage_meals,))
    sqlite_connection.commit()

def update_calorie_goal(calorie_goal, sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor) 
  
  pg_cursor.execute("UPDATE nutrition SET calorie_goal=%s WHERE email=%s", (calorie_goal, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'nutrition' SET calorie_goal=? WHERE email=?", (calorie_goal, email,))
  sqlite_connection.commit()
   
def create_nutrition_table(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  create_table = """
                 CREATE TABLE IF NOT EXISTS
                 'nutrition' (
                 email text,
                 calorie_goal text,
                 meal_plans text,
                 manage_meals text,
                 ID integer NOT NULL,
                 PRIMARY KEY(ID));
                 """
  sqlite_cursor.execute(create_table)
  sqlite_connection.commit()

def insert_default_meal_plans_values(sqlite_connection, pg_connection, calorie_goal=None):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  days_in_a_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  default_meal_names = ["Breakfast", "Lunch", "Snack", "Dinner"]
  meals = {"Past": [], "Present": [], "Future":[], "Current Week Number": int(datetime.now().strftime("%V"))}
  for time in meals:
    if not time == "Past" and not time == "Current Week Number":
      this_week_meals = {}
      for day in days_in_a_week:
        day_dict = {}
        for meal in default_meal_names:
          day_dict[meal] = []
        this_week_meals[day] = day_dict
      meals[time] = this_week_meals
   
  default_values = {"email": email, "meal_plans": json.dumps(meals), "manage_meals": json.dumps(default_meal_names)}
  if (calorie_goal != None): default_values["calorie_goal"] = calorie_goal

  columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_values.keys()))
  values = tuple(value for value in default_values.values())
  
  try:
    pg_cursor.execute(sql.SQL("INSERT INTO nutrition ({columns}) VALUES %s").format(columns=columns), (values,))
    pg_connection.commit()
    if not table_exists(sqlite_cursor): create_nutrition_table(sqlite_connection)
    sqlite_cursor.execute("INSERT INTO 'nutrition' {columns} VALUES {values}".format(columns=tuple(default_values.keys()), values=tuple(default_values.values())))
    sqlite_connection.commit()
  except psycopg2.errors.UniqueViolation:
    pg_cursor.execute("ROLLBACK")
    pg_connection.commit()
    fetch_nutrition_data(sqlite_connection, pg_connection)

def modify_meal(action, meal_to_modify, sqlite_connection, pg_connection, day=None, modify_to=None, this_week=False, next_week=False):
  assert action in ("Add", "Delete", "Rename")
  assert this_week != False or next_week != False
  assert day != None
  if action == "Rename": assert modify_to != None
  elif action == "Add": assert modify_to == None
   
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  fetched_meal_plans = json.loads(fetch_meal_plans(sqlite_cursor))
  when = [("Present" if this_week == True else None), ("Future" if next_week == True else None)]
  
  for time in fetched_meal_plans:
    if not time == "Past" and not time == "Current Week Number" and time in when:
      for day_in_a_week in fetched_meal_plans[time]:
        for meal in fetched_meal_plans[time][day_in_a_week].copy():
          
          if action == "Delete" and meal == meal_to_modify and day_in_a_week == day:
            del fetched_meal_plans[time][day_in_a_week][meal_to_modify]

          elif action == "Add" and day_in_a_week == day and not meal_to_modify in fetched_meal_plans[time][day]:
            fetched_meal_plans[time][day][meal_to_modify] = []

          elif action == "Rename" and meal == meal_to_modify and day_in_a_week == day:
            fetched_meal_plans[time][day][modify_to] = fetched_meal_plans[time][day][meal_to_modify]
            del fetched_meal_plans[time][day][meal_to_modify]
  
  new_meal_plans = json.dumps(fetched_meal_plans)
  
  pg_cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))
  sqlite_connection.commit()

def update_meal(meal_name, food_info, day, sqlite_connection, pg_connection, this_week=False, next_week=False):
  assert this_week != False or next_week != False
  assert not (this_week == True and next_week == True)
  
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  time = "Present" if this_week == True else "Future"
  email = logged_in_user_email(sqlite_cursor)
  fetched_meal_plans = json.loads(fetch_meal_plans(sqlite_cursor))

  fetched_meal_plans[time][day][meal_name].append(food_info)

  new_meal_plans = json.dumps(fetched_meal_plans)

  pg_cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))
  sqlite_connection.commit()

def rotate_meals(sqlite_connection, pg_connection):
  sqlite_cursor = sqlite_connection.cursor()
  pg_cursor = pg_connection.cursor()
  email = logged_in_user_email(sqlite_cursor)
  fetched_meal_plans = json.loads(fetch_meal_plans(sqlite_cursor))
  fetched_meal_plans["Current Week Number"] = int(datetime.now().strftime("%V"))
  
  if (len(fetched_meal_plans["Past"]) == 8): del fetched_meal_plans["Past"][0]
  
  fetched_meal_plans["Past"].append(fetched_meal_plans["Present"])
 
  fetched_meal_plans["Present"] = fetched_meal_plans["Future"]
  
  days_in_a_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  default_meal_names = ["Breakfast", "Lunch", "Snack", "Dinner"]
  default_future = {}
  for day in days_in_a_week:
    day_dict = {}
    for meal in default_meal_names:
      day_dict[meal] = []
    default_future[day] = day_dict
  fetched_meal_plans["Future"] = default_future
  
  new_meal_plans = json.dumps(fetched_meal_plans)

  pg_cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))
  pg_connection.commit()

  sqlite_cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))
  sqlite_connection.commit()
