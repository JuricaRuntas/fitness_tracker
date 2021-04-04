from PyQt5.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel,
                             QFrame, QCalendarWidget, QPushButton, QTextEdit)
from PyQt5.QtGui import QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QLocale

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
    
    calendar = QCalendarWidget(self)
    calendar.setLocale(QLocale(QLocale.English))
    calendar.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

    layout.addWidget(calendar)

    frame.setLayout(layout)
    
    return frame

  def create_stats(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Stats")
    stats_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))
    number_of_workouts = QLabel("Total Number Of Workouts Done: 240")
    workouts_done_this_month = QLabel("Workouts Done This Month: 13")
    workouts_done_this_week = QLabel("Workouts Done This Week: 13")
    last_workout = QLabel("Last Workout: 9.11.2020")
    
    stats_layout.addWidget(stats_label)
    stats_layout.addWidget(number_of_workouts)
    stats_layout.addWidget(workouts_done_this_month)
    stats_layout.addWidget(workouts_done_this_week)
    stats_layout.addWidget(last_workout)
    
    frame.setLayout(stats_layout)
    
    return frame
  
  def create_left_details(self):
    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)

    layout = QVBoxLayout()

    day_label = QLabel("March 21st 2021")
    day_label.setFont(QFont("Ariel", 18, weight=QFont.Bold))

    workout_done_layout = QHBoxLayout()
    workout_done_label = QLabel("Workout Done: Leg Day #1/None")
    workout_done_button = QPushButton("Change")
    workout_done_layout.addWidget(workout_done_label)
    workout_done_layout.addWidget(workout_done_button)
    
    specific_workout_layout = QHBoxLayout()
    specific_workout_label = QLabel("Create a workout specific for one day: ")
    specific_workout_button = QPushButton("1 Time Workout")
    specific_workout_layout.addWidget(specific_workout_label)
    specific_workout_layout.addWidget(specific_workout_button)

    will_not_label = QLabel("1 Time Workouts will not be saved!")
    
    personal_notes_layout = QVBoxLayout()
    personal_notes_label = QLabel("Personal Notes:")
    text_edit = QTextEdit()
    text_edit.setStyleSheet("color: black;")
    text_edit.setText("1 Rep Max For Squats\nSkip leg extensions dropset, do a regular set instead")
    personal_notes_save_button = QPushButton("Save Changes")
    personal_notes_layout.addWidget(personal_notes_label)
    personal_notes_layout.addWidget(text_edit)
    personal_notes_layout.addWidget(personal_notes_save_button)
    
    layout.addWidget(day_label)
    layout.addLayout(workout_done_layout)
    layout.addLayout(specific_workout_layout)
    layout.addWidget(will_not_label)
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
    
    number_of_exercises_label = QLabel("Number of Exercises: 3")
    total_set_count_label = QLabel("Total Set Count: 12")

    grid_layout = QGridLayout()
    name_label = QLabel("Exercise Name")
    sets_label = QLabel("Sets")
    reps_label = QLabel("Reps")
    rest_label = QLabel("Rest")

    label1_name = QLabel("Back Squats")
    label1_sets = QLabel("4")
    label1_reps = QLabel("12")
    label1_rest = QLabel("2 min")

    names = ["Back Squats", "Shoulder Press", "Leg Press"]
    sets = ["4", "4", "4"]
    reps = ["12", "12", "12"]
    rest = ["2 min", "N/A", "N/A"]

    grid_layout.addWidget(name_label, 0, 0)
    grid_layout.addWidget(sets_label, 0, 1)
    grid_layout.addWidget(reps_label, 0, 2)
    grid_layout.addWidget(rest_label, 0, 3)
    
    j = 1
    for i in range(len(names)):
      grid_layout.addWidget(QLabel(names[i]), j, 0)
      grid_layout.addWidget(QLabel(sets[i]), j, 1)
      grid_layout.addWidget(QLabel(reps[i]), j, 2)
      grid_layout.addWidget(QLabel(rest[i]), j, 3)
      j += 1

    layout.addWidget(details_label)
    layout.addWidget(number_of_exercises_label)
    layout.addWidget(total_set_count_label)
    layout.addWidget(QLabel(""))
    layout.addLayout(grid_layout)
    frame.setLayout(layout)

    return frame
