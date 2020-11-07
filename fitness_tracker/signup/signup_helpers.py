import os
import re
import sqlite3
import string
import hashlib
import psycopg2
from psycopg2 import sql
from PyQt5.QtCore import QFileInfo

# path for sqlite3 user info database
path = os.path.normpath(QFileInfo(__file__).absolutePath())
db_path = path.split(os.path.sep)[:-2]
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432, 
           "database": "postgres", "user": "admin", "password": "admin"}

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

def get_table_name():
  table_name = None
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    try:
      # returns table name if exists otherwise returns None
      table_name = cursor.fetchone()[0]
    except TypeError: # catch TypeError caused by subscripting 'NoneType' object
      pass
  return table_name

def create_user(user_email, user_password):
  status = True
  table_name = "".join([user_email, "_table"])
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    try:
      with conn.cursor() as cursor:
        user_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
        query = "INSERT INTO users VALUES (%s, %s, %s)"
        cursor.execute(query, (user_email, user_password, table_name,))
    except psycopg2.errors.UniqueViolation:
      status = False
      print("User with '%s' email address already exists.") % user_email
  return status

def create_user_table(email):
  status = True
  table_name = "".join([email, "_table"])
  # set user table columns here
  create_table = """
                 CREATE TABLE {table} (
                 ID bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 99999999 ),
                 name text NOT NULL,
                 gender text NOT NULL,
                 units text NOT NULL,
                 weight real NOT NULL,
                 PRIMARY KEY (ID));
                 """
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(sql.SQL(create_table).format(table=sql.Identifier(table_name)))
  
  diff_id = "bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 99999999 )"
  create_table = create_table.replace(diff_id, "integer NOT NULL").replace("{table}", '"%s"') % table_name
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(create_table) 

def create_user_info_after_signup(user_info, user_table_name):
  query = "INSERT INTO {table} ({columns}) VALUES %s"
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn: 
    with conn.cursor() as cursor:  
      columns = sql.SQL(", ").join(sql.Identifier(column) for column in tuple(user_info.keys()))
      values = tuple(value for value in user_info.values())
      cursor.execute(sql.SQL(query).format(table=sql.Identifier(user_table_name), columns=columns), (values,))
  
  sqlite_query = """INSERT INTO "{}" {columns} VALUES {values}"""
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(sqlite_query.format(user_table_name, columns=tuple(user_info.keys()), values=tuple(user_info.values())))