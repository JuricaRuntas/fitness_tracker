import sqlite3
import psycopg2
import json
from datetime import datetime
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_path, db_info

def table_exists(db_path=db_path):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='nutrition'")
    if cursor.fetchone()[0] == 0: return False
  return True

def table_is_empty(db_path=db_path):
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT (*) FROM 'nutrition' WHERE email=?", (email,))
    if cursor.fetchone()[0] == 0: return True
  return False

def fetch_calorie_goal():
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT calorie_goal FROM 'nutrition' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_meal_plans(db_path=db_path):
  email = logged_in_user_email(db_path)
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT meal_plans FROM 'nutrition' WHERE email=?", (email,))
    return cursor.fetchone()[0]

def fetch_nutrition_data(db_path=db_path):
  email = logged_in_user_email(db_path) 
  nutrition_data = None
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM nutrition WHERE email=%s", (email,))
      nutrition_data = cursor.fetchall()[0][:-1]
 
  calorie_goal = nutrition_data[1]
  meal_plans = nutrition_data[2]
  manage_meals = nutrition_data[3]
  
  if table_is_empty(db_path):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      insert_query = "INSERT INTO 'nutrition' (email, calorie_goal, meal_plans, manage_meals) VALUES (?, ?, ?, ?)"
      cursor.execute(insert_query, (email, calorie_goal, meal_plans, manage_meals,))

def update_calorie_goal(calorie_goal, db_path=db_path):
  email = logged_in_user_email(db_path) 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'nutrition' SET calorie_goal=?", (calorie_goal,))
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET calorie_goal=%s WHERE email=%s", (calorie_goal, email,))

def create_nutrition_table(db_path=db_path):
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
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
    cursor.execute(create_table)

def insert_default_meal_plans_values(db_path=db_path, calorie_goal=None):
  email = logged_in_user_email(db_path)
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
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql.SQL("INSERT INTO nutrition ({columns}) VALUES %s").format(columns=columns), (values,))
    
    if not table_exists(db_path): create_nutrition_table(db_path)
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO 'nutrition' {columns} VALUES {values}".format(columns=tuple(default_values.keys()), values=tuple(default_values.values())))
  except psycopg2.errors.UniqueViolation:
    fetch_nutrition_data(db_path)

def modify_meal(action, meal_to_modify, day=None, modify_to=None, this_week=False, next_week=False, db_path=db_path):
  assert action in ("Add", "Delete", "Rename")
  assert this_week != False or next_week != False
  assert day != None
  if action == "Rename": assert modify_to != None
  elif action == "Add": assert modify_to == None
   
  email = logged_in_user_email(db_path)
  fetched_meal_plans = json.loads(fetch_meal_plans(db_path))
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
  
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))

def update_meal(meal_name, food_info, day, this_week=False, next_week=False, db_path=db_path):
  assert this_week != False or next_week != False
  assert not (this_week == True and next_week == True)
  
  time = "Present" if this_week == True else "Future"
  email = logged_in_user_email(db_path)
  fetched_meal_plans = json.loads(fetch_meal_plans(db_path))

  fetched_meal_plans[time][day][meal_name].append(food_info)

  new_meal_plans = json.dumps(fetched_meal_plans)

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))

def rotate_meals(db_path=db_path):
  email = logged_in_user_email(db_path)
  fetched_meal_plans = json.loads(fetch_meal_plans(db_path))
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

  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("UPDATE nutrition SET meal_plans=%s WHERE email=%s", (new_meal_plans, email,))

  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'nutrition' SET meal_plans=? WHERE email=?", (new_meal_plans, email,))
