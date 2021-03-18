from functools import partial
import json
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt
from .compound_exercises_db import fetch_lift_history, delete_history_entry
from fitness_tracker.user_profile.profile_db import fetch_units

class LiftHistory(QScrollArea):
  def __init__(self, sqlite_connection, pg_connection):
    super().__init__()
    self.sqlite_connection = sqlite_connection
    self.sqlite_cursor = sqlite_connection.cursor()
    self.pg_connection = pg_connection
    self.pg_cursor = self.pg_connection
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
    self.setWindowFlags(Qt.Tool)
    self.units = "kg" if fetch_units(self.sqlite_cursor) == "metric" else "lb"
    self.setWindowTitle("Lift History")
    
    widget = QWidget()
    self.layout = QFormLayout(widget)
    exercise_label = QLabel("Exercise")
    exercise_label.setAlignment(Qt.AlignCenter)
    delete_label = QLabel("Delete")
    delete_label.setAlignment(Qt.AlignCenter)
    self.layout.addRow(exercise_label, delete_label)
    self.setWidget(widget)
    self.setWidgetResizable(True)
    self.create_history(True, True)

  @pyqtSlot(bool)
  def create_history(self, create, init_layout=False):
    lift_history = fetch_lift_history(self.sqlite_cursor)
    if create and not lift_history == None:
      if not init_layout: 
        self.delete_history()
      lift_history = json.loads(lift_history)
      self.labels = [None] * len(lift_history)
      self.delete_buttons = [None] * len(lift_history)

      for i in range(len(lift_history)):
        self.labels[i] = QLabel(self)
        self.delete_buttons[i] = QPushButton("X", self)
      
      for j, exercise in enumerate(lift_history):
        try:
          self.labels[j].setText(": ".join([exercise[0], " ".join([exercise[1], self.units])]))
        except TypeError: # joining lift for reps as 1RM lift 
          self.labels[j].setText(": ".join([exercise[0], " ".join(["x".join(exercise[1]), self.units])]))
        
        self.delete_buttons[j].setProperty("entry_index", exercise[-1])
        self.delete_buttons[j].clicked.connect(partial(self.delete_history_entry_from_layout, j, self.delete_buttons[j].property("entry_index")))
        
        self.layout.addRow(self.labels[j], self.delete_buttons[j])

  def delete_history(self):
    for i in reversed(range(self.layout.count())):
      self.layout.itemAt(i).widget().setParent(None)
  
  def delete_history_entry_from_layout(self, i, entry_index):
    self.labels[i].setParent(None)
    self.delete_buttons[i].setParent(None)
    delete_history_entry(entry_index, self.sqlite_connection, self.pg_connection)
