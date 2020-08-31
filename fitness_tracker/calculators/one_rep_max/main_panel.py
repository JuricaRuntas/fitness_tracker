from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
    weight_entry = QLineEdit()
    
    reps_label = QLabel("Repetitions", self)
    reps_entry = QLineEdit()
    
    calculate_button = QPushButton("Calculate", self)

    calculator_layout.addWidget(weight_label)
    calculator_layout.addWidget(weight_entry)
    calculator_layout.addWidget(reps_label)
    calculator_layout.addWidget(reps_entry)
    calculator_layout.addWidget(calculate_button)
    
    calculator_frame.setLayout(calculator_layout)
    
    result_label = QLabel("Your estimated one rep max is: 250 kg", self)
    
    wrapper_layout = QVBoxLayout()
    wrapper_layout.addWidget(title_frame)
    wrapper_layout.addWidget(calculator_frame)
    wrapper_layout.addWidget(result_label)
    
    return wrapper_layout

  def create_progression(self):
    frame = QFrame()
    progression_layout = QVBoxLayout()
    
    progression_label = QLabel("Progression to your max", self)
    progression_label.setAlignment(Qt.AlignCenter)
    progression_label.setFont(QFont("Ariel", 15))

    progression_layout.addWidget(progression_label)
    frame.setLayout(progression_layout)
    
    table = QTableWidget(7,5)
    table.verticalHeader().setVisible(False)
    
    table_items = {"table_headers": ["Set", "%", "Weight", "Reps", "Rest"], 
                   "sets": ["1", "2", "3", "4", "5", "6", "7", "8"],
                   "percentages": ["~30%-50%", "~60%", "~70", "~80%", "~90%", "~102%", "~104%"],
                   "number_of_reps": ["8", "5", "3", "1", "1", "1", "1"],
                   "rest": ["~2 min", "~2 min", "~3 min", "~3 min", "~5 min", "~5-15 min", "~5-15 min"]}
    
    for key, value in table_items.items():
      for i, item in enumerate(value):
        if key == "table_headers":
          table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
          table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        else:
          _item = QTableWidgetItem(item)
          _item.setTextAlignment(Qt.AlignCenter)
          if key == "sets": table.setItem(i, 0, _item)
          elif key == "percentages": table.setItem(i, 1, _item)
          elif key == "number_of_reps": table.setItem(i, 3, _item)
          elif key == "rest": table.setItem(i, 4, _item)

    for i in range(7):
      table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    grid = QGridLayout()
    grid.addWidget(frame, 0, 0)
    grid.addWidget(table, 1, 0, 1, 1)

    return grid 