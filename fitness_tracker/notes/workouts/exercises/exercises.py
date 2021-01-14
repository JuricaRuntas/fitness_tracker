import os
from functools import partial
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from ..workouts_api import WorkoutsAPI
from .exercise_info import Exercise

path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
image_path = os.path.join(path, "exercise_images") 

class Exercises(QWidget):
  show_exercise_signal = pyqtSignal(object)

  def __init__(self, parent, muscle_group):
    super().__init__(parent)
    self.api = WorkoutsAPI()
    self.muscle_group = muscle_group
    self.exercises = self.api.fetch_exercises(muscle_group, limit=10)
    self.api.download_exercise_images(self.exercises)
    self.create_panel()
    
  def create_panel(self):
    self.grid = QGridLayout()
    
    search_bar_layout = QHBoxLayout()
    search_bar_label = QLabel("Search", self)
    search_bar = QLineEdit(self)
    search_button = QPushButton()
    search_bar_layout.addWidget(search_bar_label)
    search_bar_layout.addWidget(search_bar)
    search_bar_layout.addWidget(search_button)
    self.grid.addLayout(search_bar_layout, 0, 0)
    
    exercise_layouts = [None] * len(self.exercises)
    exercise_images = [None] * len(self.exercises)
    exercise_labels = [None] * len(self.exercises)
     
    i, row = 1, 1
    for j, exercise in enumerate(self.exercises):
      if len(exercise["image"]) == 0: continue
      exercise_layouts[j] = QVBoxLayout()
      exercise_images[j] = QPushButton()
      exercise_labels[j] = QLabel()

      image_name = os.path.basename(exercise["image"][0])
      exercise_image_path = os.path.join(image_path, image_name)
      exercise_images[j].setProperty("exercise_info", exercise)
      exercise_images[j].clicked.connect(partial(self.show_exercise_signal.emit, exercise_images[j].property("exercise_info")))
      exercise_images[j].setIcon(QIcon(exercise_image_path))
      exercise_images[j].setIconSize(QSize(250, 150))
      exercise_images[j].resize(250, 150)
      exercise_images[j].setCursor(Qt.PointingHandCursor)
      exercise_images[j].setFlat(True)
      exercise_labels[j].setText(exercise["name"])
      exercise_labels[j].setAlignment(Qt.AlignCenter)

      exercise_layouts[j].addWidget(exercise_images[j])
      exercise_layouts[j].addWidget(exercise_labels[j])
      i += 1
      self.grid.addLayout(exercise_layouts[j], row, i)
      if i == 3:
        i = 0
        row += 1
    self.setLayout(self.grid)
