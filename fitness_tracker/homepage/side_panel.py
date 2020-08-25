from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class SidePanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()

  def create_panel(self):
    general_layout = QVBoxLayout()
    home_button = QPushButton("Home", self)
    user_button = QPushButton("User Physique", self)
     
    notes_layout = QVBoxLayout()
    notes_label = QLabel("Notes", self)
    notes_label.setFont(QFont("Ariel", 15))
    notes_label.setAlignment(Qt.AlignLeft)
    lifts_button = QPushButton("Big Lifts", self)
    workouts_button = QPushButton("Workouts", self)
    calories_button = QPushButton("Calories", self)
    weight_button = QPushButton("Weight Loss", self)
    
    calculators_layout = QVBoxLayout()
    calculators_label = QLabel("Calculators", self)
    calculators_label.setFont(QFont("Ariel", 15))
    calculators_label.setAlignment(Qt.AlignLeft)
    max_button = QPushButton("1 Rep Max", self)
    fat_button = QPushButton("Body Fat", self)
    strength_es_button = QPushButton("Strength Estimator", self)
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Statistics", self)
    stats_label.setFont(QFont("Ariel", 15))
    stats_label.setAlignment(Qt.AlignLeft)
    strength_button = QPushButton("Strength", self)
    weight_loss_button = QPushButton("Weight Loss", self)
    
    layouts = {general_layout: [home_button, user_button], 
               notes_layout: [notes_label, lifts_button, workouts_button, calories_button, weight_button], 
               calculators_layout: [calculators_label, max_button, fat_button, strength_es_button],
               stats_layout: [stats_label, strength_button, weight_loss_button]}
    
    for key, value in layouts.items():
      for widget in value:
        key.addWidget(widget)

    grid = QGridLayout()
    grid.addLayout(general_layout, 0, 0, 2, 1)
    grid.addLayout(notes_layout, 3, 0, 8, 1)
    grid.addLayout(calculators_layout, 12, 0, 7, 1)
    grid.addLayout(stats_layout, 20, 0, 5, 1)
    self.setLayout(grid)
