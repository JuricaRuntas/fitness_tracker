from PyQt5.QtWidgets import (QWidget, QFrame, QFormLayout, QGridLayout,
                            QVBoxLayout, QLabel, QGroupBox, QRadioButton,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from .body_fat_calculator import BodyFatCalculator
from fitness_tracker.user_profile.profile_db import fetch_units, fetch_table_name
from fitness_tracker.config import get_db_paths

db_paths = get_db_paths("profile.db")

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.table_name = fetch_table_name(db_paths["profile.db"])
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_description(), 0, 0, 1, 2)
    grid.addLayout(self.create_calculator(), 1, 0, 1, 1)
    grid.addLayout(self.create_table(), 1, 1, 1, 1)
    self.setLayout(grid)

  def create_description(self):
    description_layout = QVBoxLayout()
    
    description_label = QLabel("Body Fat Calculator estimates your body fat percentage based on your measurements.", self)
    description_label.setFixedHeight(70)
    description_layout.addWidget(description_label)
    return description_layout

  def create_calculator(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()

    calculator_label = QLabel("Calculate your body fat", self)
    calculator_label.setFont(QFont("Ariel", 15))
    calculator_label.setFixedHeight(70)

    title_layout.addWidget(calculator_label)
    title_frame.setLayout(title_layout)
    
    calculator_frame = QFrame()
    calculator_frame.setFrameStyle(QFrame.StyledPanel)
    calculator_frame.setFixedWidth(300)
     
    table_name = fetch_table_name(db_paths["profile.db"])
    form_layout = self.create_form_metric() if fetch_units(db_paths["profile.db"]) == "metric" else self.create_form_imperial()
    calculator_frame.setLayout(form_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    return wrapper_layout

  def create_form_metric(self):
    self.calculator_layout = QFormLayout()
    
    gender_label = QLabel("Gender", self)
    
    gbox = QGroupBox()
    vbox = QHBoxLayout()
    vbox.setAlignment(Qt.AlignCenter)
    
    self.male_button = QRadioButton("male")
    self.male_button.setChecked(True)
    self.female_button = QRadioButton("female")
    
    self.male_button.toggled.connect(self.hide_or_show_hip)

    vbox.addWidget(self.male_button)
    vbox.addWidget(self.female_button)
    gbox.setLayout(vbox)

    age_label = QLabel("Age", self)
    self.age_entry = QLineEdit()
    
    weight_label = QLabel("Weight", self)
    self.weight_entry = QLineEdit()
    self.weight_entry.setPlaceholderText("kg")

    height_label = QLabel("Height", self)
    self.height_entry = QLineEdit()
    self.height_entry.setPlaceholderText("cm")

    neck_label = QLabel("Neck", self)
    self.neck_entry = QLineEdit()
    self.neck_entry.setPlaceholderText("cm")
    
    waist_label = QLabel("Waist", self)
    self.waist_entry = QLineEdit()
    self.waist_entry.setPlaceholderText("cm")

    self.calculate_button = QPushButton("Calculate", self)
    self.calculate_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.calculate_button.clicked.connect(self.calculate)

    self.calculator_layout.addRow(gender_label, gbox)
    self.calculator_layout.addRow(age_label, self.age_entry)
    self.calculator_layout.addRow(weight_label, self.weight_entry)
    self.calculator_layout.addRow(height_label, self.height_entry)
    self.calculator_layout.addRow(neck_label, self.neck_entry)
    self.calculator_layout.addRow(waist_label, self.waist_entry)
    self.calculator_layout.addRow(self.calculate_button)
    return self.calculator_layout
  
  def create_form_imperial(self):
    self.calculator_layout = QFormLayout()
    
    gender_label = QLabel("Gender", self)
    
    gbox = QGroupBox()
    vbox = QHBoxLayout()
    vbox.setAlignment(Qt.AlignCenter)
    
    self.male_button = QRadioButton("male")
    self.male_button.setChecked(True)
    self.female_button = QRadioButton("female")
    
    self.male_button.toggled.connect(self.hide_or_show_hip)

    vbox.addWidget(self.male_button)
    vbox.addWidget(self.female_button)
    gbox.setLayout(vbox)

    age_label = QLabel("Age", self)
    self.age_entry = QLineEdit()
    
    weight_label = QLabel("Weight", self)
    self.weight_entry = QLineEdit()
    self.weight_entry.setPlaceholderText("pounds")

    height_layout = QHBoxLayout()
    height_label = QLabel("Height", self)
    self.height_feet_entry = QLineEdit()
    self.height_feet_entry.setPlaceholderText("feet")
    self.height_inches_entry = QLineEdit()
    self.height_inches_entry.setPlaceholderText("inches")
    
    height_layout.addWidget(self.height_feet_entry)
    height_layout.addWidget(self.height_inches_entry)
    
    neck_layout = QHBoxLayout()
    neck_label = QLabel("Neck", self)
    self.neck_feet_entry = QLineEdit()
    self.neck_feet_entry.setPlaceholderText("feet")
    self.neck_inches_entry = QLineEdit()
    self.neck_inches_entry.setPlaceholderText("inches")
    
    neck_layout.addWidget(self.neck_feet_entry)
    neck_layout.addWidget(self.neck_inches_entry)
    
    waist_layout = QHBoxLayout()
    waist_label = QLabel("Waist", self)
    self.waist_feet_entry = QLineEdit()
    self.waist_feet_entry.setPlaceholderText("feet")
    self.waist_inches_entry = QLineEdit()
    self.waist_inches_entry.setPlaceholderText("inches")
    
    waist_layout.addWidget(self.waist_feet_entry)
    waist_layout.addWidget(self.waist_inches_entry)

    self.calculate_button = QPushButton("Calculate", self)
    self.calculate_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.calculate_button.clicked.connect(self.calculate)

    self.calculator_layout.addRow(gender_label, gbox)
    self.calculator_layout.addRow(age_label, self.age_entry)
    self.calculator_layout.addRow(weight_label, self.weight_entry)
    self.calculator_layout.addRow(height_label, height_layout)
    self.calculator_layout.addRow(neck_label, neck_layout)
    self.calculator_layout.addRow(waist_label, waist_layout)
    self.calculator_layout.addRow(self.calculate_button)

    return self.calculator_layout

  def hide_or_show_hip(self):
    units = fetch_units(db_paths["profile.db"])
    
    if self.female_button.isChecked():
      self.calculator_layout.removeWidget(self.calculate_button)
      self.calculate_button.deleteLater()
      
      self.calculate_button = QPushButton("Calculate", self)
      self.calculate_button.setCursor(QCursor(Qt.PointingHandCursor))
      self.calculate_button.clicked.connect(self.calculate)
      
      self.hip_label = QLabel("Hip", self)
      
      if units == "metric":
        self.hip_entry = QLineEdit()
        self.hip_entry.setPlaceholderText("cm")
        self.calculator_layout.addRow(self.hip_label, self.hip_entry)
      elif units == "imperial":
        self.hip_layout = QHBoxLayout()
        self.hip_feet_entry = QLineEdit()
        self.hip_feet_entry.setPlaceholderText("feet")
        self.hip_inches_entry = QLineEdit()
        self.hip_inches_entry.setPlaceholderText("inches")
        
        self.hip_layout.addWidget(self.hip_feet_entry)
        self.hip_layout.addWidget(self.hip_inches_entry)
        self.calculator_layout.addRow(self.hip_label, self.hip_layout)

      self.calculator_layout.addRow(self.calculate_button)
    else:
      if units == "metric":
        self.calculator_layout.removeWidget(self.hip_label)
        self.hip_label.deleteLater()
        self.calculator_layout.removeWidget(self.hip_entry)
        self.hip_entry.deleteLater()
      elif units == "imperial":
        self.calculator_layout.removeWidget(self.hip_label)
        self.hip_label.deleteLater()
        self.calculator_layout.removeWidget(self.hip_feet_entry)
        self.hip_feet_entry.deleteLater()
        self.calculator_layout.removeWidget(self.hip_inches_entry)
        self.hip_inches_entry.deleteLater()
  
  def create_table(self):
    frame = QFrame()
    table_layout = QVBoxLayout()

    frame.setLayout(table_layout)

    self.table = QTableWidget(7, 2)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers) 
    self.table.verticalHeader().setVisible(False)
    self.table.horizontalHeader().setVisible(False)
    
    rows = [["Body Fat (U.S. Navy Method)", ""],
            ["Body Fat Category", ""],
            ["Body Fat Mass", ""],
            ["Lean Body Mass", ""],
            ["Ideal Body Fat for Given Age (Jackson & Pollard)", ""],
            ["Body Fat to Lose to Reach Ideal", ""],
            ["Body Fat (BMI method)", ""]]
    
    i = j = 0
    for row in rows:
      item1 = QTableWidgetItem(row[0])
      item2 = QTableWidgetItem(row[1])
      item1.setTextAlignment(Qt.AlignCenter)
      item2.setTextAlignment(Qt.AlignCenter)
      self.table.setItem(i, 0, item1)
      self.table.setItem(j, 1, item2)
      i += 1
      j += 1
    
    for i in range(2):
      self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    for i in range(7):
      self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    grid = QGridLayout()
    grid.addWidget(frame, 0, 0)
    grid.addWidget(self.table, 1, 0)
    return grid

  def calculate(self):
    gender = "male" if self.male_button.isChecked() else "female"
    units = "kg" if fetch_units(db_paths["profile.db"]) == "metric" else "lbs"
    m = self.get_measurements()
    try:
      calc = BodyFatCalculator(m["Gender"], m["Age"], m["Weight"], m["Height"], m["Neck"], m["Waist"], m["Units"], m["Hip"])
      results = calc.get_results()
      self.set_results(results, units)
    except TypeError: # dict values are None
      pass
  
  def get_measurements(self):
    measurements = {}
    measurements["Gender"] = "male" if self.male_button.isChecked() else "female"
    units = fetch_units(db_paths["profile.db"])
    try:
      measurements["Age"] = int(self.age_entry.text())
      measurements["Weight"] = int(self.weight_entry.text())
      measurements["Units"] = units
      if units == "metric":
        measurements["Height"] = int(self.height_entry.text())
        measurements["Neck"] = int(self.neck_entry.text())
        measurements["Waist"] = int(self.waist_entry.text())
        try:
          measurements["Hip"] = int(self.hip_entry.text())
        except (AttributeError, RuntimeError): # hip entry might not exist
          measurements["Hip"] = None
      elif units == "imperial":
        measurements["Height"] = int(self.height_feet_entry.text())*12+float(self.height_inches_entry.text())
        measurements["Neck"] = int(self.neck_feet_entry.text())*12+float(self.neck_inches_entry.text())
        measurements["Waist"] = int(self.waist_feet_entry.text())*12+float(self.waist_inches_entry.text())
        try: measurements["Hip"] = int(self.hip_feet_entry.text())*12+float(self.hip_inches_entry.text())
        except (AttributeError, RuntimeError): measurements["Hip"] = None
      return measurements
    except ValueError: # values inside entries aren't numbers
      pass
  
  def set_results(self, results, units):
    if results["Body Fat Navy"] <= 0: return
    self.table.item(0, 1).setText("".join([str(results["Body Fat Navy"]), "%"]))
    self.table.item(1, 1).setText(str(results["Body Fat Category"]))
    self.table.item(2, 1).setText(" ".join([str(results["Fat Mass"]), units]))
    self.table.item(3, 1).setText(" ".join([str(results["Lean Body Mass"]), units]))
    self.table.item(4, 1).setText(str(results["Ideal Body Fat"]))
    self.table.item(5, 1).setText(" ".join([str(results["Body Fat To Lose To Reach Ideal"]), units]))
    self.table.item(6, 1).setText("".join([str(results["Body Fat BMI"]), "%"]))
