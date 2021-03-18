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

def logout_current_user(sqlite_connection):
  sqlite_cursor = sqlite_connection.cursor()
  current_user = logged_in_user_email(sqlite_cursor)
  sqlite_cursor.execute("UPDATE 'users' SET logged_in='NO' WHERE email=? AND logged_in='YES'", (current_user,))
  sqlite_connection.commit()

def fetch_user_info(email, password, sqlite_connection, pg_cursor):
  sqlite_cursor = sqlite_connection.cursor()

  # this can be changed to fetch something else later on
  pg_cursor.execute(("SELECT * FROM users WHERE email='{email}'").format(email=email))
  user_info = pg_cursor.fetchone()[:-1]
  # fetch all column names
  # change this in the future
  query = """
          SELECT column_name FROM information_schema.columns 
          WHERE table_name = 'users';
          """
  pg_cursor.execute(query)
  columns = tuple(value[0] for value in pg_cursor.fetchall() if not value[0] == 'id')
  
  sqlite_cursor.execute("SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='users';")
  if sqlite_cursor.fetchone()[0] == 0: # table doesn't exist
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
    sqlite_cursor.execute(create_table)
    sqlite_cursor.execute("INSERT INTO 'users' {columns} VALUES {values}".format(columns=columns, values=user_info))
    sqlite_cursor.execute("UPDATE 'users' SET logged_in='YES' WHERE email=?", (email,))
  else:
    current_user_email = logged_in_user_email(sqlite_cursor)
    if email != current_user_email:
      sqlite_cursor.execute("UPDATE 'users' SET logged_in='NO' WHERE email=? AND logged_in='YES'", (current_user_email,))
      sqlite_cursor.execute("SELECT email FROM 'users' WHERE email=?", (email,))
      if sqlite_cursor.fetchone() == None:
        sqlite_cursor.execute("INSERT INTO 'users' {columns} VALUES {values}".format(columns=columns, values=user_info)) 
      sqlite_cursor.execute("UPDATE 'users' SET logged_in='YES' WHERE email=?", (email,))
  sqlite_connection.commit()
