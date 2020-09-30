import sqlite3

class ExercisesDB:
  def fetch_info(self, exercise, db_path, table_name):
    try:
      connection = sqlite3.connect(db_path)
      cursor = connection.cursor()
      
      select_info = """SELECT * FROM '%s' WHERE exercise_name='%s'""" % (table_name, exercise)
      cursor.execute(select_info)
      info = cursor.fetchone()
      cursor.close()
    except sqlite3.Error as error:
      print("Error while fetching info from '%s' table: %s" % (table_name, error))
    finally:
      if connection: connection.close()
      return info 

  def fetch_name(self):
    return self.info[1]

  def fetch_description(self):
    return self.info[2]
  
  def fetch_muscles_targeted(self):
    return self.info[3].split(" ")

  def fetch_instructions(self):
    return self.info[4]

  def fetch_tips(self):
    return self.info[5]

class ChestExercisesDB(ExercisesDB):
  def __init__(self, path):
    self.db_path = path
    self.table_name = "ChestExercises"
    self.info = None
    self.create_database()
  
  def create_database(self):
    try:
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()

      table_exists = """SELECT count(name) FROM sqlite_master WHERE type="table" AND name="ChestExercises"
                     """
      cursor.execute(table_exists)
      if cursor.fetchone()[0] == 0:
        create_table = """CREATE TABLE ChestExercises(
                          id INTEGER PRIMARY KEY,
                          exercise_name TEXT NOT NULL,
                          description TEXT NOT NULL,
                          muscles_targeted TEXT NOT NULL,
                          instructions TEXT NOT NULL,
                          tips TEXT NOT NULL);
                       """
        insert_bench_press = """INSERT INTO ChestExercises 
                                (id, exercise_name, description, muscles_targeted, instructions, tips) VALUES
                                (1, "Flat Barbell Bench Press",
                                 "Flat Barbell Bench Press is a great exercises for improving your strength and ...",
                                 "Chest Triceps",
                                 "1. Before performing big lifts like bench press, it is good idea to warmup.",
                                 "Slightly arching your back when performing lift can boost your strength.")"""
        cursor.execute(create_table)
        cursor.execute(insert_bench_press)
      connection.commit()
      cursor.close()
    except sqlite3.Error as error:
      print("Error while creating ChestExercises table", error)
    finally:
      if connection: connection.close()
  
  def fetch_info(self, exercise):
    self.info = ExercisesDB.fetch_info(self, exercise, self.db_path, self.table_name)
