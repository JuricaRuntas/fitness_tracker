import os
from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QCursor, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal

path = os.path.abspath(os.path.dirname(__file__))

icons_path = os.path.join(path, "icons")
images_path = os.path.join(path, "food_images")

class SearchResultsPanel(QWidget):
  return_to_food_db_signal = pyqtSignal(str)
  food_panel_signal = pyqtSignal(int)

  def __init__(self, parent, search_results):
    super().__init__(parent)
    self.search = search_results[1]
    self.search_results = search_results[0]
    self.create_panel()
    self.setStyleSheet("QLabel{color:white;}")

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

    results_label = QLabel('Found %s results for "%s"' % (len(self.search_results), self.search))
    results_label.setFont(QFont("Ariel", 15))
    
    spacer = QSpacerItem(40, 20, QSizePolicy.Expanding)
    
    search_bar = QLineEdit()
    search_bar.setStyleSheet("background-color:white;")
    search_bar.setPlaceholderText("Search")
    
    search_button = QPushButton("Search")
    search_button.setStyleSheet("background-color: #440D0F;color:white;")
    search_button.setCursor(QCursor(Qt.PointingHandCursor))

    summary_layout.addWidget(back_button)
    summary_layout.addWidget(results_label)
    summary_layout.addSpacerItem(spacer)
    summary_layout.addWidget(search_bar)
    summary_layout.addWidget(search_button)

    return summary_layout

  def create_results(self):
    results_grid = QGridLayout()
    
    result_layouts = [None] * len(self.search_results)
    result_images = [None] * len(self.search_results)
    result_labels = [None] * len(self.search_results)
    
    i = 0
    row = 0
    for result in self.search_results:
      result_layouts[i] = QVBoxLayout()
      result_images[i] = QPushButton()
      result_labels[i] = QLabel()

      result_images[i].setProperty("food_id", result["id"])
      result_images[i].clicked.connect(partial(self.food_panel_signal.emit, result_images[i].property("food_id")))
      result_images[i].setFlat(True)
      result_images[i].setIcon(QIcon(os.path.join(images_path, result["image"])))
      result_images[i].setIconSize(QSize(250, 200))
      result_images[i].setCursor(QCursor(Qt.PointingHandCursor))
      result_labels[i].setText(result["name"].capitalize())
      result_labels[i].setAlignment(Qt.AlignCenter)

      result_layouts[i].addWidget(result_images[i])
      result_layouts[i].addWidget(result_labels[i])
      results_grid.addLayout(result_layouts[i], row, i)
      i += 1
      if i == 3: 
        i = 0
        row += 1
    return results_grid 
