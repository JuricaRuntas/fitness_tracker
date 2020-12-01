from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QFileInfo, QSize
from PyQt5.QtGui import QFont, QIcon, QCursor

path = QFileInfo(__file__).absolutePath()
icon_size = QSize(24, 24)

class SidePanel(QWidget):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    self.create_panel()
    self.setStyleSheet("QPushButton{text-align: left}") 
  
  def create_panel(self):
    general_layout = QVBoxLayout()
    home_button = QPushButton(QIcon("".join([path, "/icons/home.png"])), "Home", self)
    home_button.clicked.connect(lambda: self.controller.display_layout(home_button.text()))
    user_button = QPushButton(QIcon("".join([path, "/icons/user.png"])), "User Data and Settings", self)
    user_button.clicked.connect(lambda: self.controller.display_layout(user_button.text()))
    
    notes_layout = QVBoxLayout()
    notes_label = QLabel("Notes", self)
    notes_label.setFont(QFont("Ariel", 15))
    notes_label.setFixedSize(100, 20)
    lifts_button = QPushButton(QIcon("".join([path, "/icons/big_lifts.png"])), "Big Lifts", self)
    lifts_button.clicked.connect(lambda: self.controller.display_layout(lifts_button.text()))
    workouts_button = QPushButton(QIcon("".join([path, "/icons/workouts.png"])), "Workouts", self)
    workouts_button.clicked.connect(lambda: self.controller.display_layout(workouts_button.text()))
    calories_button = QPushButton(QIcon("".join([path, "/icons/calories.png"])) ,"Nutrition", self)
    calories_button.clicked.connect(lambda: self.controller.display_layout(calories_button.text()))
    weight_notes_button = QPushButton(QIcon("".join([path, "/icons/weight_loss.png"])), "Weight Loss Notes", self)
    weight_notes_button.clicked.connect(lambda: self.controller.display_layout(weight_notes_button.text()))
    
    calculators_layout = QVBoxLayout()
    calculators_label = QLabel("Calculators", self)
    calculators_label.setFont(QFont("Ariel", 15))
    calculators_label.setFixedSize(120, 20)
    max_button = QPushButton(QIcon("".join([path, "/icons/one_rep_max.png"])), "1 Rep Max", self)
    max_button.clicked.connect(lambda: self.controller.display_layout(max_button.text()))
    fat_button = QPushButton(QIcon("".join([path, "/icons/body_fat.png"])), "Body Fat", self)
    fat_button.clicked.connect(lambda: self.controller.display_layout(fat_button.text()))
    strength_es_button = QPushButton(QIcon("".join([path, "/icons/strength_es.png"])), "Strength Estimator", self)
    strength_es_button.clicked.connect(lambda: self.controller.display_layout(strength_es_button.text()))
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Statistics", self)
    stats_label.setFont(QFont("Ariel", 15))
    stats_label.setFixedSize(100, 20)
    strength_button = QPushButton(QIcon("".join([path, "/icons/strength.png"])), "Strength", self)
    strength_button.clicked.connect(lambda: self.controller.display_layout(strength_button.text()))
    weight_loss_button = QPushButton(QIcon("".join([path, "/icons/weight_loss.png"])), "Weight Loss", self)
    weight_loss_button.clicked.connect(lambda: self.controller.display_layout(weight_loss_button.text()))
    
    layouts = {general_layout: [home_button, user_button], 
               notes_layout: [notes_label, lifts_button, workouts_button, calories_button, weight_notes_button], 
               calculators_layout: [calculators_label, max_button, fat_button, strength_es_button],
               stats_layout: [stats_label, strength_button, weight_loss_button]}
    
    grid = QGridLayout()
    self.setLayout(grid)
    
    for i, (key, value) in enumerate(layouts.items()):
      for widget in value:
        key.addWidget(widget)
        if isinstance(widget, QPushButton):
          widget.setIconSize(icon_size)
          widget.setCursor(QCursor(Qt.PointingHandCursor))
      grid.addLayout(key, i, 0)
