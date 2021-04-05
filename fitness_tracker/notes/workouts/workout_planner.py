import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel,
                             QFrame, QCalendarWidget, QPushButton, QTextEdit, QRadioButton,
                             QGroupBox)
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QLocale, pyqtSignal, pyqtSlot
from fitness_tracker.database_wrapper import DatabaseWrapper
from .create_workout_window import CreateWorkoutWindow

class WorkoutPlanner(QWidget):
  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      color:#c7c7c7;
      font-weight: bold;
    }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
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
      border-color: #6C6C6C;
    }""")

    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Workouts"
    self.db_wrapper.create_local_table(self.table_name)
    if self.db_wrapper.local_table_is_empty(self.table_name): self.db_wrapper.insert_default_values(self.table_name)
    self.fetched_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "workouts"))
    self.current_date = datetime.today().strftime("%d/%m/%Y")
    if not self.current_date in self.fetched_workouts:
      self.fetched_workouts[self.current_date] = {"Personal Notes": "", "Workout Name": "None"}
    self.db_wrapper.update_table_column(self.table_name, "workouts", json.dumps(self.fetched_workouts))
    self.create_panel()
      
  def create_panel(self):
    self.grid = QGridLayout()
    self.grid.addWidget(self.create_calendar(), 0, 0, 2, 1)
    self.grid.addWidget(self.create_stats(), 0, 1, 2, 1)
    self.grid.addWidget(self.create_left_details(), 2, 0, 2, 1)
    self.grid.addWidget(self.create_right_details(), 2, 1, 2, 1)
    self.setLayout(self.grid)

  def create_calendar(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)

    layout = QHBoxLayout()
    
    self.calendar = QCalendarWidget(self)
    self.calendar.setLocale(QLocale(QLocale.English))
    self.calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
    self.calendar.clicked.connect(lambda: self.show_date(self.calendar.selectedDate()))
    layout.addWidget(self.calendar)

    frame.setLayout(layout)
    
    return frame

  def create_stats(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Stats")
    stats_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    number_of_workouts = QLabel(" ".join(["Total Number Of Workouts Done:", str(len(self.fetched_workouts))]))
    
    counter_this_month = 0
    for date in self.fetched_workouts:
      if date.split("/")[1] == self.current_date.split("/")[1]: counter_this_month += 1
    
    workouts_done_this_month = QLabel(" ".join(["Workouts Done This Month:", str(counter_this_month)]))
    
    last_workout = list(self.fetched_workouts.keys())[-1]
    for date, workout in reversed(list(self.fetched_workouts.items())):
      if len(workout) > 1: # found workout that is not todays default
       last_workout = date
       break
    last_workout = QLabel(" ".join(["Last Workout:", last_workout]))
    
    stats_layout.addWidget(stats_label)
    stats_layout.addWidget(number_of_workouts)
    stats_layout.addWidget(workouts_done_this_month)
    stats_layout.addWidget(last_workout)
    
    frame.setLayout(stats_layout)
    
    return frame
  
  def create_left_details(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)

    layout = QVBoxLayout()

    self.day_label = QLabel(self.current_date)
    self.day_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    workout_done_layout = QHBoxLayout()
    self.workout_done_label = QLabel(" ".join(["Workout Done:", self.fetched_workouts[self.current_date]["Workout Name"]]))
    workout_done_button = QPushButton("Change")
    workout_done_button.clicked.connect(lambda: self.change_workout_done())
    workout_done_layout.addWidget(self.workout_done_label)
    workout_done_layout.addWidget(workout_done_button)
    
    specific_workout_layout = QHBoxLayout()
    specific_workout_label = QLabel("Create a workout specific for one day: ")
    specific_workout_button = QPushButton("1 Time Workout")
    specific_workout_button.clicked.connect(lambda: self.show_1_time_window())
    specific_workout_layout.addWidget(specific_workout_label)
    specific_workout_layout.addWidget(specific_workout_button)

    personal_notes_layout = QVBoxLayout()
    personal_notes_label = QLabel("Personal Notes:")
    self.text_edit = QTextEdit()
    self.text_edit.setStyleSheet("color: black;")
    self.text_edit.setText(self.fetched_workouts[self.current_date]["Personal Notes"])
    self.personal_notes_save_button = QPushButton("Save Changes")
    self.personal_notes_save_button.clicked.connect(lambda: self.update_personal_notes())
    personal_notes_layout.addWidget(personal_notes_label)
    personal_notes_layout.addWidget(self.text_edit)
    personal_notes_layout.addWidget(self.personal_notes_save_button)
    
    layout.addWidget(self.day_label)
    layout.addLayout(workout_done_layout)
    layout.addLayout(specific_workout_layout)
    layout.addLayout(personal_notes_layout)
    frame.setLayout(layout)

    return frame

  def create_right_details(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    details_label = QLabel("Workout Details")
    details_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))
    
    self.grid_layout = QGridLayout()
    name_label = QLabel("Exercise Name")
    sets_label = QLabel("Sets")
    reps_label = QLabel("Reps")
    rest_label = QLabel("Rest")

    layout.addWidget(details_label)
    self.grid_layout.addWidget(name_label, 0, 0)
    self.grid_layout.addWidget(sets_label, 0, 1)
    self.grid_layout.addWidget(reps_label, 0, 2)
    self.grid_layout.addWidget(rest_label, 0, 3)
   
    if "Exercises" in self.fetched_workouts[self.current_date]:
      exercises_count = len(self.fetched_workouts[self.current_date]["Exercises"])
      
      self.number_of_exercises_label = QLabel(" ".join(["Number of Exercises:", str(exercises_count)]))
      
      set_count = 0

      for exercise in self.fetched_workouts[self.current_date]["Exercises"]:
        set_count += int(self.fetched_workouts[self.current_date]["Exercises"][exercise]["Sets"])

      self.total_set_count_label = QLabel(" ".join(["Total Set Count:", str(set_count)]))

      layout.addWidget(self.number_of_exercises_label)
      layout.addWidget(self.total_set_count_label)

      names_labels = [None] * len(self.fetched_workouts[self.current_date]["Exercises"].keys())
      sets_labels = [None] * len(self.fetched_workouts[self.current_date]["Exercises"].keys())
      reps_labels = [None] * len(self.fetched_workouts[self.current_date]["Exercises"].keys())
      rest_labels = [None] * len(self.fetched_workouts[self.current_date]["Exercises"].keys())
      
      j = 1
      for i, exercise in enumerate(self.fetched_workouts[self.current_date]["Exercises"].keys()):
        names_labels[i] = QLabel(exercise)
        sets_labels[i] = QLabel(str(self.fetched_workouts[self.current_date]["Exercises"][exercise]["Sets"]))
        reps_labels[i] = QLabel(str(self.fetched_workouts[self.current_date]["Exercises"][exercise]["Reps"]))
        rest_labels[i] = QLabel(str(self.fetched_workouts[self.current_date]["Exercises"][exercise]["Rest"]))
        
        self.grid_layout.addWidget(names_labels[i], j, 0)
        self.grid_layout.addWidget(sets_labels[i], j, 1)
        self.grid_layout.addWidget(reps_labels[i], j, 2)
        self.grid_layout.addWidget(rest_labels[i], j, 3)
        j += 1 

    layout.addWidget(QLabel(""))
    layout.addLayout(self.grid_layout)
    frame.setLayout(layout)

    return frame

  def show_date(self, date):
    day = str(date.day()) if date.day() > 9 else "0"+str(date.day())
    month = str(date.month()) if date.month() > 9 else "0"+str(date.month())
    parsed_date = "/".join([day, month, str(date.year())])
    self.current_date = parsed_date
    if not self.current_date in self.fetched_workouts:
      self.fetched_workouts[self.current_date] = {"Personal Notes": "", "Workout Name": "None"}
    self.day_label.setText(self.current_date)
    self.refresh_workout_done(True, True)
    self.text_edit.setText(self.fetched_workouts[self.current_date]["Personal Notes"])
  
  def show_1_time_window(self):
    self.create_workout_window = CreateWorkoutWindow(one_time=True)
    self.create_workout_window.refresh_after_creating_signal.connect(lambda signal: self.refresh_workout_done(signal))
    self.create_workout_window.setGeometry(100, 200, 300, 300) 
    self.create_workout_window.show()

  def update_personal_notes(self):
    self.fetched_workouts[self.current_date]["Personal Notes"] = self.text_edit.toPlainText() 
    self.db_wrapper.update_table_column(self.table_name, "workouts", json.dumps(self.fetched_workouts))

  def change_workout_done(self):
    self.select_workout_window = SelectWorkout()
    self.select_workout_window.refresh_workout_done_signal.connect(lambda signal: self.refresh_workout_done(signal))
    self.select_workout_window.setGeometry(100, 200, 300, 300) 
    self.select_workout_window.show()
  
  @pyqtSlot(bool)
  def refresh_workout_done(self, signal, date_change=False):
    if signal:
      if not date_change:
        self.fetched_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "workouts"))
      self.workout_done_label.setText(" ".join(["Workout Done:", self.fetched_workouts[self.current_date]["Workout Name"]]))
      old_right_details_reference = self.grid.itemAt(3).widget()
      new_right_details = self.create_right_details()
      self.grid.replaceWidget(old_right_details_reference, new_right_details)
      old_right_details_reference.setParent(None)
      

class SelectWorkout(QWidget):
  refresh_workout_done_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      background-color: #232120;
      color:#c7c7c7;
      font-weight: bold;
      font-family: Montserrat;
      font-size: 16px;
      }
    QPushButton{
      background-color: rgba(0, 0, 0, 0);
      border: 1px solid;
      font-size: 18px;
      font-weight: bold;
      border-color: #808080;
      min-height: 28px;
      white-space:nowrap;
      text-align: left;
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
      border-color: #6C6C6C;
    }""")
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Workouts"
    self.current_date = datetime.today().strftime("%d/%m/%Y")
    self.fetched_my_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "my_workouts"))
    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowTitle("Select My Workout")
    self.create_panel()

  def create_panel(self):
    layout = QVBoxLayout()
    if len(self.fetched_my_workouts) == 0:
      layout.addWidget(QLabel("My Workouts not found"))
    else:  
      groupbox = QGroupBox()
      radio_layout = QVBoxLayout()
      self.radio_buttons = [None] * len(self.fetched_my_workouts.keys())
      for i, workout in enumerate(self.fetched_my_workouts.keys()):
        self.radio_buttons[i] = QRadioButton(workout)
        radio_layout.addWidget(self.radio_buttons[i])
      groupbox.setLayout(radio_layout)
      layout.addWidget(groupbox)

    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_workout())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    buttons_layout.addWidget(save_button)
    buttons_layout.addWidget(cancel_button)

    layout.addLayout(buttons_layout)
    self.setLayout(layout)
  
  def save_workout(self): 
    for button in self.radio_buttons:
      if button.isChecked():
        fetched_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "workouts"))
        fetched_workouts[self.current_date]["Workout Name"] = button.text()
        fetched_workouts[self.current_date]["Exercises"] = self.fetched_my_workouts[button.text()]
        self.db_wrapper.update_table_column(self.table_name, "workouts", json.dumps(fetched_workouts))
        self.refresh_workout_done_signal.emit(True)
        self.close()
