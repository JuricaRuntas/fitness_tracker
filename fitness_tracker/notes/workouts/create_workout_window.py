from functools import partial
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QRadioButton, QFormLayout, QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from .workouts_db import update_workouts, update_current_workout

class CreateWorkoutWindow1(QWidget):
  continue_signal = pyqtSignal(object)

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Create New Workout")
    self.create_layout()

  def create_layout(self):
    form = QFormLayout()
    workout_name_label = QLabel("Workout name", self)
    self.workout_name_line_edit = QLineEdit()
    
    days_in_a_week_label = QLabel("Days in a week", self)
    self.days_in_a_week = QHBoxLayout()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
     
    for day in days:
      button = QRadioButton(day)
      button.setAutoExclusive(False)
      self.days_in_a_week.addWidget(button)
    
    set_current_workout_label = QLabel("Set as current workout plan?")
    set_current_workout_layout = QHBoxLayout()
    self.yes = QRadioButton("Yes")
    self.yes.setChecked(True)
    self.no = QRadioButton("No")
    set_current_workout_layout.addWidget(self.yes)
    set_current_workout_layout.addWidget(self.no)
    
    continue_button = QPushButton("Continue")
    continue_button.clicked.connect(lambda: self.emit_continue_signal())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())

    form.addRow(workout_name_label, self.workout_name_line_edit)
    form.addRow(days_in_a_week_label, self.days_in_a_week)
    form.addRow(set_current_workout_label, set_current_workout_layout)
    form.addRow(cancel_button, continue_button)
    self.setLayout(form)

  def emit_continue_signal(self):
    workout_name = self.workout_name_line_edit.text()
    days = []
    set_current_workout = True if self.yes.isChecked() else False
    for i in range(self.days_in_a_week.count()):
      button = self.days_in_a_week.itemAt(i).widget()
      if button.isChecked():
        days.append(button.text())
    if workout_name != "" and len(days) > 0:
      self.continue_signal.emit([workout_name, days, set_current_workout])

class CreateWorkoutWindow2(QWidget):
  show_edit_workout = pyqtSignal(str)
  refresh_layout_signal = pyqtSignal(bool)
  show_existing_workout_edit = pyqtSignal(object)

  def __init__(self, workout_name, workout_days, set_as_current_workout=False, empty_workout=True):
    super().__init__()
    self.workout_name = workout_name
    self.empty_workout = empty_workout
    self.setWindowTitle(self.workout_name)
    self.set_as_current_workout = set_as_current_workout
    self.workout_days = workout_days
    self.workouts = {}
    self.create_layout()

  def create_layout(self):
    days_layout = QVBoxLayout()
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_workout_plan())
    for day in self.workout_days:
      day_button = QPushButton(day, self)
      if self.empty_workout:
        day_button.clicked.connect(partial(self.show_edit_workout.emit, day))
      else:
        day_button.clicked.connect(partial(self.show_existing_workout_edit.emit, [self.workout_name, day]))
      day_button.setFixedSize(250, 100)
      days_layout.addWidget(day_button)
    days_layout.setAlignment(Qt.AlignCenter)
    days_layout.addWidget(save_button)
    self.setLayout(days_layout)
  
  @pyqtSlot(object)
  def add_workouts(self, workout_day):
    self.workouts[workout_day[0]] = workout_day[1]

  def save_workout_plan(self):
    update_workouts(self.workout_name, self.workouts)
    if self.set_as_current_workout:
      update_current_workout(self.workout_name, self.set_as_current_workout)
    self.refresh_layout_signal.emit(True)
    self.close()

class EditWorkout(QWidget):
  update_workout_day_signal = pyqtSignal(object)

  def __init__(self, day, existing_workout_day_info={}):
    super().__init__()
    self.workout_day = day
    self.workout_info = existing_workout_day_info
    self.setWindowTitle("".join(["Edit Workout ", "- ", self.workout_day]))
    
    i = 0
    while len(self.workout_info) < 6:
      self.workout_info[str(i)] = "empty_exercise"
      i += 1
    
    self.create_layout()

  def create_layout(self):
    grid_layout = QGridLayout() 
   
    exercise_label = QLabel("Exercise")
    sets_label = QLabel("Sets")
    reps_label = QLabel("Reps")
    rest_label = QLabel("Rest")
    duration_label = QLabel("Duration (optional)")
    
    self.labels = [exercise_label, sets_label, reps_label,
                   rest_label, duration_label]

    labels_layout = QHBoxLayout()
    for label in self.labels:
      labels_layout.addWidget(label)
    
    grid_layout.addLayout(labels_layout, 0, 5)
    
    self.row_layouts = [None] * 6
    number_labels = [None] * 6
    exercise_line_edits = [None] * 6
    sets_line_edits = [None] * 6
    reps_line_edits = [None] * 6
    rest_line_edits = [None] * 6
    duration_line_edits = [None] * 6
    
    row = 1
    i = 0
    for exercise in self.workout_info:
      self.row_layouts[i] = QHBoxLayout()
      number_labels[i] = QLabel(str(i+1)+".")
      exercise_line_edits[i] = QLineEdit()
      sets_line_edits[i] = QLineEdit()
      reps_line_edits[i] = QLineEdit()
      rest_line_edits[i] = QLineEdit()
      duration_line_edits[i] = QLineEdit()
      if self.workout_info[exercise] != "empty_exercise":
        exercise_line_edits[i].setText(exercise)
        sets_line_edits[i].setText(self.workout_info[exercise]["Sets"])
        reps_line_edits[i].setText(self.workout_info[exercise]["Reps"])
        rest_line_edits[i].setText(self.workout_info[exercise]["Rest"])
        duration_line_edits[i].setText(self.workout_info[exercise]["Duration (optional)"])

      self.row_layouts[i].addWidget(number_labels[i])
      self.row_layouts[i].addWidget(exercise_line_edits[i])
      self.row_layouts[i].addWidget(sets_line_edits[i])
      self.row_layouts[i].addWidget(reps_line_edits[i])
      self.row_layouts[i].addWidget(rest_line_edits[i])
      self.row_layouts[i].addWidget(duration_line_edits[i])
      
      grid_layout.addLayout(self.row_layouts[i], row, 5)
      row += 1
      i += 1

    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_workout())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())
    
    grid_layout.addWidget(cancel_button, row, 2)
    grid_layout.addWidget(save_button, row, 3)
    self.setLayout(grid_layout)

  def save_workout(self):
    workout = {}
    for row in self.row_layouts:
      exercise_name = ""
      for i in range(row.count()):
        if i != 0: # ignore number_label
          label = self.labels[i-1].text()
          row_widget = row.itemAt(i).widget()
          if exercise_name == "" and label == "Exercise":
            exercise_name = row_widget.text()
            if exercise_name == "": break
            else: workout[exercise_name] = {}
          else:
            workout[exercise_name][label] = row_widget.text()
    self.update_workout_day_signal.emit([self.workout_day, workout])
    self.close()
