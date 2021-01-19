import re
import sqlite3
import string
import hashlib
import psycopg2
from psycopg2 import sql
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_path, db_info

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

def create_user(user_email, user_password):
  status = True
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    try:
      with conn.cursor() as cursor:
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (user_email, user_password,))
    except psycopg2.errors.UniqueViolation: # user with given email already exists
      status = False
  return status

def create_user_info_after_signup(user_info, email, db_path=db_path):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      update_query = create_update_query("users", email, user_info)
      cursor.execute(update_query)
    
    with sqlite3.connect(db_path) as conn:
      cursor = conn.cursor()
      update_query = create_update_query("users",  email, user_info, sqlite=True)
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

def create_user_table(email, password, db_path=db_path):
  status = True
  password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
  # set user table columns here
  create_table = """
                 CREATE TABLE IF NOT EXISTS 'users' (
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
                 """ 
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(create_table)
    cursor.execute("INSERT INTO 'users' (email, password) VALUES (?, ?)", (email, password,))
    cursor.execute("UPDATE 'users' SET logged_in='YES' WHERE email=?", (email,))
