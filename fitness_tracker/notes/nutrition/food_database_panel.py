from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
from .spoonacular import FoodDatabase
from fitness_tracker.homepage.side_panel import SidePanel

class FoodDatabasePanel(QWidget):
  search_signal = pyqtSignal(str)
  emit_search_results = pyqtSignal(object)

  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

  def create_panel(self):
    grid = QGridLayout()
    
    description_layout = QVBoxLayout()
    find_food_label = QLabel("Find Food")
    find_food_label.setFont(QFont("Ariel", 50))
    find_food_label.setAlignment(Qt.AlignCenter)
    
    description_label = QLabel(
    """<html><head/><body><p align="center">Lorem ipsum dolor sit amet, consectetur adipiscing elit.
       </p><p align="center">Nulla congue consequat ante, vitae viverra quam pharetra non.
       </p><p align="center">Hac habitasse platea dictumst. Aliquam eu mi imperdiet.</p></body></html>
    """)
    
    description_layout.addWidget(find_food_label)
    description_layout.addWidget(description_label)

    search_layout = QHBoxLayout()
    self.search_bar = QLineEdit()
    self.search_bar.setStyleSheet("background-color:white;")
    self.search_bar.setPlaceholderText("Search")
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding)
    spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding)

    search_layout.addSpacerItem(spacer)
    search_layout.addWidget(self.search_bar)
    search_layout.addSpacerItem(spacer1)
    
    search_button_layout = QHBoxLayout()
    search_button = QPushButton("Search")
    search_button.setStyleSheet("color:white;background-color: #440D0F;")
    search_button.setCursor(QCursor(Qt.PointingHandCursor))
    search_button.clicked.connect(self.emit_search_signal)

    spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding)
    spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding)
    search_button_layout.addSpacerItem(spacer2)
    search_button_layout.addWidget(search_button)
    search_button_layout.addSpacerItem(spacer3)

    grid.addLayout(description_layout, 0, 0)
    grid.addLayout(search_layout, 1, 0)
    grid.addLayout(search_button_layout, 2, 0)
    self.setLayout(grid)

  def emit_search_signal(self):
    if not self.search_bar.text() == '':
      api = FoodDatabase()
      search = self.search_bar.text()
      search_results = api.food_search(search, 6)
      api.download_food_images(search_results, 250)
      self.emit_search_results.emit([search_results, search])
      self.search_signal.emit("Search")
