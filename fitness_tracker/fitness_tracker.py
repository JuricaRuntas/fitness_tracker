from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QColor
import sys
import sqlite3
import os
from homepage.homepage import Homepage
from user_physique.user_physique import UserPhysique
from calculators import *
from notes import *
from statistics import *
from login.login import Login
from signup.signup import Signup
from signup.signup_questions_panel import SignupQuestions
from titlebar import TitleBar

class FitnessTracker(QMainWindow):
  def __init__(self):
    super().__init__()
    self.create_window()
    self.cw = Homepage(self) if self.user_info_exists() else Login(self)
    self.layouts = {"Login": Login, "Signup": Signup, "Continue": SignupQuestions,
                    "Home": Homepage, "User Data and Settings": UserPhysique,
                    "Big Lifts": BigLiftsNotes, "Workouts": WorkoutsNotes, "Nutrition": CaloriesNotes,
                    "Weight Loss Notes": WeightLossNotes, "1 Rep Max": OneRepMaxCalculator,
                    "Body Fat": BodyFatCalculator, "Strength Estimator": StrengthEstimator,
                    "Strength": StrengthStats, "Weight Loss": WeightLossStats}
    self.colorize_background()
    self.colorize_foreground()
    self.setup_borders()
    self.title_bar = TitleBar(self)
    main_widget = self.setup_main_layout()
    self.setCentralWidget(main_widget)

  def colorize_background(self):
    self.setAutoFillBackground(True)
    bg_palette = self.palette()
    bg_palette.setColor(self.backgroundRole(), QColor(25,23,22))
    self.setPalette(bg_palette)

  def colorize_foreground(self):
    fg_palette = self.palette()
    fg_palette.setColor(self.foregroundRole(), QColor(255,255,255))
    self.setPalette(fg_palette)

  def create_window(self):
    self.setWindowTitle("Fitness Tracker")
    self.resize(1126, 733)
    self.center()
    self.show()

  def setup_borders(self):
    #self.setWindowFlags(Qt.FramelessWindowHint)
    self.show()

  def setup_main_layout(self):
    main_layout = QVBoxLayout()
    main_layout.setSpacing(10)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.addWidget(self.title_bar)
    spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
    main_layout.addItem(spacer)
    main_layout.addWidget(self.cw)
    central_spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)
    main_layout.addItem(central_spacer)
    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    return main_widget
  
  def center(self):
    window = self.frameGeometry()
    center_point = QDesktopWidget().availableGeometry().center()
    window.moveCenter(center_point)
    self.move(window.topLeft())
  
  def display_layout(self, layout):
    for key, value in self.layouts.items():
      if layout == key:
        self.setCentralWidget(value(self))

  def user_info_exists(self):
    table_exists = True
    path = os.path.normpath(QFileInfo(__file__).absolutePath())
    db_path = path.split(os.path.sep)[:-1]
    db_path = os.path.sep.join([os.path.sep.join(db_path), "db", "user_info.db"])
    
    with sqlite3.connect(db_path) as conn:
      check_for_tables = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
      cursor = conn.cursor()
      cursor.execute(check_for_tables)
      if cursor.fetchone() == None:
        table_exists = False
    return table_exists
        
if __name__ == "__main__":
  app = QApplication(sys.argv)
  ft = FitnessTracker()
  sys.exit(app.exec_())
