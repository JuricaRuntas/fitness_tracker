import os
import hashlib
import psycopg2
import sqlite3
from psycopg2 import sql

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.sep.join([*path.split(os.path.sep)[:-2], "db"])
user_info_db = os.path.sep.join([db_path, "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

class Login():
  def check_password(self, email, password):
    status = True
    query = "SELECT * FROM users WHERE email=%s"
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (email,))
        database_password = cursor.fetchone()[1]
        if not hashlib.sha256(password.encode('UTF-8')).hexdigest() == database_password: status = False
    return status

  def fetch_user_info(self, email, password):
    table_name = "".join([email, "_table"])
    columns = None
    user_info = None
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
        with conn.cursor() as cursor:
          # this can be changed to fetch something else later on
          cursor.execute(("SELECT * FROM users WHERE email='{email}'").format(email=email))
          user_info = cursor.fetchone()[:-1]
          # fetch all column names
          # change this in the future
          query = """
                  SELECT column_name FROM information_schema.columns 
                  WHERE table_name = 'users';
                  """
          cursor.execute(query)
          columns = tuple(value[0] for value in cursor.fetchall() if not value[0] == 'id')
    
    with sqlite3.connect(user_info_db) as conn:
      table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
      cursor = conn.cursor()
      cursor.execute(table_exists.format(table=table_name))
      if cursor.fetchone() == None: # table doesn't exist
        create_table = """
                       CREATE TABLE "{table}" (
                       email text NOT NULL,
                       password text NOT NULL,
                       name text NOT NULL,
                       gender text NOT NULL,
                       units text NOT NULL,
                       weight real NOT NULL,
                       ID integer NOT NULL,
                       PRIMARY KEY (ID));
                       """
        cursor.execute(create_table.format(table=table_name))
        insert_values = "INSERT INTO '{table}' {columns} VALUES {values}"
        cursor.execute(insert_values.format(table=table_name, columns=columns, values=user_info))
