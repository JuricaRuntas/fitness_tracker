from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt
from .one_rep_max_calculator import OneRepMaxCalculator
from fitness_tracker.user_profile.profile_db import fetch_units, fetch_table_name
from fitness_tracker.config import get_db_paths

db_paths = get_db_paths("profile.db")

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_description(), 0, 0, 1, 2)
    grid.addLayout(self.create_calculator(), 1, 0, 1, 1)
    grid.addLayout(self.create_progression(), 1, 1, 2, 1)
    self.setLayout(grid)

  def create_description(self):
    description_layout = QVBoxLayout()

    description_label = QLabel(""" One Rep Max calculator can calculate your estimated maximum repetitions based on your recent heavy lift. 
 Calculator will also show suggested progression towards that one rep max. """, self)
    description_label.setStyleSheet("border: 1px solid black;")
    description_label.setFixedHeight(70)
    description_layout.addWidget(description_label)

    return description_layout

  def create_calculator(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()
    
    calculator_label = QLabel("Calculate your one rep max", self)
    calculator_label.setFont(QFont("Ariel", 15))

    title_layout.addWidget(calculator_label)
    title_frame.setLayout(title_layout)
    
    calculator_layout = QVBoxLayout()
    
    calculator_frame = QFrame()
    calculator_frame.setFrameStyle(QFrame.StyledPanel)
    calculator_frame.setFixedWidth(300) 
    
    weight_label = QLabel("Weight", self)
    self.weight_entry = QLineEdit()
    
    reps_label = QLabel("Repetitions", self)
    self.reps_entry = QLineEdit()
    
    calculate_button = QPushButton("Calculate", self)
    calculate_button.setCursor(QCursor(Qt.PointingHandCursor))
    calculate_button.clicked.connect(self.calculate)

    calculator_layout.addWidget(weight_label)
    calculator_layout.addWidget(self.weight_entry)
    calculator_layout.addWidget(reps_label)
    calculator_layout.addWidget(self.reps_entry)
    calculator_layout.addWidget(calculate_button)
    
    calculator_frame.setLayout(calculator_layout)
    
    self.result_label = QLabel(self)
    
    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    wrapper_layout.addWidget(self.result_label)
    
    return wrapper_layout

  def create_progression(self):
    frame = QFrame()
    progression_layout = QVBoxLayout()
    
    progression_label = QLabel("Progression to your max", self)
    progression_label.setAlignment(Qt.AlignCenter)
    progression_label.setFont(QFont("Ariel", 15))

    progression_layout.addWidget(progression_label)
    frame.setLayout(progression_layout)
    
    self.table = QTableWidget(7,5)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.table.verticalHeader().setVisible(False)
    
    table_items = {"table_headers": ["Set", "%", "Weight", "Reps", "Rest"], 
                   "sets": ["1", "2", "3", "4", "5", "6", "7", "8"],
                   "percentages": ["~30%-50%", "~60%", "~70", "~80%", "~90%", "~100%", "~102%"],
                   "weight": [""]*7,
                   "number_of_reps": ["8", "5", "3", "1", "1", "1", "1"],
                   "rest": ["~2 min", "~2 min", "~3 min", "~3 min", "~5 min", "~5-15 min", "~5-15 min"]}
    
    for key, value in table_items.items():
      for i, item in enumerate(value):
        if key == "table_headers":
          self.table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
          self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        else:
          _item = QTableWidgetItem(item)
          _item.setTextAlignment(Qt.AlignCenter)
          if key == "sets": self.table.setItem(i, 0, _item)
          elif key == "percentages": self.table.setItem(i, 1, _item)
          elif key == "weight": self.table.setItem(i, 2, _item)
          elif key == "number_of_reps": self.table.setItem(i, 3, _item)
          elif key == "rest": self.table.setItem(i, 4, _item)

    for i in range(7):
      self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    grid = QGridLayout()
    grid.addWidget(frame, 0, 0)
    grid.addWidget(self.table, 1, 0, 1, 1)
    return grid

  def calculate(self):
    try:
      table_name = fetch_table_name(db_paths["profile.db"])
      units = fetch_units(db_paths["profile.db"])
      weight = self.weight_entry.text()
      repetitions = self.reps_entry.text()
      units = "kg" if units == "metric" else "lb"
      
      calc = OneRepMaxCalculator(weight, repetitions)
      results = calc.results()
      self.result_label.setText("".join(["Your estimated one rep max is: ", str(results[5]), " ", units]))
      j = 0
      for i in range(7):
        self.table.item(i, 2).setText("".join([str(results[j]), " ", units]))
        j += 1
    except ValueError:
      pass
