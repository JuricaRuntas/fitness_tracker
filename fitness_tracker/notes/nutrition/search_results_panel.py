import os
from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QCursor, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from .spoonacular import FoodDatabase
from fitness_tracker.database_wrapper import DatabaseWrapper

path = os.path.abspath(os.path.dirname(__file__))

icons_path = os.path.join(path, "icons")
images_path = os.path.join(path, "food_images")

class SearchResultsPanel(QWidget):
  return_to_food_db_signal = pyqtSignal(str)
  food_panel_signal = pyqtSignal(int)

  def __init__(self, parent, search_results):
    super().__init__(parent)
    self.query_number = 6
    self.search = search_results[1]
    self.search_results = search_results[0]
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")
    self.db_wrapper = DatabaseWrapper()

  def create_panel(self):
    grid = QGridLayout()
    grid.addLayout(self.create_results_summary(), 0, 0)
    grid.addLayout(self.create_results(), 1, 0)
    self.setLayout(grid)

  def create_results_summary(self):
    summary_layout = QHBoxLayout()
    back_button = QPushButton()
    back_button.setFlat(True)
    back_button.setIcon(QIcon(os.path.join(icons_path, "back.png")))
    back_button.setIconSize(QSize(24, 24))
    back_button.setCursor(QCursor(Qt.PointingHandCursor))
    back_button.clicked.connect(lambda: self.return_to_food_db_signal.emit("Return to FoodDatabase"))

    self.results_label = QLabel('Found %s results for "%s"' % (len(self.search_results), self.search))
    self.results_label.setFont(QFont("Ariel", 15))
    
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding)
    
    search_bar = QLineEdit()
    search_bar.setStyleSheet("background-color:white;")
    search_bar.setPlaceholderText("Search")
    
    search_button = QPushButton("Search")
    search_button.setStyleSheet("background-color: #440D0F;color:white;")
    search_button.setCursor(QCursor(Qt.PointingHandCursor))
    search_button.clicked.connect(lambda:self.search_database(search_bar.text()))

    search_bar.returnPressed.connect(search_button.click)

    summary_layout.addWidget(back_button)
    summary_layout.addWidget(self.results_label)
    summary_layout.addSpacerItem(spacer)
    summary_layout.addWidget(search_bar)
    summary_layout.addWidget(search_button)

    return summary_layout

  def create_results(self):
    self.results_grid = QGridLayout()
    
    self.result_layouts = [None] * self.query_number
    self.result_images = [None] * self.query_number
    self.result_labels = [None] * self.query_number
    
    i = 0
    row = 0
    columns = 0
    for i in range(self.query_number):
    #for result in self.search_results:
      self.result_layouts[i] = QVBoxLayout()
      self.result_layouts[i].setSpacing(15)
      self.result_images[i] = QPushButton()
      self.result_labels[i] = QLabel()
      
      if i + 1 <= len(self.search_results):
        self.result_images[i].setProperty("food_id", self.search_results[i]["id"])
        self.result_images[i].clicked.connect(partial(self.food_panel_signal.emit, self.result_images[i].property("food_id")))
        self.result_images[i].setFlat(True)
        self.result_images[i].setIcon(QIcon(os.path.join(images_path, self.search_results[i]["image"])))
        self.result_images[i].setIconSize(QSize(250, 200))
        self.result_images[i].setCursor(QCursor(Qt.PointingHandCursor))
        self.result_labels[i].setText(self.search_results[i]["name"].capitalize())
        self.result_labels[i].setAlignment(Qt.AlignCenter)
      else:
        self.result_images[i].setVisible(False)

      self.result_layouts[i].addWidget(self.result_images[i])
      self.result_layouts[i].addWidget(self.result_labels[i])
      self.result_layouts[i].addStretch(0)
      self.results_grid.addLayout(self.result_layouts[i], row, columns)
      i += 1
      columns += 1
      if i == 3: 
        row += 1
        columns = 0
    return self.results_grid 

  def search_database(self, text):
    if not text == '' and self.db_wrapper.connection_exists:
      api = FoodDatabase()
      query = text
      search_results = api.food_search(query, self.query_number)
      api.download_food_images(search_results, 250)
      for item in self.result_images:
        item.setVisible(False)
      for item in self.result_labels:
        item.setVisible(False) 
      self.results_label.setText('Found %s results for "%s"' % (len(search_results), text))
      i = 0
      for i in range(self.query_number): 
        if i + 1 <= len(search_results):
          self.result_images[i].setProperty("food_id", search_results[i]["id"])
          self.result_images[i].clicked.connect(partial(self.food_panel_signal.emit, self.result_images[i].property("food_id")))
          self.result_images[i].setFlat(True)
          self.result_images[i].setIcon(QIcon(os.path.join(images_path, search_results[i]["image"])))
          self.result_images[i].setIconSize(QSize(250, 200))
          self.result_images[i].setCursor(QCursor(Qt.PointingHandCursor))
          self.result_labels[i].setText(search_results[i]["name"].capitalize())
          self.result_labels[i].setAlignment(Qt.AlignCenter)
          self.result_images[i].setVisible(True)
          self.result_labels[i].setVisible(True)
        else:
          self.result_images[i].setVisible(False)
          self.result_labels[i].setVisible(False)
        i += 1    
