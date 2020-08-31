from PyQt5.QtWidgets import (QWidget, QFrame, QGridLayout, 
                             QHBoxLayout, QVBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QFileInfo, QSize
from PyQt5.QtGui import QIcon

path = QFileInfo(__file__).absolutePath()
icon_size = QSize(24, 24)

class MainPanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()
    
    grid.addLayout(self.create_description(), 0, 0, 1, 2)
    grid.addWidget(self.create_graphs(), 1, 0, 2, 2)
    grid.addLayout(self.create_notes(), 3, 0, 2, 2)
    self.setLayout(grid)

  def create_description(self):
    notes_description = QVBoxLayout()
    notes_label = QLabel("Store food, track calories, make progress.") 
    notes_label.setFixedHeight(30)

    notes_description.addWidget(notes_label)
    return notes_description

  def create_graphs(self):
    graph_layout = QHBoxLayout()
    
    graph1 = QWidget()
    graph1.setStyleSheet("background-color: purple")
    graph2 = QWidget()
    graph2.setStyleSheet("background-color: orange")

    graph_layout.addWidget(graph1)
    graph_layout.addWidget(graph2)

    frame = QFrame()
    frame.setFrameStyle(QFrame.StyledPanel)
    frame.setLayout(graph_layout)

    return frame

  def create_notes(self):
    
    table = QTableWidget(2, 5)
    table.verticalHeader().setVisible(False)
    
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks", "Drinks"]
    
    plus_button = QPushButton(QIcon("".join([path, "/icons/plus.png"])), "Add Food", self)
    plus_button1 = QPushButton(QIcon("".join([path, "/icons/plus.png"])), "Add Food", self)
    plus_button2 = QPushButton(QIcon("".join([path, "/icons/plus.png"])), "Add Food", self)
    plus_button3 = QPushButton(QIcon("".join([path, "/icons/plus.png"])), "Add Food", self)
    plus_button4 = QPushButton(QIcon("".join([path, "/icons/plus.png"])), "Add Food", self)
    self.setStyleSheet("QPushButton{border: none}") 
    
    buttons = [plus_button, plus_button1, plus_button2, plus_button3, plus_button4] 
    j = i = 0
    for item in meals:
      table.setHorizontalHeaderItem(i, QTableWidgetItem(item))
      table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
      table.setCellWidget(0, j, buttons[i])
      j += 1
      i += 1

    for i in range(2):
      table.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
    
    label = QLabel("Monday, 31.2.2005", self)
    label.setAlignment(Qt.AlignCenter)
    
    table_title_layout = QHBoxLayout()
    
    left_button = QPushButton(QIcon("".join([path, "/icons/left.png"])), "", self)
    right_button = QPushButton(QIcon("".join([path, "/icons/right.png"])), "",self)
    
    table_title_layout.addWidget(left_button)
    table_title_layout.addWidget(label)
    table_title_layout.addWidget(right_button)
    
    title_frame = QFrame()
    title_frame.setFrameStyle(QFrame.StyledPanel)
    title_frame.setLayout(table_title_layout)

    table_frame = QFrame()
    table_frame.setFrameStyle(QFrame.StyledPanel)
    table_wrapper = QVBoxLayout()
    table_wrapper.addWidget(table)
    table_frame.setLayout(table_wrapper)
    

    grid = QGridLayout()
    grid.addWidget(title_frame, 0, 0)
    grid.addWidget(table_frame, 1, 0)
    
    return grid
