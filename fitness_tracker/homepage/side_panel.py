from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
    notes_label.setFixedSize(100,20)
    lifts_button = QPushButton("Big Lifts", self)
    workouts_button = QPushButton("Workouts", self)
    calories_button = QPushButton("Calories", self)
    weight_button = QPushButton("Weight Loss", self)
    
    calculators_layout = QVBoxLayout()
    calculators_label = QLabel("Calculators", self)
    calculators_label.setFont(QFont("Ariel", 15))
    calculators_label.setFixedSize(100,20)
    max_button = QPushButton("1 Rep Max", self)
    fat_button = QPushButton("Body Fat", self)
    strength_es_button = QPushButton("Strength Estimator", self)
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Statistics", self)
    stats_label.setFont(QFont("Ariel", 15))
    stats_label.setFixedSize(100,20)
    strength_button = QPushButton("Strength", self)
    weight_loss_button = QPushButton("Weight Loss", self)
    
    layouts = {general_layout: [home_button, user_button], 
               notes_layout: [notes_label, lifts_button, workouts_button, calories_button, weight_button], 
               calculators_layout: [calculators_label, max_button, fat_button, strength_es_button],
               stats_layout: [stats_label, strength_button, weight_loss_button]}
    
    grid = QGridLayout()
    
    for i, (key, value) in enumerate(layouts.items()):
      for widget in value:
        key.addWidget(widget)
      grid.addLayout(key, i, 0)
    self.setLayout(grid)
