import os
import importlib
import sqlite3
import psycopg2
import hashlib
import json
from datetime import datetime
from psycopg2 import sql

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

class DatabaseWrapper(metaclass=Singleton):
  db_path = os.path.join(os.path.dirname(importlib.util.find_spec("fitness_tracker").origin), "fitness_tracker.db")
  
  def __init__(self, db_path=None):
    db_path = self.db_path if db_path == None else db_path

    self.db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
                    "database": "postgres", "user": "admin", "password": os.environ["FT_ADMIN_PASSWORD"]}

    self.sqlite_connection = sqlite3.connect(db_path)
    self.pg_connection = psycopg2.connect(**self.db_info)
    
    self.sqlite_cursor = self.sqlite_connection.cursor()
    self.pg_cursor = self.pg_connection.cursor() 
    
    self.table_names = {"Users": "users", "Compound Exercises": "big_lifts", "Nutrition": "nutrition",
                        "Weight Loss": "weight_loss", "Workouts": "workouts"}

    self.table_columns = {"Users": ("email", "password", "name", "age", "gender", "units", "weight", "height", "goal",
                                    "goalparams", "goalweight"),
                          "Compound Exercises": ("email", "one_rep_maxes", "lifts_for_reps", "preferred_lifts", "lift_history",
                                                 "units", "rm_history"),
                          "Nutrition": ("email", "calorie_goal", "meal_plans", "manage_meals"),
                          "Weight Loss": ("email", "weight_history", "preferred_activity", "cardio_history"),
                          "Workouts": ("email", "workouts", "current_workout_plan")}

    self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                   'August', 'September', 'October', 'November', 'December'] 
    
    self.user_email = self.fetch_logged_in_user_email()


  ############################################
  # GENERIC METHODS FOR DATABASE INTERACTION #
  ############################################

  def fetch_logged_in_user_email(self):
    try:
      self.sqlite_cursor.execute("SELECT email FROM "+self.table_names["Users"]+" WHERE logged_in='YES'")
      return self.sqlite_cursor.fetchone()[0]
    except (TypeError, sqlite3.OperationalError): # all users have logged out
      pass
  
  def fetch_local_column(self, table_name, column):
    assert table_name in self.table_names.keys()
    assert column in self.table_columns[table_name]
    self.sqlite_cursor.execute("SELECT "+column+" FROM "+self.table_names[table_name]+" WHERE email=?", (self.user_email,))
    return self.sqlite_cursor.fetchone()[0]

  def update_table_column(self, table_name, column_name, value, delete_history_entry=False, update_preferred_lifts=False):
    assert table_name in self.table_names.keys()
    assert column_name in self.table_columns[table_name]
    
    if update_preferred_lifts or column_name == "preferred_lifts":
      value = json.dumps(value)

    elif column_name == "one_rep_maxes":
      one_rep_max_lifts = json.loads(self.fetch_local_column(table_name, column_name))
      for i, lift in enumerate(one_rep_max_lifts.keys()):
        if not lift in value: continue
        one_rep_max_lifts[lift] = value[lift]
      value = json.dumps(one_rep_max_lifts) 
    
    elif column_name == "lifts_for_reps":
      lifts_for_reps = json.loads(self.fetch_local_column(table_name, column_name))       
      value = list(value.values())
      for i, lift in enumerate(lifts_for_reps.keys()):
        lifts_for_reps[lift] = value[i]
      value = json.dumps(lifts_for_reps)

    elif column_name == "lift_history" and not delete_history_entry:
      if value == None: value = "NULL"
      else:
        current_lift_history = self.fetch_local_column(table_name, "lift_history")
        lift_history = [[exercise, value_h] for exercise, value_h in value.items()]
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
        value = new_lift_history

    pg_update_query = "UPDATE {table} SET {column}=%s WHERE email=%s"
    sqlite_update_query = "UPDATE "+self.table_names[table_name]+" SET "+column_name+"=?"+ " WHERE email=?"
    
    self.pg_cursor.execute(sql.SQL(pg_update_query).format(
                           table=sql.Identifier(self.table_names[table_name]),
                           column=sql.Identifier(column_name)), (value, self.user_email,))
    self.pg_connection.commit()

    self.sqlite_cursor.execute(sqlite_update_query, (value, self.user_email,))
    self.sqlite_connection.commit()
  
  def insert_default_values(self, table_name, calorie_goal=None):
    assert table_name in self.table_names.keys()
    default_values = {}
    if table_name == "Nutrition": 
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
         
        default_values = {"email": self.user_email, "meal_plans": json.dumps(meals), "manage_meals": json.dumps(default_meal_names)}
      if (calorie_goal != None): default_values["calorie_goal"] = calorie_goal

    elif table_name == "Compound Exercises":
      default_exercises = ["Bench Press", "Deadlift", "Back Squat", "Overhead Press"]
      secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                             "Squat": "Front Squat", "Vertical Press": "Push Press"} 
      one_RM_dict = json.dumps({exercise:"0" for exercise in default_exercises})
      lifts_for_reps = json.dumps({exercise:["0", "0"] for exercise in default_exercises})
      units = self.fetch_local_column("Users", "units")
      preferred_lifts = {"Horizontal Press": default_exercises[0],
                         "Floor Pull": default_exercises[1],
                         "Squat": default_exercises[2],
                         "Vertical Press": default_exercises[3]}
      current_year = str(datetime.now().year)
      rm_history = {current_year:{}}
      for month in self.months:
        exercises_dict = {}
        for lift_type in preferred_lifts:
          exercises_dict[lift_type] = {preferred_lifts[lift_type]:[]}
        for lift_type in secondary_exercises:
          exercises_dict[lift_type][secondary_exercises[lift_type]] = []
        rm_history[current_year][month] = exercises_dict

      default_values = {"one_rep_maxes": one_RM_dict, "lifts_for_reps": lifts_for_reps,
                        "preferred_lifts": json.dumps(preferred_lifts), "rm_history": json.dumps(rm_history),
                        "email": self.user_email, "units": units}
    
    elif table_name == "Weight Loss":
      current_date = datetime.today().strftime("%d/%m/%Y")
      default_weight_history, default_cardio_history = {}, {}
      default_activities = ["Running", "Walking", "Cycling", "Swimming"]
      default_preferred_activity = "Running"
      
      default_cardio_history[current_date] = {}
      for activity in default_activities:
        default_cardio_history[current_date][activity] = []
    
      default_values = {"email": self.user_email, "weight_history": json.dumps(default_weight_history),
                      "preferred_activity": default_preferred_activity,
                      "cardio_history": json.dumps(default_cardio_history)} 

    elif table_name == "Workouts":
      workouts = {}
      current_workout_plan = ""
      default_values = {"email": self.user_email, "workouts": json.dumps(workouts), "current_workout_plan": current_workout_plan} 

    columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(default_values.keys()))
    values = tuple(value for value in default_values.values())
    
    try:
      self.pg_cursor.execute(sql.SQL("INSERT INTO "+self.table_names[table_name]+" ({columns}) VALUES %s").format(
                             columns=columns), (values,))
      self.pg_connection.commit()
      if not self.local_table_exists(table_name): self.create_local_table(table_name)
      self.sqlite_cursor.execute("INSERT INTO "+self.table_names[table_name]+" {columns} VALUES {values}".format(
                                 columns=tuple(default_values.keys()), values=tuple(default_values.values())))
      self.sqlite_connection.commit()
    except psycopg2.errors.UniqueViolation:
      self.pg_cursor.execute("ROLLBACK")
      self.pg_connection.commit()
      self.fetch_remote_data(table_name)

  def create_local_table(self, table_name):
    assert table_name in self.table_names.keys()
    create_table = None
    if table_name == "Nutrition":
       create_table = """
                 CREATE TABLE IF NOT EXISTS
                 %s (
                 email text,
                 calorie_goal text,
                 meal_plans text,
                 manage_meals text,
                 ID integer NOT NULL,
                 PRIMARY KEY(ID));
                 """ % self.table_names["Nutrition"]
    elif table_name == "Compound Exercises":
      create_table = """
                     CREATE TABLE IF NOT EXISTS
                     %s (
                     email text,
                     one_rep_maxes text,
                     lifts_for_reps text,
                     preferred_lifts text,
                     lift_history text,
                     units text,
                     rm_history text,
                     id integer NOT NULL,
                     PRIMARY KEY(id));
                     """ % self.table_names["Compound Exercises"]
    elif table_name == "Weight Loss":
      create_table = """
                     CREATE TABLE IF NOT EXISTS
                     %s (
                     email text,
                     weight_history text,
                     preferred_activity text,
                     cardio_history text,
                     ID integer NOT NULL,
                     PRIMARY KEY(ID));
                     """ % self.table_names["Weight Loss"]
    elif table_name == "Workouts":
      create_table = """
                     CREATE TABLE IF NOT EXISTS
                     'workouts' (
                     email text,
                     workouts text,
                     current_workout_plan text,
                     id integer NOT NULL,
                     PRIMARY KEY(id));
                     """ 
    self.sqlite_cursor.execute(create_table)
    self.sqlite_connection.commit() 

  def fetch_remote_data(self, table_name):
    assert table_name in self.table_names.keys()
    values = self.fetch_all_remote_columns(table_name)
    columns = "("+", ".join(self.table_columns[table_name])+")"
    values_string = "("+", ".join(["?"]*len(values))+")"
    insert = "INSERT INTO "+self.table_names[table_name]+" "+columns+" VALUES "+values_string
    if self.local_table_is_empty(table_name):
      self.sqlite_cursor.execute(insert, (*values,))
      self.sqlite_connection.commit()

  def fetch_all_remote_columns(self, table_name):
    assert table_name in self.table_names.keys()
    self.pg_cursor.execute(sql.SQL("SELECT * FROM {table} WHERE email=%s").format(
                           table=sql.Identifier(self.table_names[table_name])), (self.user_email,))
    user_info = self.pg_cursor.fetchone()[:-1]
    return user_info

  def fetch_remote_column_names(self, table_name):
    assert table_name in self.table_names.keys()
    remote_columns = """
                     SELECT column_name FROM information_schema.columns 
                     WHERE table_name = %s
                     """
    self.pg_cursor.execute(remote_columns, (self.table_names[table_name],))
    return tuple(value[0] for value in self.pg_cursor.fetchall() if not value[0] == 'id') 
  
  def local_table_exists(self, table_name):
    assert table_name in self.table_names.keys()
    self.sqlite_cursor.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name=?", (self.table_names[table_name],))
    return False if self.sqlite_cursor.fetchone()[0] == 0 else True

  def local_table_is_empty(self, table_name):
    assert table_name in self.table_names.keys()
    self.sqlite_cursor.execute("SELECT COUNT(*) FROM "+self.table_names[table_name]+" WHERE email=?", (self.user_email,))
    if self.sqlite_cursor.fetchone()[0] == 0: return True
    return False
  

  #################################
  # METHODS USED FOR LOGIN/SIGNUP #
  #################################

  def one_logged_in_user(self):
    self.sqlite_cursor.execute("SELECT COUNT(*) FROM "+self.table_names["Users"]+" WHERE logged_in='YES'")
    if self.sqlite_cursor.fetchone()[0] != 1: return False
    return True
  
  def create_user_table(self, email=None, password=None):
    assert (email == None and password == None) or (email != None and password != None)
    create_users_table = """
                         CREATE TABLE IF NOT EXISTS %s (
                         email text NOT NULL,
                         password text NOT NULL,
                         name text,
                         age text,
                         gender text,
                         units text,
                         weight text,
                         height text,
                         goal text,
                         goalparams text, 
                         goalweight text,
                         logged_in text,
                         ID integer NOT NULL,
                         PRIMARY KEY (ID));
                         """ % self.table_names["Users"]
     
    self.sqlite_cursor.execute(create_users_table)
    if email != None and password != None:
      self.sqlite_cursor.execute("INSERT INTO "+self.table_names["Users"]+" (email, password) VALUES (?, ?)", (email, password,))
      self.sqlite_cursor.execute("UPDATE "+self.table_names["Users"]+" SET logged_in='YES' WHERE email=?", (email,))
      self.user_email = email
    self.sqlite_connection.commit()

  def fetch_local_user_info(self):
    self.sqlite_cursor.execute("SELECT * FROM "+self.table_names["Users"]+" WHERE email=?", (self.user_email,))
    fetched_info = self.sqlite_cursor.fetchall()[0][2:-2]
    info = ["Name", "Age", "Gender", "Units", "Weight", "Height", "Goal", "Goal Params", "Weight Goal"]
    user_info_dict = {}
    for (fetched, category) in zip(fetched_info, info):
      if category != "Goal Params": user_info_dict[category] = fetched
      else: user_info_dict[category] = json.loads(fetched)
    return user_info_dict

  def login_user(self, email, password):
    self.pg_cursor.execute(sql.SQL("SELECT * FROM {table} WHERE email=%s").format(
                           table=sql.Identifier(self.table_names["Users"])), (email,))
    user_info = self.pg_cursor.fetchone()[:-1]

    if not hashlib.sha256(password.encode('UTF-8')).hexdigest() == user_info[1]:
      print("Invalid Password.")
      return
    
    self.user_email = email
    remote_column_names = self.fetch_remote_column_names("Users")
    
    if self.local_table_exists("Users"):
      current_user_email = self.fetch_logged_in_user_email()
      if email != current_user_email:
         self.sqlite_cursor.execute("UPDATE "+self.table_names["Users"]+" SET logged_in='NO' WHERE email=? AND logged_in='YES'",
                                    (current_user_email,))
         # check if email exists in table
         self.sqlite_cursor.execute("SELECT email FROM "+self.table_names["Users"]+" WHERE email=?", (email,))
         if self.sqlite_cursor.fetchone() == None:
           self.sqlite_cursor.execute("INSERT INTO "+self.table_names["Users"]+" {columns} VALUES {values}".format(
                                      columns=remote_column_names, values=user_info))
         self.sqlite_cursor.execute("UPDATE "+self.table_names["Users"]+" SET logged_in='YES' WHERE email=?", (email,))
    else:
      self.create_user_table() 
      self.sqlite_cursor.execute("INSERT INTO 'users' {columns} VALUES {values}".format(
                                 columns=remote_column_names, values=user_info))
      self.sqlite_cursor.execute("UPDATE "+self.table_names["Users"]+" SET logged_in='YES' WHERE email=?", (email,))
    self.sqlite_connection.commit()
    return True

  def logout_current_user(self):
    self.sqlite_cursor.execute("UPDATE "+self.table_names["Users"]+" SET logged_in='NO' WHERE email=? AND logged_in='YES'",
                              (self.user_email,))
    self.sqlite_connection.commit()

  def create_user(self, email, password):
    status = True
    try:
      password = hashlib.sha256(password.encode('utf-8')).hexdigest()
      self.pg_cursor.execute(sql.SQL("INSERT INTO {table} (email, password) VALUES (%s, %s)").format(
                             table=sql.Identifier(self.table_names["Users"])), (email, password,))
      self.pg_connection.commit()
    except psycopg2.errors.UniqueViolation: # user with given email already exists
      print("User already exists.")
      self.pg_cursor.execute("ROLLBACK")
      self.pg_connection.commit()
      status = False
    return status 

  def create_user_info_after_signup(self, user_info):
    email = "'{e}'".format(e=self.user_email)
    pg_query = sql.SQL("UPDATE {table} SET {data} WHERE email="+email).format(
               table=sql.Identifier(self.table_names["Users"]),
               data=sql.SQL(', ').join(sql.Composed([sql.Identifier(k), sql.SQL("="), sql.Placeholder(k)]) for k in user_info.keys()))
    
    self.pg_cursor.execute(pg_query, user_info)
    self.pg_connection.commit()
    
    sqlite_query = "UPDATE %s SET name=?, age=?, gender=?, units=?, weight=?, height=?, goal=?, goalparams=?, goalweight=? WHERE email='{e}'"
    sqlite_query = sqlite_query % (self.table_names["Users"])
    self.sqlite_cursor.execute(sqlite_query.format(e=self.user_email), tuple(user_info.values())) 
    self.sqlite_connection.commit()


  ##################################
  # METHODS USED IN OTHER CONTEXTS #
  ################################## 

  def rotate_meals(self, fetched_meal_plans): 
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
   self.update_table_column("Nutrition", "meal_plans", new_meal_plans)

  def update_meal(self, meal_name, food_info, day, this_week=False, next_week=False):
    assert this_week != False or next_week != False
    assert not (this_week == True and next_week == True)
    
    time = "Present" if this_week == True else "Future"
    fetched_meal_plans = json.loads(self.fetch_local_column("Nutrition", "meal_plans"))

    fetched_meal_plans[time][day][meal_name].append(food_info)

    new_meal_plans = json.dumps(fetched_meal_plans)
    
    self.update_table_column("Nutrition", "meal_plans", new_meal_plans)

  def modify_meal(self, action, meal_to_modify, day=None, modify_to=None, this_week=False, next_week=False):
    assert action in ("Add", "Delete", "Rename")
    assert this_week != False or next_week != False
    assert day != None
    if action == "Rename": assert modify_to != None
    elif action == "Add": assert modify_to == None
     
    fetched_meal_plans = json.loads(self.fetch_local_column("Nutrition", "meal_plans"))
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
    
    self.update_table_column("Nutrition", "meal_plans", new_meal_plans) 
