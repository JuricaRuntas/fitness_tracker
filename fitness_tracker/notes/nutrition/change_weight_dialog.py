import json
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
                             QFormLayout, QLineEdit, QComboBox, QRadioButton, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from fitness_tracker.user_profile.profile_db import (fetch_user_weight, fetch_goal_weight, fetch_goal,
                                                     fetch_age, fetch_gender, fetch_height, fetch_goal_params,
                                                     update_weight, update_goal, update_goal_parameters,
                                                     update_goal_weight)
from .nutrition_db import update_calorie_goal
from .calorie_goal_calculator import CalorieGoalCalculator

class ChangeWeightDialog(QWidget):
  change_current_weight_signal = pyqtSignal(str)
  change_goal_weight_signal = pyqtSignal(str)
  change_calorie_goal_signal = pyqtSignal(str)

  def __init__(self):
    super().__init__()
    self.user_weight = fetch_user_weight()
    self.goal_weight = fetch_goal_weight()
    goal_parameters = json.loads(fetch_goal_params())
    self.goal = fetch_goal()
    self.activity_level = goal_parameters[0]
    self.weight_per_week = goal_parameters[1]
    self.age = fetch_age()
    self.gender = fetch_gender()
    self.height = fetch_height()
    self.setWindowTitle("Edit weight")
    self.create_layout()
    
  def create_layout(self):
    layout = QFormLayout()

    current_weight_label = QLabel("Current weight")
    self.current_weight_line_edit = QLineEdit()
    self.current_weight_line_edit.setText(self.user_weight)
    
    goal_label = QLabel("Goal")
    goal_layout = QHBoxLayout()
    goal = QGroupBox()
    self.weight_loss_button = QRadioButton("Weight loss")
    self.maintain_weight_button = QRadioButton("Maintain weight")
    self.weight_gain_button = QRadioButton("Weight gain")
    if self.goal == "Weight loss": self.weight_loss_button.setChecked(True)
    elif self.goal == "Maintain weight": self.maintain_weight_button.setChecked(True)
    elif self.goal == "Weight gain": self.weight_gain_button.setChecked(True)
    goal_layout.addWidget(self.weight_loss_button)
    goal_layout.addWidget(self.maintain_weight_button)
    goal_layout.addWidget(self.weight_gain_button)
    goal.setLayout(goal_layout)

    goal_parameters_label = QLabel("Goal parameters")
    goal_parameters_layout = QHBoxLayout()

    activity_level_layout = QVBoxLayout()
    activity_level_label = QLabel("Activity level")
    self.activity_level_cb = QComboBox()
    self.activity_level_cb.addItems(["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])
    self.activity_level_cb.setCurrentText(self.activity_level)
    activity_level_layout.addWidget(activity_level_label)
    activity_level_layout.addWidget(self.activity_level_cb)
    
    weight_per_week_layout = QVBoxLayout()
    weight_per_week_label = QLabel("Weight to lose/gain per week (kg)")
    self.weight_per_week_cb = QComboBox()
    self.weight_per_week_cb.addItems(["0.25", "0.5", "1"])
    self.weight_per_week_cb.setCurrentText(str(self.weight_per_week))
    weight_per_week_layout.addWidget(weight_per_week_label)
    weight_per_week_layout.addWidget(self.weight_per_week_cb)
    
    goal_parameters_layout.addLayout(activity_level_layout)
    goal_parameters_layout.addLayout(weight_per_week_layout)

    goal_weight_label = QLabel("Goal weight")
    self.goal_weight_line_edit = QLineEdit()
    self.goal_weight_line_edit.setText(self.goal_weight)

    save_changes_button = QPushButton("Save changes")
    save_changes_button.clicked.connect(lambda: self.save_changes())
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(lambda: self.close())

    layout.addRow(current_weight_label, self.current_weight_line_edit)
    layout.addRow(goal_label, goal)
    layout.addRow(goal_parameters_label, goal_parameters_layout)
    layout.addRow(goal_weight_label, self.goal_weight_line_edit)
    layout.addRow(save_changes_button, cancel_button)
    self.setLayout(layout)

  def save_changes(self):
    current_weight = str(float(self.current_weight_line_edit.text()))
    if self.weight_loss_button.isChecked():
      goal = "Weight loss"
    elif self.maintain_weight_button.isChecked():
      goal = "Maintain weight"
    elif self.weight_gain_button.isChecked():
      goal = "Weight gain"
    goal_params = [self.activity_level_cb.currentText(), float(self.weight_per_week_cb.currentText())]
    goal_weight = str(float(self.goal_weight_line_edit.text()))

    try:
      if not current_weight == self.user_weight:
        update_weight(str(float(current_weight)))
        self.user_weight = current_weight
        self.change_current_weight_signal.emit(current_weight)
        self.current_weight_line_edit.setText(current_weight)
      if not goal == self.goal:
        update_goal(goal)
        self.goal = goal
        if goal == "Weight loss":
          self.weight_loss_button.setChecked(True)
        elif goal == "Maintain weight":
          self.maintain_weight_button.setChecked(True)
        elif goal == "Weight gain":
          self.weight_gain_button.setChecked(True)
      if not goal_params[0] == self.activity_level or not goal_params[1] == self.weight_per_week:
        update_goal_parameters(json.dumps(goal_params))
        self.activity_level = goal_params[0]
        self.weight_per_week = goal_params[1]
      if not goal_weight == self.goal_weight:
        update_goal_weight(goal_weight)
        self.goal_weight = goal_weight
        self.change_goal_weight_signal.emit(goal_weight)
        self.goal_weight_line_edit.setText(goal_weight)
      
      calculator = CalorieGoalCalculator(int(self.age), self.gender, float(self.height), float(self.user_weight), goal_params[0], goal, goal_params[1])
      calorie_goal = calculator.calculate_calorie_goal()
      update_calorie_goal(calorie_goal)
      self.change_calorie_goal_signal.emit(str(calorie_goal))
      self.close()
    except ValueError:
      pass
