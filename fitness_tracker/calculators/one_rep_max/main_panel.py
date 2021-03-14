from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout)
from PyQt5.QtGui import QFont, QCursor, QIntValidator
from PyQt5.QtCore import Qt
from .one_rep_max_calculator import OneRepMaxCalculator
from fitness_tracker.user_profile.profile_db import fetch_units
from fitness_tracker.config import db_path

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__()
    self.setStyleSheet("""
    QWidget{
      font-family: Montserrat;
      color:#c7c7c7;
      font-weight: bold;      
      font-size:12px;
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
    }
    """)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    grid.setContentsMargins(0, 5, 5, 5)
    grid.addLayout(self.create_description(), 0, 0, 1, 1)
    grid.addLayout(self.create_calculator(), 1, 0, 1, 1)
    grid.addWidget(self.create_progression(), 2, 0, 15, 1)
    self.setLayout(grid)

  def create_description(self):
    description_layout = QVBoxLayout()

    description_label = QLabel("""Calculate your one rep max based on results of your previous lifts. Use the suggested progression \ntoward the max to get the most out of your max out.""", self)
    description_label.setFont(QFont("Montserrat", 12))
    description_label.setStyleSheet("font-size: 16px")
    description_label.setFixedHeight(43)
    description_layout.addWidget(description_label)

    return description_layout

  def create_calculator(self):
    title_frame = QFrame()
    title_layout = QVBoxLayout()
    title_frame.setLayout(title_layout)
    
    calculator_layout = QVBoxLayout()
    
    calculator_frame = QFrame()
    calculator_frame.setObjectName("graphObj")
    calculator_frame.setFrameStyle(QFrame.Box)
    calculator_frame.setLineWidth(3)
    calculator_frame.setStyleSheet("""#graphObj {color: #322d2d;}""")
    calculator_frame.setFixedWidth(450) 
    
    weight_label = QLabel("Weight", self)
    self.weight_entry = QLineEdit()
    weight_validator = QIntValidator(1, 999)
    self.weight_entry.setValidator(weight_validator)
    
    reps_label = QLabel("Repetitions", self)
    self.reps_entry = QLineEdit()
    rep_validator = QIntValidator(1, 20)
    self.reps_entry.setValidator(rep_validator)
    
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
    
    wrapper_layout = QHBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    wrapper_layout.addWidget(self.result_label)
    
    return wrapper_layout

  def create_progression(self):
    frame = QFrame()
    progression_layout = QVBoxLayout()

    frame.setLayout(progression_layout)
    
    self.table = QTableWidget(7,5)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.table.verticalHeader().setVisible(False)
    
    table_items = {"table_headers": ["Set", "%", "Weight", "Reps", "Rest"], 
                   "sets": ["1", "2", "3", "4", "5", "6", "7", "8"],
                   "percentages": ["~30%-50%", "~60%", "~70%", "~80%", "~90%", "~100%", "~102%"],
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
          _item.setFlags(Qt.ItemIsEnabled)
          if key == "sets": self.table.setItem(i, 0, _item)
          elif key == "percentages": self.table.setItem(i, 1, _item)
          elif key == "weight": self.table.setItem(i, 2, _item)
          elif key == "number_of_reps": self.table.setItem(i, 3, _item)
          elif key == "rest": self.table.setItem(i, 4, _item)

    for i in range(7):
      self.table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    grid = QGridLayout()
    grid_frame = QFrame()
    grid_frame.setObjectName("graphObj")
    grid_frame.setFrameStyle(QFrame.Box)
    grid_frame.setLineWidth(3)
    grid_frame.setStyleSheet("""#graphObj {color: #322d2d;}""")
    grid.addWidget(self.table, 1, 0, 1, 1)
    grid_frame.setLayout(grid)
    return grid_frame

  def calculate(self):
    try:
      units = fetch_units()
      weight = self.weight_entry.text()
      repetitions = self.reps_entry.text()
      units = "kg" if units == "metric" else "lb"
      
      calc = OneRepMaxCalculator(weight, repetitions)
      results = calc.results()
      self.result_label.setText("".join(["Estimated ORM: ", str(results[5]), " ", units]))
      self.result_label.setStyleSheet("font-size: 16px;")
      j = 0
      for i in range(7):
        self.table.item(i, 2).setText("".join([str(results[j]), " ", units]))
        j += 1
    except ValueError:
      pass
