import json
import os
from PyQt5.QtWidgets import (QSizePolicy, QWidget, QGridLayout, QFrame, QVBoxLayout, QFormLayout, QLineEdit,
                             QLabel, QPushButton, QGroupBox, QRadioButton, QHBoxLayout, QComboBox, QSpacerItem)
from PyQt5.QtGui import QFont, QCursor, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from fitness_tracker.notes.nutrition.calorie_goal_calculator import CalorieGoalCalculator
from fitness_tracker.database_wrapper import DatabaseWrapper

icon_path = os.path.join(os.path.dirname(__file__), os.path.pardir, "icons", "ftarizonacalligraphy.png")

class SignupQuestions(QWidget):
  display_layout_signal = pyqtSignal(str)

  def __init__(self, email, password):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      background-position: center;
      color: #D9D9D9;
      font-family: Montserrat;
      font-size: 14px;
    }
    QPushButton{
      border-radius: 1px;
      background-color: #440D0F;
    }
    QPushButton:hover:!pressed{
      background-color: #5D1A1D
    }
    QPushButton:pressed{
      background-color: #551812
    }    
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border-radius: 2px;
    }
    QComboBox{
      border-radius: 4px;
      font-size: 18px;
      font-weight: bold;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
      min-height: 28px;
      background-color: #440D0F;
    }
    QComboBox:down-arrow{
      width: 0px;
      height: 0px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
      width: 0px;
      height: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    """)
    self.db_wrapper = DatabaseWrapper()
    self.email = email
    self.password = password
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_login(), 0, 0, 1, 1)
    self.setLayout(grid)

  def create_login(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()

    signup_label = QLabel()
    pixmap = QPixmap(icon_path)
    signup_label.setPixmap(pixmap)
    signup_label.setAlignment(Qt.AlignCenter)

    title_layout.addWidget(signup_label)
    title_frame.setLayout(title_layout)

    form_layout = self.create_form_layout()
    form_layout.setAlignment(Qt.AlignCenter)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.setAlignment(Qt.AlignCenter)
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addLayout(form_layout)
    return wrapper_layout

  def create_form_layout(self):
    self.form_layout = QFormLayout()
    self.form_layout.setFormAlignment(Qt.AlignCenter)
    self.form_layout.setAlignment(Qt.AlignCenter)

    self.name_entry = QLineEdit()
    self.name_entry.setPlaceholderText("Name")
    self.name_entry.setFixedSize(300, 30)
    
    self.age_line_edit = QLineEdit()
    self.age_line_edit.setPlaceholderText("Age")
    self.age_line_edit.setFixedSize(300, 30)

    gender = QGroupBox()
    gender.setAlignment(Qt.AlignCenter)
    gender.setFixedSize(185, 40)
    gender_layout = QHBoxLayout()
    gender_layout.setAlignment(Qt.AlignCenter)

    gender_label = QLabel("Gender", self)
    gender_label.setAlignment(Qt.AlignCenter)
    gender_label.setFixedSize(115, 30)
    self.male_button = QRadioButton("Male")
    self.male_button.setChecked(True)
    self.female_button = QRadioButton("Female")
    gender_layout.addWidget(self.male_button)
    gender_layout.addWidget(self.female_button)
    gender.setLayout(gender_layout)
    
    units = QGroupBox()
    units.setAlignment(Qt.AlignCenter)
    units.setFixedSize(185, 40)
    units_layout = QHBoxLayout()
    units_layout.setAlignment(Qt.AlignCenter)

    units_label = QLabel("Units", self)
    units_label.setAlignment(Qt.AlignCenter)
    units_label.setFixedSize(115, 30)
    self.metric_button = QRadioButton("Metric")
    self.metric_button.setChecked(True)
    self.metric_button.toggled.connect(lambda: self.change_height_input())
    self.imperial_button = QRadioButton("Imperial")
    self.imperial_button.toggled.connect(lambda: self.change_height_input())
    units_layout.addWidget(self.metric_button)
    units_layout.addWidget(self.imperial_button)
    units.setLayout(units_layout)
    
    self.weight_entry = QLineEdit()
    self.weight_entry.setPlaceholderText("Weight")
    self.weight_entry.setFixedSize(300, 30)
    
    self.height_layout = QHBoxLayout()
    self.height_entry = QLineEdit()
    self.height_entry.setFixedSize(300, 30)
    self.height_entry.setPlaceholderText("Height")
    self.height_layout.addWidget(self.height_entry)

    self.form_layout.addRow(self.age_line_edit)
    self.form_layout.addRow(gender_label, gender)
    self.form_layout.addRow(units_label, units)
    self.form_layout.addRow(self.weight_entry)
    self.form_layout.addRow(self.height_layout)

    goal_label = QLabel("Goal", self)
    goal_label.setAlignment(Qt.AlignCenter)
    goal_label.setFixedSize(115, 30)
    goal_layout = QVBoxLayout()
    goal_layout.setAlignment(Qt.AlignCenter)
    goal = QGroupBox()
    goal.setAlignment(Qt.AlignCenter)
    goal.setFixedSize(185, 120)
    self.weight_loss_button = QRadioButton("Weight loss")
    self.weight_loss_button.setChecked(True)
    self.weight_loss_button.toggled.connect(lambda: self.hide_or_show_params_layout())

    self.maintain_weight_button = QRadioButton("Maintain weight")
    self.maintain_weight_button.toggled.connect(lambda: self.hide_or_show_params_layout())
    self.weight_gain_button = QRadioButton("Weight gain")
    self.weight_gain_button.toggled.connect(lambda: self.hide_or_show_params_layout())
    
    goal_layout.addWidget(self.weight_loss_button)
    goal_layout.addWidget(self.maintain_weight_button)
    goal_layout.addWidget(self.weight_gain_button)
    goal.setLayout(goal_layout)

    self.form_layout.addRow(goal_label, goal)
    
    self.params_label = QLabel("Goal Parameters:")
    self.params_label.setFixedWidth(300)
    self.params_layout = self.calorie_params_layout()
    self.form_layout.addRow(self.params_label)
    self.form_layout.addRow(self.params_layout)

    self.signup_button = QPushButton("Signup", self)
    self.signup_button.clicked.connect(lambda: self.signup())
    self.signup_button.setFixedSize(230, 30)
    self.signup_button.setCursor(QCursor(Qt.PointingHandCursor))
    
    self.form_layout.addRow(self.signup_button)

    return self.form_layout

  def change_height_input(self):
    if self.imperial_button.isChecked():
      try:
        if self.height_entry2 == None: self.height_entry2 = QLineEdit()
        self.height_layout.addWidget(self.height_entry2)
      
      except (AttributeError, RuntimeError):
        self.height_entry2 = QLineEdit()
        self.height_layout.addWidget(self.height_entry2)

    else:
      self.height_entry2.setParent(None)
      self.height_entry2.deleteLater()
  
  def hide_or_show_params_layout(self):
    if self.maintain_weight_button.isChecked():
      self.signup_button.setParent(None)
      self.delete_layout(self.params_layout)
      self.form_layout.addRow(self.signup_button)
    else:
      if not self.params_layout == None:
        self.signup_button.setParent(None)
        self.params_label.setParent(None)
        self.delete_layout(self.params_layout)
        self.params_label = QLabel("Goal parameters")
        self.params_layout = self.calorie_params_layout()
        self.form_layout.addRow(self.params_label, self.params_layout)
        self.form_layout.addRow(self.signup_button)

  def delete_layout(self, layout):
    if layout is not None:
      while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
          widget.setParent(None)
        else:
          self.delete_layout(item.layout())

  def calorie_params_layout(self):
    params_layout = QVBoxLayout()
    
    goal_weight_layout = QVBoxLayout()
    #goal_weight_label = QLabel("Goal weight")
    self.goal_weight_line_edit = QLineEdit()
    self.goal_weight_line_edit.setPlaceholderText("Goal Weight")
    self.goal_weight_line_edit.setFixedSize(300, 30)

    #goal_weight_layout.addWidget(goal_weight_label)
    goal_weight_layout.addWidget(self.goal_weight_line_edit)
    
    activity_level_layout = QHBoxLayout()
    activity_level_label = QLabel("Activity Level:")
    activity_level_label.setFixedSize(120, 30)
    self.activity_level = QComboBox()
    self.activity_level.addItems(["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])
    self.activity_level.setFixedSize(180, 30)

    activity_level_layout.addWidget(activity_level_label)
    activity_level_layout.addWidget(self.activity_level)
    
    weight_per_week_layout = QHBoxLayout()
    weight_per_week_label = QLabel("Weight/Week (kg):")
    weight_per_week_label.setFixedSize(160, 30)
    self.weight_per_week = QComboBox()
    self.weight_per_week.setFixedSize(140, 30)
    self.weight_per_week.addItems(["0.25", "0.5", "1"])
    
    weight_per_week_layout.addWidget(weight_per_week_label)
    weight_per_week_layout.addWidget(self.weight_per_week)

    params_layout.addLayout(goal_weight_layout)
    params_layout.addLayout(activity_level_layout)
    params_layout.addLayout(weight_per_week_layout)
    
    return params_layout

  def signup(self):
    try:
      age = str(int(self.age_line_edit.text()))
      gender = "male" if self.male_button.isChecked() else "female"
      units = "metric" if self.metric_button.isChecked() else "imperial"
      height = json.dumps([float(self.height_entry.text()),
                           float(self.height_entry2.text())]) if units == "imperial" else str(float(self.height_entry.text()))
      if self.weight_loss_button.isChecked():
        goal = "Weight loss"
      elif self.maintain_weight_button.isChecked():
        goal = "Maintain weight"
      elif self.weight_gain_button.isChecked():
        goal = "Weight gain"
      goal_params = json.dumps([self.activity_level.currentText(),
                                float(self.weight_per_week.currentText())]) if not goal == "Maintain weight" else json.dumps(["Maintain", 0])
      weight = str(float(self.weight_entry.text()))
      goal_weight = str(float(self.goal_weight_line_edit.text()))
      user_info = {"name": self.name_entry.text(),
                   "age": age,
                   "gender": gender,
                   "units": units,
                   "weight": weight,
                   "height": height,
                   "goal": goal,
                   "goalparams": goal_params,
                   "goalweight": goal_weight}
    except ValueError:
      return
    
    if not gender == "" and not units == "" and not self.name_entry.text() == "" and not self.weight_entry.text() == "":
      goal_params = json.loads(goal_params)
      self.db_wrapper.create_user(self.email, self.password)
      self.db_wrapper.create_user_table(self.email, self.password)
      self.db_wrapper.create_user_info_after_signup(user_info)
      calorie_goal_calculator = CalorieGoalCalculator(int(age), gender, float(height),
                                                      float(weight), goal_params[0], goal, goal_params[1])
      calorie_goal = calorie_goal_calculator.calculate_calorie_goal()
      self.db_wrapper.insert_default_values("Nutrition", calorie_goal=calorie_goal)
      self.display_layout_signal.emit("Compound Exercises")
