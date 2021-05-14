import os
import json
from functools import partial
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from fitness_tracker.database_wrapper import DatabaseWrapper
from .create_workout_window import CreateWorkoutWindow
import sys

path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
if getattr(sys, 'frozen', False):
    path = os.path.join(os.path.dirname(sys.executable), "notes", "workouts")
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

class ExercisesAndWorkouts(QWidget):
  show_muscle_group_signal = pyqtSignal(str)

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
    self.fetched_my_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "my_workouts"))
    self.create_panel()

  def create_panel(self):
    self.grid = QGridLayout()
    self.grid.addWidget(self.create_my_workouts(), 0, 0)
    self.grid.addWidget(self.create_muscle_groups(), 0, 1)
    self.setLayout(self.grid)

  def create_my_workouts(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    
    layout = QVBoxLayout()

    self.workouts_layout = QVBoxLayout()
    self.workouts_layout.setAlignment(Qt.AlignTop)

    label_layout = QHBoxLayout()
    label_layout.setAlignment(Qt.AlignCenter)
    label = QLabel("My Workouts")
    label.setFont(QFont("Ariel", 18, weight=QFont.Bold))
    label_layout.addWidget(label)
    self.workouts_layout.addLayout(label_layout)

    if len(self.fetched_my_workouts.keys()) > 0:
      self.buttons = [None] * len(self.fetched_my_workouts.keys())
      
      for i, workout in enumerate(self.fetched_my_workouts.keys()):
        self.buttons[i] = QPushButton(workout)
        self.buttons[i].setProperty("button_index", i)
        self.buttons[i].clicked.connect(partial(self.select_button, self.buttons[i].property("button_index")))
        self.workouts_layout.addWidget(self.buttons[i])
    
    buttons_layout = QHBoxLayout()
    create_new_workout_button = QPushButton("Create New Workout")
    create_new_workout_button.clicked.connect(lambda: self.create_new_workout())
    edit_workout_button = QPushButton("Edit Workout")
    edit_workout_button.clicked.connect(lambda: self.edit_workout())
    buttons_layout.addWidget(create_new_workout_button)
    buttons_layout.addWidget(edit_workout_button)
    
    layout.addLayout(self.workouts_layout)
    layout.addLayout(buttons_layout)
    frame.setLayout(layout)

    return frame
  
  def create_muscle_groups(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)    

    label_layout = QHBoxLayout()
    label = QLabel("Exercises by muscle group", self)
    label.setFont(QFont("Ariel", 15))
    label_layout.addWidget(label)
    
    grid_layout = QGridLayout()
    grid_layout.setAlignment(Qt.AlignCenter)

    chest_muscle_group = QVBoxLayout()
    chest_image = QPushButton(self)
    chest_image.setIcon(QIcon(muscle_groups["Chest"]))
    
    chest_image.setIconSize(QSize(100, 100))
    chest_image.resize(100, 100)
    chest_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    chest_image.setCursor(Qt.PointingHandCursor)
    chest_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Chest"))

    chest_label = QLabel("Chest", self)
    chest_label.setAlignment(Qt.AlignCenter)
    chest_muscle_group.addWidget(chest_image)
    chest_muscle_group.addWidget(chest_label)
    
    back_muscle_group = QVBoxLayout()
    back_image = QPushButton(self)
    back_image.setIcon(QIcon(muscle_groups["Back"]))
    back_image.setIconSize(QSize(100, 100))
    back_image.resize(100, 100)
    back_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    back_image.setCursor(Qt.PointingHandCursor)
    back_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Back"))
    
    back_label = QLabel("Back", self)
    back_label.setAlignment(Qt.AlignCenter)
    back_muscle_group.addWidget(back_image)
    back_muscle_group.addWidget(back_label)
    
    triceps_muscle_group = QVBoxLayout()
    triceps_image = QPushButton(self)
    triceps_image.setIcon(QIcon(muscle_groups["Triceps"]))
    triceps_image.setIconSize(QSize(100, 100))
    triceps_image.resize(100, 100)
    triceps_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    triceps_image.setCursor(Qt.PointingHandCursor)
    triceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Triceps"))

    triceps_label = QLabel("Triceps", self)
    triceps_label.setAlignment(Qt.AlignCenter)
    triceps_muscle_group.addWidget(triceps_image)
    triceps_muscle_group.addWidget(triceps_label) 
   
    biceps_muscle_group = QVBoxLayout()
    biceps_image = QPushButton(self)
    biceps_image.setIcon(QIcon(muscle_groups["Biceps"]))
    biceps_image.setIconSize(QSize(100, 100))
    biceps_image.resize(100, 100)
    biceps_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    biceps_image.setCursor(Qt.PointingHandCursor)
    biceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Biceps"))
    
    biceps_label = QLabel("Biceps", self)
    biceps_label.setAlignment(Qt.AlignCenter)
    biceps_muscle_group.addWidget(biceps_image)
    biceps_muscle_group.addWidget(biceps_label) 
    
    shoulders_muscle_group = QVBoxLayout()
    shoulders_image = QPushButton(self)
    shoulders_image.setIcon(QIcon(muscle_groups["Shoulders"]))
    shoulders_image.setIconSize(QSize(100, 100))
    shoulders_image.resize(100, 100)
    shoulders_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    shoulders_image.setCursor(Qt.PointingHandCursor)
    shoulders_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Shoulders"))
    
    shoulders_label = QLabel("Shoulders", self)
    shoulders_label.setAlignment(Qt.AlignCenter)
    shoulders_muscle_group.addWidget(shoulders_image)
    shoulders_muscle_group.addWidget(shoulders_label) 
    
    core_muscle_group = QVBoxLayout()
    core_image = QPushButton(self)
    core_image.setIcon(QIcon(muscle_groups["Core"]))
    core_image.setIconSize(QSize(100, 100))
    core_image.resize(100, 100)
    core_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    core_image.setCursor(Qt.PointingHandCursor)
    core_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Core"))

    core_label = QLabel("Core", self)
    core_label.setAlignment(Qt.AlignCenter)
    core_muscle_group.addWidget(core_image)
    core_muscle_group.addWidget(core_label)

    quadriceps_muscle_group = QVBoxLayout()
    quadriceps_image = QPushButton(self)
    quadriceps_image.setIcon(QIcon(muscle_groups["Quadriceps"]))
    quadriceps_image.setIconSize(QSize(100, 100))
    quadriceps_image.resize(100, 100)
    quadriceps_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    quadriceps_image.setCursor(Qt.PointingHandCursor)
    quadriceps_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    quadriceps_label = QLabel("Quadriceps", self)
    quadriceps_label.setAlignment(Qt.AlignCenter)
    quadriceps_muscle_group.addWidget(quadriceps_image)
    quadriceps_muscle_group.addWidget(quadriceps_label)

    calves_muscle_group = QVBoxLayout()
    calves_image = QPushButton(self)
    calves_image.setIcon(QIcon(muscle_groups["Calves"]))
    calves_image.setIconSize(QSize(100, 100))
    calves_image.resize(100, 100)
    calves_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    calves_image.setCursor(Qt.PointingHandCursor)
    calves_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Calves"))
    
    calves_label = QLabel("Calves", self)
    calves_label.setAlignment(Qt.AlignCenter)
    calves_muscle_group.addWidget(calves_image)
    calves_muscle_group.addWidget(calves_label)
    
    hamstrings_muscle_group = QVBoxLayout()
    hamstrings_image = QPushButton(self)
    hamstrings_image.setIcon(QIcon(muscle_groups["Hamstrings"]))
    hamstrings_image.setIconSize(QSize(100, 100))
    hamstrings_image.resize(100, 100)
    hamstrings_image.setStyleSheet("border: none; padding-left: 50%; background-color: white;")
    hamstrings_image.setCursor(Qt.PointingHandCursor)
    hamstrings_image.clicked.connect(lambda: self.show_muscle_group_signal.emit("Legs"))
    
    hamstrings_label = QLabel("Hamstrings", self)
    hamstrings_label.setAlignment(Qt.AlignCenter)
    hamstrings_muscle_group.addWidget(hamstrings_image)
    hamstrings_muscle_group.addWidget(hamstrings_label)

    grid_layout.addLayout(chest_muscle_group, 0, 0)
    grid_layout.addLayout(back_muscle_group, 0, 1)
    grid_layout.addLayout(triceps_muscle_group, 0, 2)
    grid_layout.addLayout(biceps_muscle_group, 1, 0)
    grid_layout.addLayout(shoulders_muscle_group, 1, 1)
    grid_layout.addLayout(core_muscle_group, 1, 2)
    grid_layout.addLayout(quadriceps_muscle_group, 2, 0)
    grid_layout.addLayout(calves_muscle_group, 2, 1)
    grid_layout.addLayout(hamstrings_muscle_group, 2, 2)

    layout.addLayout(label_layout) 
    layout.addWidget(QLabel(" "))
    layout.addLayout(grid_layout)
    frame.setLayout(layout) 

    return frame

  def create_new_workout(self):
    self.create_workout_window = CreateWorkoutWindow() 
    self.create_workout_window.refresh_after_creating_signal.connect(lambda signal: self.refresh_my_workouts_after_create(signal))
    self.create_workout_window.setGeometry(100, 200, 300, 300) 
    self.create_workout_window.show()

  def edit_workout(self):
    selected_button = None
    try:
      for button in self.buttons:
        if button.isFlat(): selected_button = button
      if selected_button != None:
        self.edit_workout_window = CreateWorkoutWindow(selected_button.text())
        self.edit_workout_window.refresh_my_workouts_signal.connect(lambda workout_name: self.refresh_my_workouts(workout_name))
        self.edit_workout_window.setGeometry(100, 200, 300, 300) 
        self.edit_workout_window.show()
    except AttributeError: # no workouts
      return

  def select_button(self, button_index):
    for button in self.buttons:
      if button.isFlat():
        button.setFlat(False)
        button.setStyleSheet("")
        button.setStyleSheet("""
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
        QPushButton:pressed:{
          border: 2px solid;
          background-color: #323232;
          border-color: #6C6C6C;
        }""")

    self.buttons[button_index].setFlat(True)
    self.buttons[button_index].setStyleSheet("background-color: #323232; border-color: #6C6C6C; border: 2px solid;")
  
  @pyqtSlot(str)
  def refresh_my_workouts(self, workout_name): 
    for button in self.buttons:
      if button.text() == workout_name:
        button.setParent(None)

  @pyqtSlot(bool)
  def refresh_my_workouts_after_create(self, signal):
    if signal:
      self.fetched_my_workouts = json.loads(self.db_wrapper.fetch_local_column(self.table_name, "my_workouts"))
      for i in reversed(range(self.workouts_layout.count())):
        if self.workouts_layout.itemAt(i).widget() != None:
          self.workouts_layout.itemAt(i).widget().setParent(None)
      
      if len(self.fetched_my_workouts.keys()) > 0:
        self.buttons = [None] * len(self.fetched_my_workouts.keys())
        for i, workout in enumerate(self.fetched_my_workouts.keys()):
          self.buttons[i] = QPushButton(workout)
          self.buttons[i].setProperty("button_index", i)
          self.buttons[i].clicked.connect(partial(self.select_button, self.buttons[i].property("button_index")))
          self.workouts_layout.addWidget(self.buttons[i])
