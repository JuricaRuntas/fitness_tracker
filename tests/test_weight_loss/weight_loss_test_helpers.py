import sqlite3
import json
import hashlib
import psycopg2
from fitness_tracker.config import db_info
from fitness_tracker.signup.signup_helpers import create_user_table, create_user_info_after_signup, create_user

test_user = {"email": "test@gmail.com",
             "password": hashlib.sha256("testpassword123".encode('UTF-8')).hexdigest(),
             "name": "Test", "age": "18", "gender": "male", "units": "metric",
             "weight": "100", "height": "190", "goal": "Weight gain",
             "goalparams": json.dumps(["Moderately active", 0.25]), "goalweight": "120"}

def create_test_user(sqlite_connection, pg_connection):
  create_user(test_user["email"], "testpassword123", pg_connection)
  create_user_table(test_user["email"], "testpassword123", sqlite_connection)
  create_user_info_after_signup(test_user, test_user["email"], sqlite_connection, pg_connection)

def delete_test_user(email):
  with psycopg2.connect(host=db_info["host"], port=db_info["port"], database=db_info["database"],
                        user=db_info["user"], password=db_info["password"]) as conn:
    with conn.cursor() as cursor:
      cursor.execute("DELETE FROM users WHERE email=%s", (email,))
      cursor.execute("DELETE FROM weight_loss WHERE email=%s", (email,))

def fetch_weight_loss_columns(cursor):
  cursor.execute("SELECT * FROM weight_loss")
  return tuple(description[0] for description in cursor.description if not description[0] == "ID")

def fetch_weight_loss_data(pg_cursor):
  pg_cursor.execute("SELECT * FROM weight_loss WHERE email=%s", (test_user["email"],))
  return pg_cursor.fetchall()

def fetch_weight_loss_data(pg_cursor):
  pg_cursor.execute("SELECT * FROM weight_loss WHERE email=%s", (test_user["email"],))
  return pg_cursor.fetchall()

def fetch_local_weight_loss_data(sqlite_cursor):
  sqlite_cursor.execute("SELECT * FROM 'weight_loss' WHERE email=?", (test_user["email"],))
  return sqlite_cursor.fetchall()
