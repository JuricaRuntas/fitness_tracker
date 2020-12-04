import os
import re
import sqlite3
import string
import hashlib
import psycopg2
from psycopg2 import sql

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.sep.join([*path.split(os.path.sep)[:-2], "db"])
user_info_db = os.path.sep.join([db_path, "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432, 
           "database": "postgres", "user": "admin", "password": "admin"}

class Signup:
  def check_valid_email(self, email):
    # basic validation, checks for example@gmail.com and similar format
    # for real validation, email confirmation is needed
    email_regex = re.compile(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,6}$")
    return not re.match(email_regex, email) == None
   
  def check_valid_password(self, password):
    valid = True
    valid_characters = set(string.ascii_letters + string.digits + '@#$%^&+=')
    if (len(password) < 8):
      valid = False
      print("Password is too short.")
    elif any(char not in valid_characters for char in password):
      valid = False
      print("Password contains invalid characters.")
    return valid

  def fetch_user_email(self):
    email = None
    with sqlite3.connect(user_info_db) as conn:
      cursor = conn.cursor()
      table_name = self.fetch_table_name()
      cursor.execute("SELECT email FROM '{table}'".format(table=table_name))
      try:
        email = cursor.fetchone()[0]
      except TypeError:
        pass
    return email

  def fetch_table_name(self):
    table_name = None
    with sqlite3.connect(user_info_db) as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
      try:
        # returns table name if exists otherwise returns None
        table_name = cursor.fetchone()[0]
      except TypeError: # catch TypeError caused by subscripting 'NoneType' object
        pass
    return table_name

  def create_user(self, user_email, user_password):
    self.email = user_email
    status = True
    #table_name = "".join([user_email, "_table"])6
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      try:
        with conn.cursor() as cursor:
          user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
          query = "INSERT INTO users (email, password) VALUES (%s, %s)"
          cursor.execute(query, (user_email, user_password,))
      except psycopg2.errors.UniqueViolation:
        status = False
        print("User with '%s' email address already exists.") % user_email
    return status

  def create_user_info_after_signup(self, user_info, email):
    table_name = self.fetch_table_name()
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        update_query = self.create_update_query("users", email, user_info)
        cursor.execute(update_query)
      
      with sqlite3.connect(user_info_db) as conn:
        cursor = conn.cursor()
        update_query = self.create_update_query(table_name, email, user_info, sqlite=True)
        cursor.execute(update_query)

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
        update_query = " ".join([update_query, "WHERE email='%s'"])
      else: update_query = ", ".join([update_query, joined_pair])
    if sqlite: # make adjustments for sqlite3
      update_query = update_query.replace("{table}", "'%s'")#.replace("email=%s", "email='%s'")
      return update_query % (table_name, email)
    else: # make sql query for psycopg2
      update_query = update_query.format(table=table_name)
      return update_query % email

  def create_user_table(self, email, password):
    status = True
    table_name = "".join([email, "_table"])
    # set user table columns here
    create_table = """
                   CREATE TABLE '%s' (
                   email text NOT NULL,
                   password text NOT NULL,
                   name text,
                   gender text,
                   units text,
                   weight real,
                   id integer NOT NULL,
                   PRIMARY KEY (ID));
                   """ % table_name
                   
    with sqlite3.connect(user_info_db) as conn:
      cursor = conn.cursor()
      cursor.execute(create_table)
      insert_email = "INSERT INTO '%s'(email, password) VALUES ('%s', '%s')" % (table_name, email, password)
      cursor.execute(insert_email)
