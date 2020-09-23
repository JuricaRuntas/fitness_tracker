from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QSize, Qt, QFileInfo

path = QFileInfo(__file__).absolutePath()

class BackExercises(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    grid = QGridLayout()

    search_bar_layout = QHBoxLayout()
    search_bar_label = QLabel("Search", self)
    search_bar = QLineEdit(self)
    search_bar_layout.addWidget(search_bar_label)
    search_bar_layout.addWidget(search_bar)
    
    pull_ups_layout = QVBoxLayout()
    pull_ups = QPushButton(self)
    pull_ups.setIcon(QIcon("".join([path, "/back_exercises/pull_ups.png"])))
    pull_ups.setIconSize(QSize(250, 150))
    pull_ups.resize(250, 150)
    pull_ups.setStyleSheet("border: none")
    pull_ups.setCursor(Qt.PointingHandCursor)

    pull_ups_label = QLabel("Pull Ups", self)
    pull_ups_label.setAlignment(Qt.AlignCenter)
    pull_ups_layout.addWidget(pull_ups)
    pull_ups_layout.addWidget(pull_ups_label)

    lat_pulldown_layout = QVBoxLayout()
    lat_pulldown = QPushButton(self)
    lat_pulldown.setIcon(QIcon("".join([path, "/back_exercises/lat_pulldown.jpeg"])))
    lat_pulldown.setIconSize(QSize(250, 150))
    lat_pulldown.resize(250, 150)
    lat_pulldown.setStyleSheet("border: none")
    lat_pulldown.setCursor(Qt.PointingHandCursor)

    lat_pulldown_label = QLabel("Lateral Pulldown", self)
    lat_pulldown_label.setAlignment(Qt.AlignCenter)
    lat_pulldown_layout.addWidget(lat_pulldown)
    lat_pulldown_layout.addWidget(lat_pulldown_label)

    barbell_row_layout = QVBoxLayout()
    barbell_row = QPushButton(self)
    barbell_row.setIcon(QIcon("".join([path, "/back_exercises/barbell_row.jpg"])))
    barbell_row.setIconSize(QSize(250, 150))
    barbell_row.resize(250, 150)
    barbell_row.setStyleSheet("border: none")
    barbell_row.setCursor(Qt.PointingHandCursor)

    barbell_row_label = QLabel("Barbell Row", self)
    barbell_row_label.setAlignment(Qt.AlignCenter)
    barbell_row_layout.addWidget(barbell_row)
    barbell_row_layout.addWidget(barbell_row_label)

    grid.addLayout(search_bar_layout, 0, 0, 1, 4)
    grid.addLayout(pull_ups_layout, 1, 0)
    grid.addLayout(lat_pulldown_layout, 1, 1)
    grid.addLayout(barbell_row_layout, 1, 2)
    self.setLayout(grid)
