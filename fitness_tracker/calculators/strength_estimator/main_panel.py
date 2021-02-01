from PyQt5.QtWidgets import (QPushButton, QLabel, QComboBox, QLineEdit, QGridLayout, QWidget,
                             QVBoxLayout, QHBoxLayout, QRadioButton, QScrollArea, QTableWidget,
                             QTableWidgetItem, QAbstractItemView, QFrame, QFormLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fitness_tracker.user_profile.profile_db import fetch_units
from .estimator import StrengthLevelEstimator
from .exercise_standards import LiftStandards

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.setStyleSheet("""
    QWidget{
      font-family: Montserrat;
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
    }
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border-radius: 2px;
    }
    QTableWidget{
      background-color: rgb(33,33,33);  
      border: 1px solid;
      border-color: rgb(88, 88, 88);
      font-size: 14px;
    }
    QHeaderView:section{
      background-color: rgb(54,54,54);  
      border: 1px solid;
      border-color: rgb(88, 88, 88)
    }""")
    self.units = "kg" if fetch_units() == "metric" else "lb"
    self.CreatePanel()

  def CreatePanel(self):
    main_panel_layout = QGridLayout()
    main_panel_layout.addLayout(self.description(), 0, 0, 1, 1)
    main_panel_layout.addWidget(self.calculator(), 2, 0, 2, 1)
    main_panel_layout.addLayout(self.strength_standards(), 6, 0, 4, 1)
    self.setLayout(main_panel_layout)

  def description(self):
    description_layout = QVBoxLayout()
    description_label = QLabel("Take a quick test and see where you are standing compared to other lifters.")
    description_label.setFixedHeight(30)
    description_layout.addWidget(description_label)

    return description_layout

  def calculator(self):
    calculator_framed = QFrame()
    calculator_layout = QHBoxLayout()
    data_layout = QFormLayout()
    print_layout = QVBoxLayout()
    
    gender_age_label = QLabel("Gender/Age")
    gender_age_label.setFont(QFont("Ariel", 10))
    self.gender_combobox = QComboBox(self)
    self.gender_combobox.addItems(["Male", "Female"])
    self.age_combobox = QComboBox(self)
    self.age_combobox.addItems(["14-17", "18-23", "24-39", "40-49", "50-59", "60-69", "70-79", "80-89"]) 
    
    gender_age_layout = QHBoxLayout()
    gender_age_layout.addWidget(self.gender_combobox)
    gender_age_layout.addWidget(self.age_combobox)

    bodyweight_layout = QHBoxLayout()
    units_label = QLabel(self.units)
    bodyweight_label = QLabel("Bodyweight")
    bodyweight_label.setFont(QFont("Ariel", 10))
    self.bodyweight_line_edit = QLineEdit()
    bodyweight_layout.addWidget(self.bodyweight_line_edit)
    bodyweight_layout.addWidget(units_label)
    
    exercise_label = QLabel("Exercise")
    exercise_label.setFont(QFont("Ariel", 10))
    self.exercise_combobox = QComboBox()
    self.exercise_combobox.addItems(["Bench Press", "Deadlift", "Squat"])

    weight_layout = QHBoxLayout()
    units_label1 = QLabel(self.units)
    weight_label = QLabel("Weight")
    weight_label.setFont(QFont("Ariel", 10))
    self.weight_line_edit = QLineEdit()
    weight_layout.addWidget(self.weight_line_edit)
    weight_layout.addWidget(units_label1)
    
    self.calculate_button = QPushButton("Calculate strength")
    self.calculate_button.clicked.connect(lambda: self.calculate())
    
    data_layout.addRow(gender_age_label, gender_age_layout)
    data_layout.addRow(bodyweight_label, bodyweight_layout)
    data_layout.addRow(exercise_label, self.exercise_combobox)
    data_layout.addRow(weight_label, weight_layout)
    data_layout.addRow(self.calculate_button)

    strength_estimator_exercise_label = QLabel("Your strength level for deadlift is")
    strength_estimator_exercise_label.setFont(QFont("Ariel", 14))

    self.strength_level_exercise_label = QLabel()
    self.strength_level_exercise_label.setFont(QFont("Ariel", 14))

    self.strength_to_bodyweight_label = QLabel()
    self.strength_to_bodyweight_label.setFont(QFont("Ariel", 14))

    print_layout.addWidget(strength_estimator_exercise_label)
    print_layout.addWidget(self.strength_level_exercise_label)
    print_layout.addWidget(self.strength_to_bodyweight_label)

    framed_data_layout = QFrame()
    framed_data_layout.setFrameStyle(QFrame.StyledPanel)
    framed_data_layout.setLayout(data_layout)

    calculator_layout.addWidget(framed_data_layout)
    calculator_layout.addLayout(print_layout)

    calculator_framed.setFrameStyle(QFrame.StyledPanel)
    calculator_framed.setLayout(calculator_layout)

    return calculator_framed

  def calculate(self):
    try:
      gender = self.gender_combobox.currentText()
      age = self.age_combobox.currentText()
      bodyweight = float(self.bodyweight_line_edit.text())
      exercise = self.exercise_combobox.currentText()
      weight = float(self.weight_line_edit.text())
      estimator = StrengthLevelEstimator(gender, age, bodyweight, exercise, weight, self.units)
      strength_group = estimator.find_strength_group()
      self.strength_level_exercise_label.setText(strength_group)

      lift_weight_ratio = estimator.lift_weight_ratio()
      self.strength_to_bodyweight_label.setText(" ".join(["Your lift is", str(lift_weight_ratio), "times your bodyweight."]))
    except ValueError: # user submitted text in bodyweight or weight line edit
      pass

  def strength_standards(self):
    strength_standards_layout = QVBoxLayout()
    standards_label = QLabel("Strength Standards")
    standards_label.setFont(QFont("Ariel", 18))
    strength_standards_layout.addWidget(standards_label)

    standards_info_layout = QHBoxLayout()
    self.male_button = QRadioButton("Male")
    self.male_button.setChecked(True)
    self.male_button.toggled.connect(self.update_standards_table)
    standards_info_layout.addWidget(self.male_button)
    self.female_button = QRadioButton("Female")
    self.female_button.toggled.connect(self.update_standards_table)
    standards_info_layout.addWidget(self.female_button)

    self.table_age_combobox = QComboBox(self)
    self.table_age_combobox.addItems(["14-17", "18-23", "24-39", "40-49", "50-59", "60-69", "70-79", "80-89"])
    self.table_age_combobox.activated[str].connect(self.update_standards_table)
    self.table_age_combobox.setFixedWidth(80)
    self.table_exercise_combobox = QComboBox()
    self.table_exercise_combobox.addItems(["Bench Press", "Deadlift", "Squat"])
    self.table_exercise_combobox.setFixedWidth(120)
    self.table_exercise_combobox.activated[str].connect(self.update_standards_table)
    standards_info_layout.addWidget(self.table_age_combobox)
    standards_info_layout.addWidget(self.table_exercise_combobox)
    standards_info_layout.addStretch(1)
    standards_info_layout.setSpacing(10)

    strength_standards_layout.addLayout(standards_info_layout)
    strength_standards_layout.addWidget(self.create_standards_table())
    
    return strength_standards_layout

  def create_standards_table(self):
    standards_table_scroll_area = QScrollArea()

    self.standards_table = QTableWidget()
    self.standards_table.setRowCount(20)
    self.standards_table.setColumnCount(6)
    self.standards_table.horizontalHeader().setVisible(False)
    self.standards_table.verticalHeader().setVisible(False)
    
    exercise = self.table_exercise_combobox.currentText()
    age_range = self.table_age_combobox.currentText()
    gender = "Male" if self.male_button.isChecked() else "Female"
    fetch_standard = LiftStandards(exercise, age_range, gender, self.units).standard()
    standards_table_info = [fetch_standard[0]]
    for standard in fetch_standard[1:]:
      standards_table_info.append(list(map(str, standard)))
    
    currentRow = 0
    for row in standards_table_info:
      currentColumn = 0
      for item in row:
        table_item = QTableWidgetItem(item)
        table_item.setFlags(Qt.ItemIsEnabled)
        self.standards_table.setItem(currentRow, currentColumn, table_item)
        currentColumn += 1
      currentRow += 1

    standards_table_scroll_area.setWidget(self.standards_table)
    standards_table_scroll_area.setWidgetResizable(True)

    return standards_table_scroll_area

  def update_standards_table(self):
    exercise = self.table_exercise_combobox.currentText()
    age_range = self.table_age_combobox.currentText()
    gender = "Male" if self.male_button.isChecked() else "Female"
    fetch_standard = LiftStandards(exercise, age_range, gender, self.units).standard()
    standards_table_info = [fetch_standard[0]]
    for standard in fetch_standard[1:]:
      standards_table_info.append(list(map(str, standard)))
    
    currentRow = 0
    for row in standards_table_info:
      currentColumn = 0
      for item in row:
        table_item = QTableWidgetItem(item)
        table_item.setFlags(Qt.ItemIsEnabled)
        self.standards_table.setItem(currentRow, currentColumn, table_item)
        currentColumn += 1
      currentRow += 1
