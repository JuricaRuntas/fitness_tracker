import json
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper

class CreateWorkoutWindow(QWidget):
  refresh_my_workouts_signal = pyqtSignal(str)
  refresh_after_creating_signal = pyqtSignal(bool)

  def __init__(self, workout_name=None, one_time=False):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      background-color: #322d2d;
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
    self.setWindowModality(Qt.ApplicationModal)
    self.setWindowTitle("Create a New Workout")
    self.db_wrapper = DatabaseWrapper()
    self.table_name = "Workouts"
    self.workout_name = workout_name
    self.one_time = one_time
    self.current_date = datetime.today().strftime("%d/%m/%Y")
    self.fetched_my_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "my_workouts"))
    self.create_panel()

  def create_panel(self):
    layout = QVBoxLayout()
    
    workout_name_layout = QHBoxLayout()
    workout_name_label = QLabel("Workout Name:")
    self.workout_name_edit = QLineEdit()
    workout_name_layout.addWidget(workout_name_label)
    workout_name_layout.addWidget(self.workout_name_edit)
    
    grid_layout = QGridLayout()
    empty = QLabel("")
    name_label = QLabel("Name")
    sets_label = QLabel("Sets")
    reps_label = QLabel("Reps")
    rest_label = QLabel("Rest(Opt.)[min]")
    grid_layout.addWidget(empty, 0, 0)
    grid_layout.addWidget(name_label, 0, 1)
    grid_layout.addWidget(sets_label, 0, 2)
    grid_layout.addWidget(reps_label, 0, 3)
    grid_layout.addWidget(rest_label, 0, 4)
    
    exercise_number = [None] * 10
    self.name_edits = [None] * 10
    self.sets_edits = [None] * 10
    self.reps_edits = [None] * 10
    self.rest_edits = [None] * 10
    
    j = 1
    for i in range(10):
      exercise_number[i] = QLabel("Exercise #"+ str(i+1))
      self.name_edits[i], self.sets_edits[i], self.reps_edits[i], self.rest_edits[i] = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
      self.sets_edits[i].setValidator(QIntValidator())
      self.reps_edits[i].setValidator(QIntValidator())
      self.rest_edits[i].setValidator(QIntValidator())
      grid_layout.addWidget(exercise_number[i], j, 0)
      grid_layout.addWidget(self.name_edits[i], j, 1)
      grid_layout.addWidget(self.sets_edits[i], j, 2)
      grid_layout.addWidget(self.reps_edits[i], j, 3)
      grid_layout.addWidget(self.rest_edits[i], j, 4)
      j += 1
    
    if self.workout_name != None:
      self.workout_name_edit.setText(self.workout_name)
      for i, exercise in enumerate(self.fetched_my_workouts[self.workout_name].keys()):
        self.name_edits[i].setText(exercise)
        self.sets_edits[i].setText(self.fetched_my_workouts[self.workout_name][exercise]["Sets"])
        self.reps_edits[i].setText(self.fetched_my_workouts[self.workout_name][exercise]["Reps"])
        self.rest_edits[i].setText(self.fetched_my_workouts[self.workout_name][exercise]["Rest"])

    buttons_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_changes())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    buttons_layout.addWidget(save_button)
    if self.workout_name != None:
      delete_button = QPushButton("Delete Workout")
      delete_button.clicked.connect(lambda: self.delete_workout())
      buttons_layout.addWidget(delete_button)
    buttons_layout.addWidget(cancel_button)

    layout.addLayout(workout_name_layout)
    layout.addLayout(grid_layout)
    layout.addLayout(buttons_layout)
    self.setLayout(layout)
  
  def delete_workout(self):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Question)
    message_box.setText("Are you sure you want to delete this workout?")
    message_box.setWindowTitle("Confirm delete") 
    message_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    message_box.buttonClicked.connect(lambda answer: self.delete_workout_confirmed(answer.text()))
    message_box.exec_()

  def delete_workout_confirmed(self, answer):
    if "OK" in answer:
      del self.fetched_my_workouts[self.workout_name]
      self.db_wrapper.update_table_column(self.table_name, "my_workouts", json.dumps(self.fetched_my_workouts))
      self.refresh_my_workouts_signal.emit(self.workout_name)
      self.close()

  def save_changes(self):
    workout_name = self.workout_name_edit.text()
    if workout_name != "":
      new_workout = {}
      for i in range(10):
        exercise_dict = {}
        if self.name_edits[i].text() != "" and self.sets_edits[i].text() != "" and self.reps_edits[i].text() != "":
          exercise_dict["Sets"] = str(self.sets_edits[i].text())
          exercise_dict["Reps"] = str(self.reps_edits[i].text())
          exercise_dict["Rest"] = "N/A" if self.rest_edits[i].text() == "" else str(self.rest_edits[i].text())
          new_workout[self.name_edits[i].text()] = exercise_dict
      if self.one_time == False:
        self.fetched_my_workouts[workout_name] = new_workout
        self.db_wrapper.update_table_column(self.table_name, "my_workouts", json.dumps(self.fetched_my_workouts))
      else:
        workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "workouts"))
        if not self.current_date in workouts:
          self.fetched_workouts[self.current_date] = {"Personal Notes": "", "Workout Name": "None"}
        workouts[self.current_date]["Workout Name"] = workout_name
        workouts[self.current_date]["Exercises"] = new_workout
        self.db_wrapper.update_table_column(self.table_name, "workouts", json.dumps(workouts))
      self.refresh_after_creating_signal.emit(True)
    self.close()
