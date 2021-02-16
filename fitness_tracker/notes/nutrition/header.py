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
    

    
    grid.addLayout(nutrition_title_layout, 0, 0)
    self.setLayout(grid)


