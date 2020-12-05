import json
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QComboBox
from PyQt5.QtGui import  QFont
from PyQt5.QtCore import pyqtSignal
from .big_lifts_db import fetch_preferred_lifts, update_preferred_lifts, update_1RM_and_lifts_for_reps

class PreferredLifts(QWidget):
  change_lifts_signal = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Edit Preferred Lifts")
    self.preferred_lifts = json.loads(fetch_preferred_lifts())
    self.setLayout(self.create_panel())
    self.set_preferred_lifts()
  
  def create_panel(self):
    form_layout = QFormLayout()

    horizontal_press_label = QLabel("Horizontal Press")
    self.horizontal_press_dropdown = QComboBox()
    self.horizontal_press_dropdown.addItems(["Bench Press", "Incline Bench Press"])

    floor_pull_label = QLabel("Floor Pull")
    self.floor_pull_dropdown = QComboBox()
    self.floor_pull_dropdown.addItems(["Deadlift", "Sumo Deadlift"])

    squat_label = QLabel("Squat")
    self.squat_dropdown = QComboBox()
    self.squat_dropdown.addItems(["Back Squat", "Front Squat"])

    vertical_press_label = QLabel("Vertical Press")
    self.vertical_press_dropdown = QComboBox()
    self.vertical_press_dropdown.addItems(["Overhead Press", "Push Press"])
    
    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: self.save_preferred_lifts())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())

    form_layout.addRow(horizontal_press_label, self.horizontal_press_dropdown)
    form_layout.addRow(floor_pull_label, self.floor_pull_dropdown)
    form_layout.addRow(squat_label, self.squat_dropdown)
    form_layout.addRow(vertical_press_label, self.vertical_press_dropdown)
    form_layout.addRow(save_button, cancel_button)
    return form_layout

  def set_preferred_lifts(self):
    horizontal_press_index = self.horizontal_press_dropdown.findText(self.preferred_lifts["Horizontal Press"])
    floor_pull_index = self.floor_pull_dropdown.findText(self.preferred_lifts["Floor Pull"])
    squat_index = self.squat_dropdown.findText(self.preferred_lifts["Squat"])
    vertical_press_index = self.vertical_press_dropdown.findText(self.preferred_lifts["Vertical Press"])

    self.horizontal_press_dropdown.setCurrentIndex(horizontal_press_index)
    self.floor_pull_dropdown.setCurrentIndex(floor_pull_index)
    self.squat_dropdown.setCurrentIndex(squat_index)
    self.vertical_press_dropdown.setCurrentIndex(vertical_press_index)

  def save_preferred_lifts(self):
    horizontal_press = str(self.horizontal_press_dropdown.currentText())
    floor_pull = str(self.floor_pull_dropdown.currentText())
    squat = str(self.squat_dropdown.currentText())
    vertical_press = str(self.vertical_press_dropdown.currentText())
    new_preferred_lifts = {"Horizontal Press": horizontal_press, "Floor Pull":floor_pull,
                           "Squat": squat, "Vertical Press": vertical_press}
    update_preferred_lifts(new_preferred_lifts)
    update_1RM_and_lifts_for_reps()
    self.change_lifts_signal.emit(True)
    self.close()
