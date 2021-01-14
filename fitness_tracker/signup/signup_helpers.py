import os
import re
import sqlite3
import string
import hashlib
import psycopg2
from psycopg2 import sql
from fitness_tracker.config import db_info
from fitness_tracker.user_profile.profile_db import fetch_table_name

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.sep.join([*path.split(os.path.sep)[:-2], "db"])
profile_db = os.path.sep.join([db_path, "profile.db"])

def check_valid_email(email):
  # basic validation, checks for example@gmail.com and similar format
  # for real validation, email confirmation is needed
  email_regex = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,6}$")
  return not re.match(email_regex, email) == None
 
def check_valid_password(password):
  valid = True
  valid_characters = set(string.ascii_letters + string.digits + '@#$%^&+=')
  if (len(password) < 8):
    valid = False
    print("Password is too short.")
  elif any(char not in valid_characters for char in password):
    valid = False
    print("Password contains invalid characters.")
  return valid

#def fetch_table_name():
#  table_name = None
#  with sqlite3.connect(profile_db) as conn:
#    cursor = conn.cursor()
#    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
#    try:
#      # returns table name if exists otherwise returns None
#      table_name = cursor.fetchone()[0]
#    except TypeError: # catch TypeError caused by subscripting 'NoneType' object
#      pass
#  return table_name

def create_user(user_email, user_password):
  status = True
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    try:
      with conn.cursor() as cursor:
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (user_email, user_password,))
    except psycopg2.errors.UniqueViolation: # user with given email already exists
      status = False
  return status

def create_user_info_after_signup(user_info, email, user_path=profile_db):
  table_name = fetch_table_name(user_path)
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      update_query = create_update_query("users", email, user_info)
      cursor.execute(update_query)
    
    with sqlite3.connect(user_path) as conn:
      cursor = conn.cursor()
      update_query = create_update_query(table_name, email, user_info, sqlite=True)
      cursor.execute(update_query)

def create_update_query(table_name, email, columns_values_dict, sqlite=False):
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
      update_query = " ".join([update_query, "WHERE email='%s'"])
    else: update_query = ", ".join([update_query, joined_pair])
  if sqlite: # make adjustments for sqlite3
    update_query = update_query.replace("{table}", "'%s'")
    return update_query % (table_name, email)
  else: # make sql query for psycopg2
    update_query = update_query.format(table=table_name)
    return update_query % email

def create_user_table(email, password, user_path=profile_db):
  status = True
  table_name = "".join([email, "_table"])
  password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
  # set user table columns here
  create_table = """
                 CREATE TABLE '%s' (
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
                 ID integer NOT NULL,
                 PRIMARY KEY (ID));
                 """ % table_name
                 
  with sqlite3.connect(user_path) as conn:
    cursor = conn.cursor()
    cursor.execute(create_table)
    insert_email = "INSERT INTO '%s'(email, password) VALUES ('%s', '%s')" % (table_name, email, password)
    cursor.execute(insert_email)
