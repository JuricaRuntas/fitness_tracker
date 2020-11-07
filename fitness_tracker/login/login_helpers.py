import os
import hashlib
import psycopg2
import sqlite3
from psycopg2 import sql
from PyQt5.QtCore import QFileInfo

# path for sqlite3 user info database
path = os.path.normpath(QFileInfo(__file__).absolutePath())
db_path = path.split(os.path.sep)[:-2]
db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])

db_info = {"host": "fitnesstracker.cc7s2r4sjjv6.eu-west-3.rds.amazonaws.com", "port": 5432,
           "database": "postgres", "user": "admin", "password": "admin"}

def check_password(email, password):
  status = True
  query = "SELECT * FROM users WHERE email=%s"
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute(query, (email,))
      database_password = cursor.fetchone()[1]
      if not hashlib.sha256(password.encode('UTF-8')).hexdigest() == database_password: status = False
  return status

def get_table_name(email, password):
  table_name = None
  if check_password(email, password):
    query = "SELECT * FROM users WHERE email=%s"
    with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
      with conn.cursor() as cursor:
        cursor.execute(query, (email,))
        table_name = cursor.fetchone()[2]
  return table_name

def get_user_info(email, password):
  table_name = get_table_name(email, password)
  columns = None
  user_info = None

  with sqlite3.connect(db_path) as conn:
    table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
    sqlite_cursor = conn.cursor()
    sqlite_cursor.execute(table_exists.format(table=table_name))
    if sqlite_cursor.fetchone() == None: # table doesn't exist
      with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                          user=db_info["user"], password=db_info["password"]) as conn:
        with conn.cursor() as cursor:
          # this can be changed to fetch something else later on
          cursor.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name)))
          user_info = cursor.fetchone()[1:]
          query = """
                  SELECT column_name FROM information_schema.columns 
                  WHERE table_name = %s;
                  """
          cursor.execute(query, (table_name,))
          # fetch all column names
          # change this in the future
          columns = tuple(value[0] for value in cursor.fetchall()[1:])
      create_table = """
                     CREATE TABLE "{table}" (
                     ID integer NOT NULL,
                     name text NOT NULL,
                     gender text NOT NULL,
                     units text NOT NULL,
                     weight real NOT NULL,
                     PRIMARY KEY (ID));
                     """
      sqlite_cursor.execute(create_table.format(table=table_name))
      insert_values = "INSERT INTO '{table}' {columns} VALUES {values}"
      sqlite_cursor.execute(insert_values.format(table=table_name, columns=columns, values=user_info))
