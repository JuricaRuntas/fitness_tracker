import os
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QPoint, QDir, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QCursor, QPainter, QColor, QBrush, QFontDatabase
from fitness_tracker.login.login_helpers import logout_current_user

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "icons")

icons = {"Home": os.path.join(path, "home.png"),
         "Profile": os.path.join(path, "user.png"),
         "Logout": os.path.join(path, "logout.png"),
         "Compound Exercises": os.path.join(path, "big_lifts.png"),
         "Workouts": os.path.join(path, "workouts.png"),
         "Nutrition": os.path.join(path, "calories.png"),
         "Weight Loss": os.path.join(path, "weight_loss.png"),
         "1 Rep Max": os.path.join(path, "one_rep_max.png"),
         "Body Fat": os.path.join(path, "body_fat.png"),
         "Strength Estimator": os.path.join(path, "strength_es.png")}

icon_size = QSize(24, 24)

class SidePanel(QWidget):
  emit_layout_name = pyqtSignal(str)

  def __init__(self, parent):
    super().__init__(parent)
    self.create_panel()
    self.setMaximumWidth(201)
    self.setStyleSheet("""
                       QPushButton{
                         text-align: center;
                         background-color: #440D0F;
                         border-radius: 3px;
                         min-height: 23px;
                         min-width: 180px;
                         color: #c7c7c7;
                         font: 15px;
                         font-weight:500;
                         font-family:Montserrat;
                         padding-bottom: 3px;
                         }
                       QPushButton:hover:!pressed{
                         background-color: #5D1A1D
                       }
                       QPushButton:pressed{
                         background-color: #551812
                       }
                       """)
  
  def create_panel(self):
    line_divider_general = self.create_line_divider()
    line_divider_calc = self.create_line_divider()
    line_divider_notes = self.create_line_divider()
    line_divider_stats = self.create_line_divider()
    line_divider_logout = self.create_line_divider()

    general_layout = QVBoxLayout()
    general_layout.setContentsMargins(0, 0, 0, 0)
    home_button = QPushButton("Home", self)
    home_button.clicked.connect(lambda: self.emit_layout_name.emit(home_button.text()))
    user_button = QPushButton("Profile", self)
    user_button.clicked.connect(lambda: self.emit_layout_name.emit(user_button.text()))
    logout_button = QPushButton("Logout", self)
    logout_button.clicked.connect(lambda: self.logout())

    notes_layout = QVBoxLayout()
    notes_layout.setContentsMargins(0, 0, 0, 0)
    lifts_button = QPushButton("Compound Exercises", self)
    lifts_button.clicked.connect(lambda: self.emit_layout_name.emit(lifts_button.text()))
    workouts_button = QPushButton("Workouts", self)
    workouts_button.clicked.connect(lambda: self.emit_layout_name.emit(workouts_button.text()))
    nutrition_button = QPushButton("Nutrition", self)
    nutrition_button.clicked.connect(lambda: self.emit_layout_name.emit(nutrition_button.text()))
    weight_notes_button = QPushButton("Weight Loss", self)
    weight_notes_button.clicked.connect(lambda: self.emit_layout_name.emit(weight_notes_button.text()))
    food_database_button = QPushButton("Food Database", self)
    food_database_button.clicked.connect(lambda: self.emit_layout_name.emit(food_database_button.text()))
    
    calculators_layout = QVBoxLayout()
    calculators_layout.setContentsMargins(0, 0, 0, 0)
    max_button = QPushButton("1 Rep Max Calculator", self)
    max_button.clicked.connect(lambda: self.emit_layout_name.emit(max_button.text()))
    fat_button = QPushButton("Body Fat Calculator", self)
    fat_button.clicked.connect(lambda: self.emit_layout_name.emit(fat_button.text()))
    strength_es_button = QPushButton("Strength Estimator", self)
    strength_es_button.clicked.connect(lambda: self.emit_layout_name.emit(strength_es_button.text()))
    
    layouts = {general_layout: [line_divider_general, home_button, user_button,
                                line_divider_notes, lifts_button, workouts_button,
                                nutrition_button, weight_notes_button, food_database_button,
                                line_divider_calc, max_button, fat_button, strength_es_button,
                                line_divider_logout, logout_button],
               notes_layout: [],
               calculators_layout: [],
               }
    
    grid = QGridLayout()
    grid.setSpacing(11)
    #grid.setAlignment(Qt.AlignTop)
    
    for i, (key, value) in enumerate(layouts.items()):
      for widget in value:
        key.addWidget(widget)
        if isinstance(widget, QPushButton):
          widget.setIconSize(icon_size)
          widget.setCursor(QCursor(Qt.PointingHandCursor))
      grid.addLayout(key, i, 0)
    
    self.setLayout(grid)
  
  def logout(self):
    logout_current_user()
    self.emit_layout_name.emit("Logout")
    
  def create_line_divider(self):
    line_divider = QWidget()
    line_divider.setStyleSheet("""
    background-color: #603A36;
    """)
    line_divider.setMaximumSize(183, 3)
    return line_divider

  def paintEvent(self, event):
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.fillRect(event.rect(), QBrush(QColor(17, 16, 15, 255)))
