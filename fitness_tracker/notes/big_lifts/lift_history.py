from functools import partial
import json
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot
from .big_lifts_db import fetch_lift_history, delete_history_entry
from fitness_tracker.user_profile.profile_db import fetch_units

class LiftHistory(QWidget):
  def __init__(self):
    super().__init__()
    self.units = "kg" if fetch_units() == "metric" else "lb"
    self.setWindowTitle("Lift History")
    self.layout = QVBoxLayout()
    self.setLayout(self.layout)
    self.create_history(True, True)

  @pyqtSlot(bool)
  def create_history(self, create, init_layout=False):
    lift_history = fetch_lift_history()
    if create and not lift_history == None:
      if not init_layout: 
        self.delete_history()
      lift_history = json.loads(lift_history)
      self.layouts = [None] * len(lift_history)
      self.labels = [None] * len(lift_history)
      self.delete_buttons = [None] * len(lift_history)

      for i in range(len(lift_history)):
        self.layouts[i] = QHBoxLayout()
        self.labels[i] = QLabel(self)
        self.delete_buttons[i] = QPushButton("X", self)
      
      for j, exercise in enumerate(lift_history):
        try:
          self.labels[j].setText(": ".join([exercise[0], " ".join([exercise[1], self.units])]))
        except TypeError: # joining lift for reps as 1RM lift 
          self.labels[j].setText(": ".join([exercise[0], " ".join(["x".join(exercise[1]), self.units])]))
        
        self.delete_buttons[j].setProperty("entry_index", exercise[-1])
        self.delete_buttons[j].clicked.connect(partial(self.delete_history_entry, j, self.delete_buttons[j].property("entry_index")))
        
        self.layouts[j].addWidget(self.labels[j])
        self.layouts[j].addWidget(self.delete_buttons[j])
        self.layout.addLayout(self.layouts[j])

  def delete_history(self):
    index = self.layout.count()
    for i in reversed(range(index)):
      history_entry = self.layout.itemAt(i).layout()
      history_entry_index = history_entry.count()
      for j in reversed(range(history_entry_index)):
        history_entry_widget = history_entry.itemAt(j).widget()
        history_entry_widget.setParent(None)
      self.layout.removeItem(self.layouts[i])
  
  def delete_history_entry(self, i, entry_index):
    self.labels[i].setParent(None)
    self.delete_buttons[i].setParent(None)
    self.layout.removeItem(self.layouts[i])
    delete_history_entry(entry_index)
