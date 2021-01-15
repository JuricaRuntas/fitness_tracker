import hashlib
import psycopg2
import sqlite3
from psycopg2 import sql
from fitness_tracker.config import db_info, get_db_paths

db_paths = get_db_paths("profile.db")

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

def fetch_user_info(email, password, user_path=db_paths["profile.db"]):
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
  
  with sqlite3.connect(user_path) as conn:
    table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"
    cursor = conn.cursor()
    cursor.execute(table_exists.format(table=table_name))
    if cursor.fetchone() == None: # table doesn't exist
      create_table = """
                     CREATE TABLE "{table}" (
                     email text NOT NULL,
                     password text NOT NULL,
                     name text NOT NULL,
                     age text NOT NULL,
                     gender text NOT NULL,
                     units text NOT NULL,
                     weight text NOT NULL,
                     height text NOT NULL,
                     goal text NOT NULL,
                     goalparams text NOT NULL, 
                     goalweight text NOT NULL,
                     ID integer NOT NULL,
                     PRIMARY KEY (ID));
                     """
      cursor.execute(create_table.format(table=table_name))
      insert_values = "INSERT INTO '{table}' {columns} VALUES {values}"
      cursor.execute(insert_values.format(table=table_name, columns=columns, values=user_info))
