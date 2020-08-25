from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QFileInfo, QSize
from PyQt5.QtGui import QFont, QIcon

path = QFileInfo(__file__).absolutePath()
icon_size = QSize(24, 24)

class SidePanel(QWidget):
  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
  
  def create_panel(self):
    general_layout = QVBoxLayout()
    
    home_button = QPushButton(QIcon("".join([path, "/icons/home.png"])), "Home", self)
    home_button.setIconSize(icon_size)

    user_button = QPushButton(QIcon("".join([path, "/icons/user.png"])), "User Physique", self)
    user_button.setIconSize(icon_size)
     
    notes_layout = QVBoxLayout()
    
    notes_label = QLabel("Notes", self)
    notes_label.setFont(QFont("Ariel", 15))
    notes_label.setFixedSize(100,20)

    lifts_button = QPushButton(QIcon("".join([path, "/icons/big_lifts.png"])), "Big Lifts", self)
    lifts_button.setIconSize(icon_size)

    workouts_button = QPushButton(QIcon("".join([path, "/icons/workouts.png"])), "Workouts", self)
    workouts_button.setIconSize(icon_size)

    calories_button = QPushButton(QIcon("".join([path, "/icons/calories.png"])) ,"Calories", self)
    calories_button.setIconSize(icon_size)

    weight_button = QPushButton(QIcon("".join([path, "/icons/weight_loss.png"])), "Weight Loss", self)
    weight_button.setIconSize(icon_size)
    
    calculators_layout = QVBoxLayout()

    calculators_label = QLabel("Calculators", self)
    calculators_label.setFont(QFont("Ariel", 15))
    calculators_label.setFixedSize(100,20)
    
    max_button = QPushButton(QIcon("".join([path, "/icons/one_rep_max.png"])), "1 Rep Max", self)
    max_button.setIconSize(icon_size)

    fat_button = QPushButton(QIcon("".join([path, "/icons/body_fat.png"])), "Body Fat", self)
    fat_button.setIconSize(icon_size)

    strength_es_button = QPushButton(QIcon("".join([path, "/icons/strength_es.png"])), "Strength Estimator", self)
    strength_es_button.setIconSize(icon_size)

    stats_layout = QVBoxLayout()
    
    stats_label = QLabel("Statistics", self)
    stats_label.setFont(QFont("Ariel", 15))
    stats_label.setFixedSize(100,20)
    
    strength_button = QPushButton(QIcon("".join([path, "/icons/strength.png"])), "Strength", self)
    strength_button.setIconSize(icon_size)
    
    weight_loss_button = QPushButton(QIcon("".join([path, "/icons/weight_loss.png"])), "Weight Loss", self)
    weight_loss_button.setIconSize(icon_size)
    
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
