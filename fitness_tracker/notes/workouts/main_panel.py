import os
import json
from functools import partial
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QCalendarWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QLocale, QSize, pyqtSignal, pyqtSlot
from .exercises.exercises import Exercises
from .create_workout_window import CreateWorkoutWindow1, CreateWorkoutWindow2, EditWorkout
from .workouts_db import (create_workouts_table, insert_default_workouts_data,
                          table_is_empty, fetch_current_workout_plan, fetch_workouts,
                          delete_workout, update_current_workout)

path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
muscle_groups_path = os.path.join(path, "muscle_groups")
icons_path = os.path.join(path, "icons")

muscle_groups = {"Chest": os.path.join(muscle_groups_path, "chest.svg"),
                 "Back": os.path.join(muscle_groups_path, "back.svg"),
                 "Core": os.path.join(muscle_groups_path, "core.svg"),
                 "Biceps": os.path.join(muscle_groups_path, "biceps.svg"),
                 "Triceps": os.path.join(muscle_groups_path, "triceps.svg"),
                 "Quadriceps": os.path.join(muscle_groups_path, "quads.svg"),
                 "Calves": os.path.join(muscle_groups_path, "calves.svg"),
                 "Shoulders": os.path.join(muscle_groups_path, "shoulders.svg"),
                 "Gluteus": os.path.join(muscle_groups_path, "gluteus.svg"),
                 "Hamstrings": os.path.join(muscle_groups_path, "hamstrings.svg")}

