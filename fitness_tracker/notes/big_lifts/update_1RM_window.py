import json
import os
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from .big_lifts_db import (fetch_preferred_lifts, fetch_one_rep_maxes, lift_difference,
                           update_lift_history, update_1RM_lifts, update_one_rep_maxes_history)
from fitness_tracker.user_profile.profile_db import fetch_units

class Update1RMWindow(QWidget):
  change_1RM_lifts_signal = pyqtSignal(bool)
  history_signal = pyqtSignal(bool)
  update_graph_signal = pyqtSignal(bool)
  currently_selected_year_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.currently_selected_year = None
    self.units = "kg" if fetch_units() == "metric" else "lb"
    self.preferred_lifts = json.loads(fetch_preferred_lifts())
    self.setWindowTitle("Update One Rep Max Lifts")
    self.setLayout(self.create_panel())
    self.set_line_edit_values()

  def create_panel(self):
    form_layout = QFormLayout()

    exercise_label = QLabel("Exercise")
    weight_label = QLabel("Weight")
    
    horizontal_press_label = QLabel(self.preferred_lifts["Horizontal Press"])
    self.horizontal_press_edit = QLineEdit()
    units_label = QLabel(self.units)
    hbox = QHBoxLayout()
    hbox.addWidget(self.horizontal_press_edit)
    hbox.addWidget(units_label)

    floor_pull_label = QLabel(self.preferred_lifts["Floor Pull"])
    self.floor_pull_edit = QLineEdit()
    units_label1 = QLabel(self.units)
    hbox1 = QHBoxLayout()
    hbox1.addWidget(self.floor_pull_edit)
    hbox1.addWidget(units_label1)

    squat_label = QLabel(self.preferred_lifts["Squat"])
    self.squat_edit = QLineEdit()
    units_label2 = QLabel(self.units)
    hbox2 = QHBoxLayout()
    hbox2.addWidget(self.squat_edit)
    hbox2.addWidget(units_label2)

    vertical_press_label = QLabel(self.preferred_lifts["Vertical Press"])
    self.vertical_press_edit = QLineEdit()
    units_label3 = QLabel(self.units)
    hbox3 = QHBoxLayout()
    hbox3.addWidget(self.vertical_press_edit)
    hbox3.addWidget(units_label3)

    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_1RM_lifts())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close_update_1RM())

    form_layout.addRow(exercise_label, weight_label)
    form_layout.addRow(horizontal_press_label, hbox)
    form_layout.addRow(floor_pull_label, hbox1)
    form_layout.addRow(squat_label, hbox2)
    form_layout.addRow(vertical_press_label, hbox3)
    form_layout.addRow(save_button, cancel_button)
    return form_layout

  def save_1RM_lifts(self):
    try:
      exercises = list(json.loads(fetch_one_rep_maxes()).keys())
      horizontal_press_max = str(float(self.horizontal_press_edit.text()))
      floor_pull_max = str(float(self.floor_pull_edit.text()))
      squat_max = str(float(self.squat_edit.text()))
      vertical_press_max = str(float(self.vertical_press_edit.text()))
      new_maxes = {exercises[0]:horizontal_press_max, exercises[1]:floor_pull_max,
                   exercises[2]:squat_max, exercises[3]:vertical_press_max}
      
      diff = lift_difference(new_maxes, one_RM=True)
      
      update_lift_history(diff) 
      self.history_signal.emit(True)
      
      update_1RM_lifts(new_maxes)
      self.currently_selected_year_signal.emit(True)
      update_one_rep_maxes_history(new_maxes, self.currently_selected_year)
      
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
    one_rep_maxes = list(json.loads(fetch_one_rep_maxes()).values())
    self.horizontal_press_edit.setText(one_rep_maxes[0])
    self.floor_pull_edit.setText(one_rep_maxes[1])
    self.squat_edit.setText(one_rep_maxes[2])
    self.vertical_press_edit.setText(one_rep_maxes[3])
  
  def get_year(self, year):
    self.currently_selected_year = year
