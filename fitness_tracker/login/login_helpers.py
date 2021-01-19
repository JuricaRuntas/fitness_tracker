import hashlib
import psycopg2
import sqlite3
from fitness_tracker.user_profile.profile_db import logged_in_user_email
from fitness_tracker.config import db_info, db_path

def check_password(email, password):
  status = True
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
      database_password = cursor.fetchone()[1]
      if not hashlib.sha256(password.encode('UTF-8')).hexdigest() == database_password: status = False
  return status

def logout_current_user():
  current_user = logged_in_user_email()
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("UPDATE 'users' SET logged_in='NO' WHERE email=? AND logged_in='YES'", (current_user,))

def fetch_user_info(email, password, db_path=db_path):
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
  
  with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='users';")
    insert_values = "INSERT INTO 'users' {columns} VALUES {values}"
    if cursor.fetchone()[0] == 0: # table doesn't exist
      create_table = """
                     CREATE TABLE 'users' (
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
      cursor.execute(create_table)
      cursor.execute(insert_values.format(columns=columns, values=user_info))
      cursor.execute("UPDATE 'users' SET logged_in='YES' WHERE email=?", (email,))
    else:
      current_user_email = logged_in_user_email()
      if email != current_user_email:
        cursor.execute("UPDATE 'users' SET logged_in='NO' WHERE email=? AND logged_in='YES'", (current_user_email,))
        cursor.execute("SELECT email FROM 'users' WHERE email=?", (email,))
        if cursor.fetchone() == None:
          cursor.execute(insert_values.format(columns=columns, values=user_info)) 
        cursor.execute("UPDATE 'users' SET logged_in='YES' WHERE email=?", (email,))
