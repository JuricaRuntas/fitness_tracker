from PyQt5.QtWidgets import (QWidget, QFrame, QFormLayout, QGridLayout,
                            QVBoxLayout, QLabel, QGroupBox, QRadioButton,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

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

    calculator_layout = QFormLayout()
    
    gender_label = QLabel("Gender", self)
    
    gbox = QGroupBox()
    vbox = QHBoxLayout()
    vbox.setAlignment(Qt.AlignCenter)
    
    male_button = QRadioButton("male")
    male_button.setChecked(True)

    female_button = QRadioButton("female")

    vbox.addWidget(male_button)
    vbox.addWidget(female_button)
    gbox.setLayout(vbox)

    age_label = QLabel("Age", self)
    line_edit = QLineEdit()

    weight_label = QLabel("Weight", self)
    line_edit1 = QLineEdit()

    height_label = QLabel("Height", self)
    line_edit2 = QLineEdit()

    neck_label = QLabel("Neck", self)
    line_edit3 = QLineEdit()
    
    waist_label = QLabel("Waist", self)
    line_edit4 = QLineEdit()

    hip_label = QLabel("Hip", self)
    line_edit5 = QLineEdit()
    
    calculate_button = QPushButton("Calculate", self)

    calculator_layout.addRow(gender_label, gbox)
    calculator_layout.addRow(age_label, line_edit)
    calculator_layout.addRow(weight_label, line_edit1)
    calculator_layout.addRow(height_label, line_edit2)
    calculator_layout.addRow(neck_label, line_edit3)
    calculator_layout.addRow(waist_label, line_edit4)
    calculator_layout.addRow(hip_label, line_edit5)
    calculator_layout.addRow(calculate_button)
    
    calculator_frame.setLayout(calculator_layout)

    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    return wrapper_layout

  def create_table(self):
    frame = QFrame()
    table_layout = QVBoxLayout()

    frame.setLayout(table_layout)

    table = QTableWidget(7, 2)
  
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setVisible(False)
    
    rows = [["Body Fat (U.S. Navy Method)", "15.7%"],
            ["Body Fat Category", "Fitness"],
            ["Body Fat Mass", "11.0 kgs"],
            ["Lean Body Mass", "59.0 kgs"],
            ["Ideal Body Fat for Given Age (Jackson & Pollard)", "10.5%"],
            ["Body Fat to Lose to Reach Ideal", "3.6 kgs"],
            ["Body Fat (BMI method)", "16.1%"]]
    
    i = j = 0
    for row in rows:
      item1 = QTableWidgetItem(row[0])
      item2 = QTableWidgetItem(row[1])
      item1.setTextAlignment(Qt.AlignCenter)
      item2.setTextAlignment(Qt.AlignCenter)
      table.setItem(i, 0, item1)
      table.setItem(j, 1, item2)
      i += 1
      j += 1
    
    for i in range(2):
      table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    for i in range(7):
      table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    grid = QGridLayout()
    grid.addWidget(frame, 0, 0)
    grid.addWidget(table, 1, 0)
    return grid