class MainPanel(QWidget):
  show_muscle_group_signal = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__()
    create_workouts_table()
    if table_is_empty(): insert_default_workouts_data()
    self.current_workout_plan = fetch_current_workout_plan()
    if self.current_workout_plan == "":
      self.current_workout_plan = "None"
    self.fetched_workouts = json.loads(fetch_workouts())
    # {WorkoutName: {("CreateWorkoutWindow2", CreateWorkoutWindow2): {Day: EditWorkout object}}}
    self.workouts = self.generate_workouts_objects()
    self.create_panel()
      
  def create_panel(self):
    self.grid = QGridLayout()
    self.grid.addWidget(self.create_stats(), 0, 0, 1, 2)
    self.grid.addWidget(self.create_calendar_workouts(), 1, 0, 1, 2)
    self.grid.addWidget(self.create_exercises(), 2, 0, 1, 2)
    self.setLayout(self.grid)
    
  def generate_workouts_objects(self):
    workouts = {}
    if len(self.fetched_workouts) > 0:
      for workout in self.fetched_workouts:
        workout_name = workout
        workout_days = list(self.fetched_workouts[workout].keys())
        create_workout_window_2 = CreateWorkoutWindow2(workout_name, workout_days, empty_workout=False)
        create_workout_window_2.show_existing_workout_edit.connect(lambda s: self.show_existing_workout_edit(s))
        days = {}
        for workout_day in self.fetched_workouts[workout].keys():
           workout_day_info = self.fetched_workouts[workout][workout_day]
           edit_workout_object = EditWorkout(workout_day, workout_day_info)
           edit_workout_object.update_workout_day_signal.connect(lambda s: create_workout_window_2.add_workouts(s))
           days[workout_day] = edit_workout_object
        workouts[workout] = {("CreateWorkoutWindow2", create_workout_window_2): days}
    
    i = 0
    while len(workouts) < 3:
      workouts[str(i)] = "empty_workout"
      i += 1
    return workouts
  
  @pyqtSlot(object)
  def show_create_window_2(self, signal):
    self.create_workout_window1.close()
    workout_name = signal[0]
    workout_days = signal[1]
    current_workout = signal[2]
    self.create_workout_window2 = CreateWorkoutWindow2(workout_name, workout_days, set_as_current_workout=current_workout, empty_workout=True)
    self.create_workout_window2.show_edit_workout.connect(lambda s: self.show_edit_workout_window(s))
    self.create_workout_window2.refresh_layout_signal.connect(lambda s: self.refresh_layout(s)) 
    
    self.edit_windows = {}
    for day in signal[1]:
      self.edit_windows[day] = EditWorkout(day)
      self.edit_windows[day].update_workout_day_signal.connect(lambda s: self.create_workout_window2.add_workouts(s))
    
    self.create_workout_window2.show()
  
  @pyqtSlot(str)
  def show_edit_workout_window(self, workout_day):
    self.edit_windows[workout_day].show()  
  
  def show_empty_workout_edit(self):
    self.create_workout_window1 = CreateWorkoutWindow1()
    self.create_workout_window1.continue_signal.connect(lambda s: self.show_create_window_2(s))
    self.create_workout_window1.show()

  def show_existing_workout(self, workout):
    create_workout_window_2 = list(self.workouts[workout].keys())[0][1]
    create_workout_window_2.show()
  
  @pyqtSlot(object)
  def show_existing_workout_edit(self, workout):
    workout_name = workout[0]
    workout_day = workout[1]
    for key in self.workouts[workout_name]:
      for day in self.workouts[workout_name][key]:
        if day == workout_day:
          self.workouts[workout_name][key][day].show()

  @pyqtSlot(bool)
  def refresh_layout(self, signal):
    if signal:
      self.fetched_workouts = json.loads(fetch_workouts())
      self.workouts = self.generate_workouts_objects()
      self.current_workout_plan = fetch_current_workout_plan()
      
      if self.current_workout_plan == "" or self.fetched_workouts == {}:
        self.current_workout_plan = ""
      elif not self.current_workout_plan in self.fetched_workouts:
        next_workout = list(self.workouts.keys())[0]
        self.current_workout_plan = next_workout
      update_current_workout(self.current_workout_plan, True)
      self.current_workout_label2.setText(self.current_workout_plan)
       
      old_workouts_reference = self.grid.itemAt(1).widget()
      new_calendar_workouts_frame = self.create_calendar_workouts()
      self.grid.replaceWidget(old_workouts_reference, new_calendar_workouts_frame)
      old_workouts_reference.setParent(None)
  
  def show_delete_workout_dialog(self, workout):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Question)
    message_box.setText("Are you sure you want to delete this workout?")
    message_box.setWindowTitle("Confirm delete")
    message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    message_box.buttonClicked.connect(lambda answer: self.delete_existing_workout(answer.text(), workout))
    message_box.exec_()
  
  def delete_existing_workout(self, answer, workout):
    if "OK" in answer:
      delete_workout(workout)
      self.refresh_layout(True)

  def create_stats(self):
    frame = QFrame()
    frame.setProperty("name", "Stats frame 1")
    frame.setFrameStyle(QFrame.StyledPanel)

    current_workout_frame = QFrame()
    current_workout_frame.setFrameStyle(QFrame.StyledPanel)
    current_workout_layout = QVBoxLayout()

    current_workout_label = QLabel("Current workout plan", self)
    current_workout_label.setAlignment(Qt.AlignCenter)
    self.current_workout_label2 = QLabel(self.current_workout_plan, self)
    self.current_workout_label2.setAlignment(Qt.AlignCenter)

    current_workout_layout.addWidget(current_workout_label)
    current_workout_layout.addWidget(self.current_workout_label2)

    current_workout_frame.setLayout(current_workout_layout)

    last_workout_frame = QFrame()
    last_workout_frame.setFrameStyle(QFrame.StyledPanel)
    last_workout_layout = QVBoxLayout()

    last_workout_label = QLabel("Last workout", self)
    last_workout_label.setAlignment(Qt.AlignCenter)
    last_workout_label2 = QLabel("Monday, 9.2.2017", self)
    last_workout_label2.setAlignment(Qt.AlignCenter)

    last_workout_layout.addWidget(last_workout_label)
    last_workout_layout.addWidget(last_workout_label2)

    last_workout_frame.setLayout(last_workout_layout)

    number_of_workouts_frame = QFrame()
    number_of_workouts_frame.setFrameStyle(QFrame.StyledPanel)
    number_of_workouts_layout = QVBoxLayout()

    number_of_workouts_label = QLabel("Total number of workouts", self)
    number_of_workouts_label.setAlignment(Qt.AlignCenter)
    number_of_workouts_label2 = QLabel("31", self)
    number_of_workouts_label2.setAlignment(Qt.AlignCenter)

    number_of_workouts_layout.addWidget(number_of_workouts_label)
    number_of_workouts_layout.addWidget(number_of_workouts_label2)

    number_of_workouts_frame.setLayout(number_of_workouts_layout)

    wrapper = QHBoxLayout()
    wrapper.addWidget(current_workout_frame)
    wrapper.addWidget(last_workout_frame)
    wrapper.addWidget(number_of_workouts_frame)
    frame.setLayout(wrapper)
    return frame

  def create_calendar_workouts(self):
    frame = QFrame()
    frame.setProperty("name", "Calendar frame 2")
    frame.setFrameStyle(QFrame.StyledPanel)
    layout = QHBoxLayout()
    
    calendar = QCalendarWidget(self)
    calendar.setLocale(QLocale(QLocale.English))
    calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

    layout.addWidget(calendar)
    layout.addWidget(self.create_my_workouts())
    frame.setLayout(layout)
    return frame   
  
  def create_my_workouts(self):
    my_workouts_frame = QFrame()
    my_workouts_frame.setFrameStyle(QFrame.StyledPanel)
    my_workouts_layout = QVBoxLayout()
    my_workouts_label = QLabel("My Workouts", self)
    my_workouts_layout.addWidget(my_workouts_label)

    workout_buttons_layouts = [None] * 3
    workout_buttons = [None] * 3
    workout_buttons_frames = [None] * 3
    delete_buttons = [None] * 3
    
    i = 0 
    for workout in self.workouts:
      workout_buttons_frames[i] = QFrame()   
      workout_buttons_frames[i].setFrameStyle(QFrame.StyledPanel)
      workout_buttons_layouts[i] = QHBoxLayout()
      
      delete_buttons[i] = QPushButton(QIcon(os.path.join(icons_path, "x.png")), "", self)
      delete_buttons[i].setStyleSheet("border: none")
      delete_buttons[i].setCursor(QCursor(Qt.PointingHandCursor))
      
      if self.workouts[workout] == "empty_workout":
        workout_buttons[i] = QPushButton("<empty workout> 0 days", self)
        workout_buttons[i].clicked.connect(lambda: self.show_empty_workout_edit())
      else:
        key_for_days = list(self.workouts[workout].keys())[0]
        days = len(self.workouts[workout][key_for_days])
        if days == 1: string_days = "day"
        else: string_days = "days"
        workout_buttons[i] = QPushButton(" ".join([workout, str(days), string_days]))
        workout_buttons[i].clicked.connect(partial(self.show_existing_workout, workout))
        delete_buttons[i].clicked.connect(partial(self.show_delete_workout_dialog, workout))

      workout_buttons[i].setFlat(True)
      workout_buttons[i].setStyleSheet("color: white")
      workout_buttons[i].setCursor(QCursor(Qt.PointingHandCursor))
      
      workout_buttons_layouts[i].addWidget(workout_buttons[i])
      workout_buttons_layouts[i].addWidget(delete_buttons[i])
      workout_buttons_frames[i].setLayout(workout_buttons_layouts[i])
      my_workouts_layout.addWidget(workout_buttons_frames[i]) 
    
    my_workouts_frame.setLayout(my_workouts_layout)
    return my_workouts_frame

  def create_exercises(self):
    frame = QFrame()
    frame.setProperty("name", "Exercises frame 3")
    frame.setFrameStyle(QFrame.StyledPanel)
    exercises_layout = QVBoxLayout()

    label = QLabel("Exercises", self)
    label.setFont(QFont("Ariel", 15))
    
    first_row = QHBoxLayout()

    chest_muscle_group = QVBoxLayout()
    chest_image = QPushButton(self)
    chest_image.setIcon(QIcon(muscle_groups["Chest"]))
    chest_image.setIconSize(QSize(100, 60))
    chest_image.resize(100, 60)
    chest_image.setStyleSheet("border: none")
    chest_image.setCursor(Qt.PointingHandCursor)
    chest_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Chest"))

    chest_label = QLabel("Chest", self)
    chest_label.setAlignment(Qt.AlignCenter)
    chest_muscle_group.addWidget(chest_image)
    chest_muscle_group.addWidget(chest_label)
    
    back_muscle_group = QVBoxLayout()
    back_image = QPushButton(self)
    back_image.setIcon(QIcon(muscle_groups["Back"]))
    back_image.setIconSize(QSize(100, 60))
    back_image.resize(100, 60)
    back_image.setStyleSheet("border: none")
    back_image.setCursor(Qt.PointingHandCursor)
    back_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Back"))
    
    back_label = QLabel("Back", self)
    back_label.setAlignment(Qt.AlignCenter)
    back_muscle_group.addWidget(back_image)
    back_muscle_group.addWidget(back_label)
    
    triceps_muscle_group = QVBoxLayout()
    triceps_image = QPushButton(self)
    triceps_image.setIcon(QIcon(muscle_groups["Triceps"]))
    triceps_image.setIconSize(QSize(100, 60))
    triceps_image.resize(100, 60)
    triceps_image.setStyleSheet("border: none")
    triceps_image.setCursor(Qt.PointingHandCursor)
    triceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Triceps"))

    triceps_label = QLabel("Triceps", self)
    triceps_label.setAlignment(Qt.AlignCenter)
    triceps_muscle_group.addWidget(triceps_image)
    triceps_muscle_group.addWidget(triceps_label)

    biceps_muscle_group = QVBoxLayout()
    biceps_image = QPushButton(self)
    biceps_image.setIcon(QIcon(muscle_groups["Biceps"]))
    biceps_image.setIconSize(QSize(100, 60))
    biceps_image.resize(100, 60)
    biceps_image.setStyleSheet("border: none")
    biceps_image.setCursor(Qt.PointingHandCursor)
    biceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Biceps"))
    
    biceps_label = QLabel("Biceps", self)
    biceps_label.setAlignment(Qt.AlignCenter)
    biceps_muscle_group.addWidget(biceps_image)
    biceps_muscle_group.addWidget(biceps_label)
    
    shoulders_muscle_group = QVBoxLayout()
    shoulders_image = QPushButton(self)
    shoulders_image.setIcon(QIcon(muscle_groups["Shoulders"]))
    shoulders_image.setIconSize(QSize(100, 60))
    shoulders_image.resize(100, 60)
    shoulders_image.setStyleSheet("border: none")
    shoulders_image.setCursor(Qt.PointingHandCursor)
    shoulders_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Shoulders"))
    
    shoulders_label = QLabel("Shoulders", self)
    shoulders_label.setAlignment(Qt.AlignCenter)
    shoulders_muscle_group.addWidget(shoulders_image)
    shoulders_muscle_group.addWidget(shoulders_label)

    first_row.addLayout(chest_muscle_group)
    first_row.addLayout(back_muscle_group)
    first_row.addLayout(triceps_muscle_group)
    first_row.addLayout(biceps_muscle_group)
    first_row.addLayout(shoulders_muscle_group)
    
    second_row = QHBoxLayout()
    
    core_muscle_group = QVBoxLayout()
    core_image = QPushButton(self)
    core_image.setIcon(QIcon(muscle_groups["Core"]))
    core_image.setIconSize(QSize(100, 60))
    core_image.resize(100, 60)
    core_image.setStyleSheet("border: none")
    core_image.setCursor(Qt.PointingHandCursor)
    core_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Core"))
    
    core_label = QLabel("Core", self)
    core_label.setAlignment(Qt.AlignCenter)
    core_muscle_group.addWidget(core_image)
    core_muscle_group.addWidget(core_label)
    
    gluteus_muscle_group = QVBoxLayout()
    gluteus_image = QPushButton(self)
    gluteus_image.setIcon(QIcon(muscle_groups["Gluteus"]))
    gluteus_image.setIconSize(QSize(100, 60))
    gluteus_image.resize(100, 60)
    gluteus_image.setStyleSheet("border: none")
    gluteus_image.setCursor(Qt.PointingHandCursor)
    gluteus_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    gluteus_label = QLabel("Gluteus", self)
    gluteus_label.setAlignment(Qt.AlignCenter)
    gluteus_muscle_group.addWidget(gluteus_image)
    gluteus_muscle_group.addWidget(gluteus_label)

    quadriceps_muscle_group = QVBoxLayout()
    quadriceps_image = QPushButton(self)
    quadriceps_image.setIcon(QIcon(muscle_groups["Quadriceps"]))
    quadriceps_image.setIconSize(QSize(100, 60))
    quadriceps_image.resize(100, 60)
    quadriceps_image.setStyleSheet("border: none")
    quadriceps_image.setCursor(Qt.PointingHandCursor)
    quadriceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    quadriceps_label = QLabel("Quadriceps", self)
    quadriceps_label.setAlignment(Qt.AlignCenter)
    quadriceps_muscle_group.addWidget(quadriceps_image)
    quadriceps_muscle_group.addWidget(quadriceps_label)

    calves_muscle_group = QVBoxLayout()
    calves_image = QPushButton(self)
    calves_image.setIcon(QIcon(muscle_groups["Calves"]))
    calves_image.setIconSize(QSize(100, 60))
    calves_image.resize(100, 60)
    calves_image.setStyleSheet("border: none")
    calves_image.setCursor(Qt.PointingHandCursor)
    calves_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Calves"))
    
    calves_label = QLabel("Calves", self)
    calves_label.setAlignment(Qt.AlignCenter)
    calves_muscle_group.addWidget(calves_image)
    calves_muscle_group.addWidget(calves_label)
    
    hamstrings_group = QVBoxLayout()
    hamstrings_image = QPushButton(self)
    hamstrings_image.setIcon(QIcon(muscle_groups["Hamstrings"]))
    hamstrings_image.setIconSize(QSize(100, 60))
    hamstrings_image.resize(100, 60)
    hamstrings_image.setStyleSheet("border: none")
    hamstrings_image.setCursor(Qt.PointingHandCursor)
    hamstrings_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    hamstrings_label = QLabel("Hamstrings", self)
    hamstrings_label.setAlignment(Qt.AlignCenter)
    hamstrings_group.addWidget(hamstrings_image)
    hamstrings_group.addWidget(hamstrings_label)
    
    second_row.addLayout(core_muscle_group)
    second_row.addLayout(gluteus_muscle_group)
    second_row.addLayout(quadriceps_muscle_group)
    second_row.addLayout(calves_muscle_group)
    second_row.addLayout(hamstrings_group)

    exercises_layout.addWidget(label)
    exercises_layout.addLayout(first_row)
    exercises_layout.addLayout(second_row)
    frame.setLayout(exercises_layout)
    return frame
