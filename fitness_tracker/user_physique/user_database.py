import sqlite3

class UserDatabase:
  def __init__(self):
    self.create_database()

  def create_database(self):
    try:
      connection = sqlite3.connect("../db/user_data.db")
      cursor = connection.cursor()

      table_exists = """SELECT count(name) FROM sqlite_master
                        WHERE type="table" AND name="UserData"
                     """
      cursor.execute(table_exists)
      if cursor.fetchone()[0] == 0:
        create_table = """CREATE TABLE UserData(
                          id INTEGER PRIMARY KEY,
                          units TEXT NOT NULL);
                       """
        cursor.execute(create_table)
        insert_units = """INSERT INTO UserData (id, units) VALUES (1, "metric")"""
        cursor.execute(insert_units)
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Error while creating UserData table", error)
    finally:
      if connection: connection.close()

  def fetch_units(self):
    try:
      connection = sqlite3.connect("../db/user_data.db")
      cursor = connection.cursor()

      select_units = """SELECT * FROM UserData WHERE id=1"""
      cursor.execute(select_units)
      units = cursor.fetchone()
      cursor.close()
    except sqlite3.Error as error:
      print("Error while fetching units from UserData table", error)
    finally:
      if connection: connection.close()
      return units[1]

  def update_units(self):
    try:
      connection = sqlite3.connect("../db/user_data.db")
      cursor = connection.cursor()

      set_units_imperial = "UPDATE UserData SET units='imperial'"
      set_units_metric = "UPDATE UserData SET units='metric'"
      fetch_current_units = "SELECT * FROM UserData WHERE id=1"

      cursor.execute(fetch_current_units)
      update_units = set_units_imperial if cursor.fetchone()[1]=="metric" else set_units_metric
      cursor.execute(update_units)
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Error while updating UserData table units", error)
    finally:
      if connection: connection.close()
