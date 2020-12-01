from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

class Header(QWidget):
  change_layout_signal = pyqtSignal(str)
  
  def __init__(self, parent):
    super().__init__(parent)
    self.setStyleSheet("QPushButton{color:white;background-color: #191716;}")
    self.create_header()
  
  def create_header(self):
    grid = QGridLayout()

    nutrition_title_layout = QVBoxLayout()
    nutrition_label = QLabel("Nutrition")
    nutrition_label.setFont(QFont("Ariel", 15))
    nutrition_label.setStyleSheet("color:white;font-weight:bold;")
    nutrition_label.setFixedHeight(20)

    nutrition_description = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    nutrition_description.setFont(QFont("Ariel", 9))
    nutrition_description.setStyleSheet("color:grey;")

    nutrition_title_layout.addWidget(nutrition_label)
    nutrition_title_layout.addWidget(nutrition_description)
    
    buttons_layout = QHBoxLayout()
    self.notes_button = QPushButton("Notes")
    self.notes_button.setStyleSheet("background-color: #603A40;")
    self.notes_button.setFixedSize(60, 35)
    self.notes_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.notes_button.clicked.connect(lambda: self.change_layout_signal.emit(self.notes_button.text()))
    self.food_database_button = QPushButton("Food Database")
    self.food_database_button.setFixedSize(110, 35)
    self.food_database_button.setCursor(QCursor(Qt.PointingHandCursor))
    self.food_database_button.clicked.connect(lambda: self.change_layout_signal.emit(self.food_database_button.text()))
    
    buttons_layout.addWidget(self.notes_button)
    buttons_layout.addWidget(self.food_database_button)
    
    grid.addLayout(nutrition_title_layout, 0, 0)
    grid.addLayout(buttons_layout, 0, 1)
    self.setLayout(grid)

  def set_current_layout_button(self, layout):
    if layout == "Food Database":
      self.food_database_button.setStyleSheet("background-color: #603A40;")
      self.notes_button.setStyleSheet("background-color: #191716;")
    elif layout == "Notes":
      self.notes_button.setStyleSheet("background-color: #603A40;")
      self.food_database_button.setStyleSheet("background-color: #191716;")
