from functools import partial
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QScrollArea
from PyQt5.QtGui import QFont 
from PyQt5.QtCore import Qt, pyqtSignal
from .workouts_api import WorkoutsAPI
from .exercise_info import Exercise

class Exercises(QScrollArea):
  show_exercise_signal = pyqtSignal(object)

  def __init__(self, parent, muscle_group):
    super().__init__(parent)
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
    self.api = WorkoutsAPI()
    self.muscle_group = muscle_group
    self.exercises = self.api.fetch_exercises(muscle_group, limit=100)
    widget = QWidget()
    self.grid = QGridLayout(widget)
    self.setWidget(widget)
    self.setWidgetResizable(True)
    self.create_panel()
    
  def create_panel(self):
    self.found_results_label = QLabel("Found "+str(len(self.exercises))+" for '"+self.muscle_group+"' muscle group")
    self.found_results_label.setFont(QFont("Ariel", 20, weight=QFont.Bold))
    self.grid.addWidget(self.found_results_label, 0, 0)

    self.buttons = [None] * len(self.exercises)
    j = 1
    for i, exercise in enumerate(self.exercises):
      self.buttons[i] = QPushButton(exercise["name"])
      self.buttons[i].setProperty("exercise_info", exercise)
      self.buttons[i].clicked.connect(partial(self.show_exercise_signal.emit, self.buttons[i].property("exercise_info"))) 
      self.grid.addWidget(self.buttons[i], j, 0)
      j += 1
