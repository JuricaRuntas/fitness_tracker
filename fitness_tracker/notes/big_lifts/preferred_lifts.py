from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QFormLayout, QComboBox
from PyQt5.QtGui import  QFont

class PreferredLifts(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Edit Preferred Lifts")
    self.setLayout(self.create_panel())

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
    cancel_button = QPushButton("Cancel")

    form_layout.addRow(horizontal_press_label, self.horizontal_press_dropdown)
    form_layout.addRow(floor_pull_label, self.floor_pull_dropdown)
    form_layout.addRow(squat_label, self.squat_dropdown)
    form_layout.addRow(vertical_press_label, self.vertical_press_dropdown)
    form_layout.addRow(save_button, cancel_button)
    return form_layout

  def fetch_current_exercises(self):
    horizontal_press = str(self.horizontal_press_dropdown.currentText())
    floor_pull = str(self.floor_pull_dropdown.currentText())
    squat = str(self.squat_dropdown.currentText())
    vertical_press = str(self.vertical_press_dropdown.currentText())
    return [horizontal_press, floor_pull, squat, vertical_press]
