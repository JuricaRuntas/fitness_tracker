from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QCursor, QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize, QFileInfo, pyqtSignal

path = QFileInfo(__file__).absolutePath()

class SearchResultsPanel(QWidget):
  return_to_food_db_signal = pyqtSignal(str)
  show_scrambled_eggs_signal = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__(parent)
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
    back_button.setIcon(QIcon("".join([path, "/icons/back.png"])))
    back_button.setIconSize(QSize(24, 24))
    back_button.setCursor(QCursor(Qt.PointingHandCursor))
    back_button.clicked.connect(lambda: self.return_to_food_db_signal.emit("Return to FoodDatabase"))

    results_label = QLabel('Found 25 results for "eggs"')
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
    
    result_layout = QVBoxLayout()
    result_image = QLabel()
    result_image = QPushButton()
    result_image.setFlat(True)
    result_image.setIcon(QIcon("".join([path, "/placeholder_images/eggs.jpg"])))
    result_image.setIconSize(QSize(250, 200))
    result_image.setCursor(QCursor(Qt.PointingHandCursor))
    result_label = QLabel("Eggs")
    result_label.setAlignment(Qt.AlignCenter)

    result_layout.addWidget(result_image)
    result_layout.addWidget(result_label)
    
    result_layout1 = QVBoxLayout()
    result_image1 = QPushButton()
    result_image1.setFlat(True)
    result_image1.setIcon(QIcon("".join([path, "/placeholder_images/boiled_eggs.jpg"])))
    result_image1.setIconSize(QSize(250, 200))
    result_image1.setCursor(QCursor(Qt.PointingHandCursor))

    result_label1 = QLabel("Boiled Eggs")
    result_label1.setAlignment(Qt.AlignCenter)

    result_layout1.addWidget(result_image1)
    result_layout1.addWidget(result_label1)
    
    result_layout2 = QVBoxLayout()
    result_image2 = QPushButton()
    result_image2.setFlat(True)
    result_image2.setIcon(QIcon("".join([path, "/placeholder_images/scrambled_eggs.jpg"])))
    result_image2.setIconSize(QSize(250, 200))
    result_image2.setCursor(QCursor(Qt.PointingHandCursor))
    result_image2.clicked.connect(lambda: self.show_scrambled_eggs_signal.emit("Scrambled Eggs"))

    result_label2 = QLabel("Scrambled Eggs")
    result_label2.setAlignment(Qt.AlignCenter)

    result_layout2.addWidget(result_image2)
    result_layout2.addWidget(result_label2)

    results_grid.addLayout(result_layout, 0, 0)
    results_grid.addLayout(result_layout1, 0, 1)
    results_grid.addLayout(result_layout2, 0, 2) 
    
    return results_grid
