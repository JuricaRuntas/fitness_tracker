import os
import sqlite3
import psycopg2
from psycopg2 import sql
from PyQt5.QtCore import QFileInfo

path = os.path.normpath(QFileInfo(__file__).absolutePath())
db_path = path.split(os.path.sep)[:-3]
db_path_user_info = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "big_lifts.db"])

#db_info = {"host": "localhost", "port": 5432,
#           "database": "postgres", "user": "admin", "password": "admin"}

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

class BigLifts:
  def table_is_empty(self):
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT COUNT (*) FROM big_lifts")
      if cursor.fetchone()[0] == 0: return True
      else: return False

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
    return self.parse_lifts_string(one_rep_maxes)

  def fetch_lifts_for_reps(self):
    lifts_for_reps = None
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT lifts_for_reps FROM big_lifts")
      lifts_for_reps = cursor.fetchone()[0]
    return self.parse_lifts_string(lifts_for_reps)
  
  def insert_default_values(self, exercises):
    email = self.fetch_user_email()
    table_name = self.fetch_user_info_table_name()
    one_RM_dict = self.stringify_lifts_dict({exercise:"0" for exercise in exercises})
    lifts_for_reps = self.stringify_lifts_dict({exercise:"0" for exercise in exercises})
    preferred_lifts = ",".join(exercises)
    
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

  def create_update_query(self, table_name, email, columns_values_dict, sqlite=False):
    update_query = "UPDATE {table} SET"
    # create list with [column_name, value] pairs
    pairs = [[pair[0], pair[1]] for pair in zip(columns_values_dict.keys(), columns_values_dict.values())]
    for pair in pairs:
      pair[1] = "'%s'" % pair[1] # add ticks to value
      joined_pair = "=".join([pair[0], pair[1]]) # create column='value' string
      # if its first pair, join it to update_query with blank space
      if pairs.index(pair) == 0: update_query = " ".join([update_query, joined_pair])
      # if its last pair, add WHERE email={email} to the end of update_query
      elif pairs.index(pair) == len(pairs)-1:
        update_query = ", ".join([update_query, joined_pair])
        update_query = " ".join([update_query, "WHERE email={email}"])
      else: update_query = ", ".join([update_query, joined_pair])
    if sqlite: # make adjustments for sqlite3
      update_query = update_query.replace("{table}", "'%s'").replace("email={email}", "email='%s'")
      return update_query % (table_name, email)
    else: # make sql query for psycopg2
      return sql.SQL(update_query).format(table=sql.Identifier(table_name), email=sql.Identifier(email))
  
  def stringify_lifts_dict(self, lifts_dict):
    # make tuple with "lift_name->weight" pairs
    parse_dict = tuple(("->".join([lift[0], lift[1]])) for lift in zip(lifts_dict.keys(), lifts_dict.values()))
    lifts_string = ",".join(parse_dict)
    return lifts_string

  def parse_lifts_string(self, lifts_string):
    parsed_lifts_string = [lift_pair.split("->") for lift_pair in lifts_string.split(",")]
    lifts_dict = {lift_pair[0]:lift_pair[1] for lift_pair in parsed_lifts_string}
    return lifts_dict

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
