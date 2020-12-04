import os
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QFont, QIcon, QCursor, QPainter, QColor, QBrush

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icons")

icons = {"Home": os.path.join(path, "home.png"),
         "Profile": os.path.join(path, "user.png"),
         "Logout": os.path.join(path, "logout.png"),
         "Big Lifts": os.path.join(path, "big_lifts.png"),
         "Workouts": os.path.join(path, "workouts.png"),
         "Nutrition": os.path.join(path, "calories.png"),
         "Weight Loss Notes": os.path.join(path, "weight_loss.png"),
         "1 Rep Max": os.path.join(path, "one_rep_max.png"),
         "Body Fat": os.path.join(path, "body_fat.png"),
         "Strength Estimator": os.path.join(path, "strength_es.png"),
         "Strength": os.path.join(path, "strength.png"),
         "Weight Loss": os.path.join(path, "weight_loss.png")}

icon_size = QSize(24, 24)

class SidePanel(QWidget):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    self.create_panel()
    self.setStyleSheet("""
                       QPushButton{
                         text-align: left;
                         background-color: #440D0F;
                         color:white;}
                       QLabel{
                         color:white;
                       }
                       """) 
  
  def create_panel(self):
    general_layout = QVBoxLayout()
    overview_label = QLabel("Overview", self)
    overview_label.setFont(QFont("Ariel", 15))
    overview_label.setFixedSize(100, 20)
    home_button = QPushButton(QIcon(icons["Home"]), "Home", self)
    home_button.clicked.connect(lambda: self.controller.display_layout(home_button.text()))
    user_button = QPushButton(QIcon(icons["Profile"]), "Profile", self)
    user_button.clicked.connect(lambda: self.controller.display_layout(user_button.text()))
    logout_button = QPushButton(QIcon(icons["Logout"]), "Logout", self)
    logout_button.clicked.connect(lambda: self.controller.display_layout(logout_button.text()))

    notes_layout = QVBoxLayout()
    notes_label = QLabel("Notes", self)
    notes_label.setFont(QFont("Ariel", 15))
    notes_label.setFixedSize(100, 20)
    lifts_button = QPushButton(QIcon(icons["Big Lifts"]), "Big Lifts", self)
    lifts_button.clicked.connect(lambda: self.controller.display_layout(lifts_button.text()))
    workouts_button = QPushButton(QIcon(icons["Workouts"]), "Workouts", self)
    workouts_button.clicked.connect(lambda: self.controller.display_layout(workouts_button.text()))
    nutrition_button = QPushButton(QIcon(icons["Nutrition"]), "Nutrition", self)
    nutrition_button.clicked.connect(lambda: self.controller.display_layout(nutrition_button.text()))
    weight_notes_button = QPushButton(QIcon(icons["Weight Loss Notes"]), "Weight Loss Notes", self)
    weight_notes_button.clicked.connect(lambda: self.controller.display_layout(weight_notes_button.text()))
    
    calculators_layout = QVBoxLayout()
    calculators_label = QLabel("Calculators", self)
    calculators_label.setFont(QFont("Ariel", 15))
    calculators_label.setFixedSize(120, 20)
    max_button = QPushButton(QIcon(icons["1 Rep Max"]), "1 Rep Max", self)
    max_button.clicked.connect(lambda: self.controller.display_layout(max_button.text()))
    fat_button = QPushButton(QIcon(icons["Body Fat"]), "Body Fat", self)
    fat_button.clicked.connect(lambda: self.controller.display_layout(fat_button.text()))
    strength_es_button = QPushButton(QIcon(icons["Strength Estimator"]), "Strength Estimator", self)
    strength_es_button.clicked.connect(lambda: self.controller.display_layout(strength_es_button.text()))
    
    stats_layout = QVBoxLayout()
    stats_label = QLabel("Statistics", self)
    stats_label.setFont(QFont("Ariel", 15))
    stats_label.setFixedSize(100, 20  )
    strength_button = QPushButton(QIcon(icons["Strength"]), "Strength", self)
    strength_button.clicked.connect(lambda: self.controller.display_layout(strength_button.text()))
    weight_loss_button = QPushButton(QIcon(icons["Weight Loss"]), "Weight Loss", self)
    weight_loss_button.clicked.connect(lambda: self.controller.display_layout(weight_loss_button.text()))
    
    layouts = {general_layout: [overview_label, home_button, user_button, logout_button], 
               notes_layout: [notes_label, lifts_button, workouts_button, nutrition_button, weight_notes_button], 
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

  def paintEvent(self, event):
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.fillRect(event.rect(), QBrush(QColor(20, 18, 17, 255)))
