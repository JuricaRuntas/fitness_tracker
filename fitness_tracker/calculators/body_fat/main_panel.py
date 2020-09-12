from PyQt5.QtWidgets import (QWidget, QFrame, QFormLayout, QGridLayout,
                            QVBoxLayout, QLabel, QGroupBox, QRadioButton,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from .calculator import BodyFatCalculator

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
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

    height_label = QLabel("Height", self)
    self.height_entry = QLineEdit()

    neck_label = QLabel("Neck", self)
    self.neck_entry = QLineEdit()
    
    waist_label = QLabel("Waist", self)
    self.waist_entry = QLineEdit()

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
    
    calculator_frame.setLayout(self.calculator_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    return wrapper_layout

  def hide_or_show_hip(self):
    if self.female_button.isChecked():
      self.calculator_layout.removeWidget(self.calculate_button)
      self.calculate_button.deleteLater()
      
      self.hip_label = QLabel("Hip", self)
      self.hip_entry = QLineEdit()
      
      self.calculate_button = QPushButton("Calculate", self)
      self.calculate_button.setCursor(QCursor(Qt.PointingHandCursor))
      self.calculate_button.clicked.connect(self.calculate)

      self.calculator_layout.addRow(self.hip_label, self.hip_entry)
      self.calculator_layout.addRow(self.calculate_button)
    else:
      self.calculator_layout.removeWidget(self.hip_label)
      self.hip_label.deleteLater()
      self.calculator_layout.removeWidget(self.hip_entry)
      self.hip_entry.deleteLater()
  
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
    try:
      age = int(self.age_entry.text())
      weight = int(self.weight_entry.text())
      height = int(self.height_entry.text())
      neck = int(self.neck_entry.text())
      waist = int(self.waist_entry.text())
      units = "metric"  # this should be fetched from database
      try: hip = int(self.hip_entry.text())
      except (AttributeError, RuntimeError): hip = None
      calc = BodyFatCalculator(gender, age, weight, height, neck, waist, units, hip)
      results = calc.get_results()
      self.table.item(0, 1).setText("".join([str(results["Body Fat Navy"]), "%"]))
      self.table.item(1, 1).setText(str(results["Body Fat Category"]))
      self.table.item(2, 1).setText(str(results["Fat Mass"]))
      self.table.item(3, 1).setText(str(results["Lean Body Mass"]))
      self.table.item(4, 1).setText(str(results["Ideal Body Fat"]))
      self.table.item(5, 1).setText(str(results["Body Fat To Lose To Reach Ideal"]))
      self.table.item(6, 1).setText("".join([str(results["Body Fat BMI"]), "%"]))
    except ValueError:
      pass
