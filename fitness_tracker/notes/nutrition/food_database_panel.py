from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal
from .spoonacular import FoodDatabase
from fitness_tracker.homepage.side_panel import SidePanel
from fitness_tracker.database_wrapper import DatabaseWrapper

class FoodDatabasePanel(QWidget):
  search_signal = pyqtSignal(object)

  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
    self.setStyleSheet("""
    QWidget{
      color:#c7c7c7;
      font-weight: bold;
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
    QComboBox{
      border-radius: 4px;
      font-size: 18px;
      font-weight: bold;
      white-space:nowrap;
      text-align: left;
      padding-left: 5%;
      font-family: Montserrat;
      min-height: 28px;
      background-color: #440D0F;
    }
    QComboBox:down-arrow{
      width: 0px;
      height: 0px;
      background: #d3d3d3; 
      opacity:0
    }
    QComboBox:drop-down{
      background-color: #440D0F;
      border: 0px;
      opacity:0;
      border-radius: 0px;
      width: 0px;
      height: 0px;
    }
    QComboBox:hover:!pressed{
      background-color: #5D1A1D;
    }
    QComboBox:pressed{
      background-color: #551812;
    }
    QLineEdit{
      padding: 6px;
      background-color: rgb(33,33,33);
      border: 1px solid;
      border-color: #cdcdcd;
    }
    """)
    self.db_wrapper = DatabaseWrapper()

  def create_panel(self):
    grid = QGridLayout()
    
    description_layout = QVBoxLayout()
    find_food_label = QLabel("Find Food")
    find_food_label.setFont(QFont("Ariel", 50))
    find_food_label.setAlignment(Qt.AlignCenter)
    
    description_label = QLabel(
    """<html><head/><body><p align="center">Use this search engine to find nutritional facts of almost every ingredient in the world.</p></body></html>
    """)
    description_label.setWordWrap(True)
    description_label.setFont(QFont("Cantonese", 18))
    description_label.setStyleSheet("""font-weight: normal;""")
    
    description_layout.addWidget(find_food_label)
    description_layout.addWidget(description_label)

    search_layout = QHBoxLayout()
    self.search_bar = QLineEdit()
    self.search_bar.setPlaceholderText("Enter Ingredient")
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding)
    spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding)

    search_layout.addSpacerItem(spacer)
    search_layout.addWidget(self.search_bar)
    search_layout.addSpacerItem(spacer1)
    
    search_button_layout = QHBoxLayout()
    search_button = QPushButton("Search")
    search_button.setFixedWidth(240)
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
    if not self.search_bar.text() == '' and self.db_wrapper.connection_exists:
      api = FoodDatabase()
      search = self.search_bar.text()
      search_results = api.food_search(search, 6)
      api.download_food_images(search_results, 250)
      self.search_signal.emit([search_results, search])
