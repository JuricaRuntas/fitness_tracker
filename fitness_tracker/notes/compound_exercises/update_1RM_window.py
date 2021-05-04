import json
from datetime import datetime
import os
from datetime import datetime
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, Qt
from fitness_tracker.database_wrapper import DatabaseWrapper

class Update1RMWindow(QWidget):
  change_1RM_lifts_signal = pyqtSignal(bool)
  history_signal = pyqtSignal(bool)
  update_graph_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Compound Exercises"
    self.setStyleSheet("""
    QWidget{
      background-color: #232120;
      font-weight: bold;
      color:#c7c7c7;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: center;
      padding-left: 5%;
      font-family: Montserrat;
    }
    QPushButton:hover:!pressed{
      border: 2px solid;
      border-color: #747474;
    }
    QPushButton:pressed{
      border: 2px solid;
      background-color: #323232;
    }
    """)
    self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
    self.setWindowModality(Qt.ApplicationModal)
    self.current_year = str(datetime.now().year)
    self.units = "kg" if self.db_wrapper.fetch_local_column("Users", "units") == "metric" else "lb"
    self.preferred_lifts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "preferred_lifts"))
    self.setWindowTitle("Update One Rep Max Lifts")
    self.setLayout(self.create_panel())
    self.set_line_edit_values()

  def create_panel(self):
    form_layout = QFormLayout()

    exercise_label = QLabel("Exercise")
    weight_label = QLabel("Weight")
    
    horizontal_press_label = QLabel(self.preferred_lifts["Horizontal Press"])
    self.horizontal_press_edit = QLineEdit()
    self.horizontal_press_edit.setValidator(QIntValidator())

    units_label = QLabel(self.units)
    hbox = QHBoxLayout()
    hbox.addWidget(self.horizontal_press_edit)
    hbox.addWidget(units_label)

    floor_pull_label = QLabel(self.preferred_lifts["Floor Pull"])
    self.floor_pull_edit = QLineEdit()
    self.floor_pull_edit.setValidator(QIntValidator())
    
    units_label1 = QLabel(self.units)
    hbox1 = QHBoxLayout()
    hbox1.addWidget(self.floor_pull_edit)
    hbox1.addWidget(units_label1)

    squat_label = QLabel(self.preferred_lifts["Squat"])
    self.squat_edit = QLineEdit()
    self.squat_edit.setValidator(QIntValidator())
    
    units_label2 = QLabel(self.units)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(self.squat_edit)
    hbox2.addWidget(units_label2)

    vertical_press_label = QLabel(self.preferred_lifts["Vertical Press"])
    self.vertical_press_edit = QLineEdit()
    self.vertical_press_edit.setValidator(QIntValidator())
    
    units_label3 = QLabel(self.units)
    hbox3 = QHBoxLayout()
    hbox3.addWidget(self.vertical_press_edit)
    hbox3.addWidget(units_label3)
    
    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_1RM_lifts())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_update_1RM())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)
    
    form_layout.addRow(exercise_label, weight_label)
    form_layout.addRow(horizontal_press_label, hbox)
    form_layout.addRow(floor_pull_label, hbox1)
    form_layout.addRow(squat_label, hbox2)
    form_layout.addRow(vertical_press_label, hbox3)
    
    main_layout = QVBoxLayout()
    main_layout.addLayout(form_layout)
    main_layout.addLayout(buttons_layout)
    
    return main_layout
  
  def save_1RM_lifts(self):
    try:
      fetched_rep_maxes = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes"))
      exercises = list(fetched_rep_maxes.keys())
      horizontal_press_max = str(float(self.horizontal_press_edit.text()))
      floor_pull_max = str(float(self.floor_pull_edit.text()))
      squat_max = str(float(self.squat_edit.text()))
      vertical_press_max = str(float(self.vertical_press_edit.text()))
      new_maxes = {exercises[0]:horizontal_press_max, exercises[1]:floor_pull_max,
                   exercises[2]:squat_max, exercises[3]:vertical_press_max}
      
      diff = self.lift_difference(new_maxes, fetched_rep_maxes, one_RM=True)
      
      self.db_wrapper.update_table_column(self.table_name, "lift_history", diff) 
      self.history_signal.emit(True)
      
      self.db_wrapper.update_table_column(self.table_name, "one_rep_maxes", new_maxes) 
      self.update_one_rep_maxes_history(diff, self.current_year)
      
      self.update_graph_signal.emit(True)
      self.change_1RM_lifts_signal.emit(True)
      
      self.set_line_edit_values()
      self.close() 
    except ValueError: # user submitted text/empty string
      pass
  
  def close_update_1RM(self):
    self.close()
    self.set_line_edit_values()

  def set_line_edit_values(self):
    one_rep_maxes = list(json.loads(self.db_wrapper.fetch_local_column(self.table_name, "one_rep_maxes")).values())
    self.horizontal_press_edit.setText(one_rep_maxes[0])
    self.floor_pull_edit.setText(one_rep_maxes[1])
    self.squat_edit.setText(one_rep_maxes[2])
    self.vertical_press_edit.setText(one_rep_maxes[3])

  def sort_exercises(self, exercise):
    if exercise in ["Bench Press", "Incline Bench Press"]: return 4
    elif exercise in ["Deadlift", "Sumo Deadlift"]: return 3
    elif exercise in ["Back Squat", "Front Squat"]: return 2
    elif exercise in ["Overhead Press", "Push Press"]: return 1 

  # returns sorted dictionary containing updated lifts
  def lift_difference(self, new_lifts, old_lifts, one_RM=False, lifts_reps=False):
    difference = None
    if one_RM:
      db_lifts = set(": ".join([exercise, weight]) for exercise, weight in old_lifts.items())
      new_lifts = set(": ".join([exercise, weight]) for exercise, weight in new_lifts.items() if not weight == '0.0')
      diff = list(new_lifts.difference(db_lifts)) # local lifts that are not in db
      difference = {exercise.split(": ")[0]:exercise.split(": ")[1] for exercise in diff}
    elif lifts_reps:
      db_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in old_lifts.items())
      new_lifts = set(":".join([exercise, "x".join(values)]) for exercise, values in new_lifts.items() if not values[1] == '0.0')
      diff = list(new_lifts.difference(db_lifts))
      difference = {exercise.split(":")[0]:exercise.split(":")[1].split("x") for exercise in diff}
    return {key: value for key, value in sorted(difference.items(), key=lambda exercise: self.sort_exercises(exercise[0]))}

  def update_one_rep_maxes_history(self, diff, year):
    rm_history = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "rm_history"))
    default_exercises = {"Horizontal Press": "Bench Press", "Floor Pull": "Deadlift",
                         "Squat": "Back Squat", "Vertical Press": "Overhead Press"}
    secondary_exercises = {"Horizontal Press": "Incline Bench Press", "Floor Pull": "Sumo Deadlift",
                           "Squat": "Front Squat", "Vertical Press": "Push Press"} 
    exercises = {}

    for default in default_exercises:
      if not default in exercises: exercises[default] = []
      exercises[default].append(default_exercises[default])

    for secondary in secondary_exercises:
      exercises[secondary].append(secondary_exercises[secondary])

    now = datetime.now()
    if year not in rm_history:
      rm_history[year] = {}
      for month in self.db_wrapper.months:
        exercises_dict = {}
        for lift_type in default_exercises:
          exercises_dict[lift_type] = {default_exercises[lift_type]:[]}
        for lift_type in secondary_exercises:
          exercises_dict[lift_type][secondary_exercises[lift_type]] = []
        rm_history[year][month] = exercises_dict 
    
    for i, (lift, weight) in enumerate(diff.items()):
      lift_type = None
      for exercise_type in exercises:
        if lift in exercises[exercise_type]: lift_type = exercise_type
      entry = rm_history[year][self.db_wrapper.months[now.month-1]][lift_type]
      if lift not in entry: entry[lift] = []
      entry[lift].append(weight) 
    
    rm_history = json.dumps(rm_history)
    self.db_wrapper.update_table_column(self.table_name, "rm_history", rm_history)
